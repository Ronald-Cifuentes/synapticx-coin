"""
Cadena lineal PoW: bloques en orden, reorg corto si llega cadena más pesada.
"""

from typing import List, Optional

from .blocks import Block, BlockHeader
from .config import Config
from .crypto_primitives import hash_hex
from .pow import mine_block, validate_block_pow
from .state import ChainState
from .transactions import PrivateTransaction, validate_transaction_basic
from .types import BlockHash


GENESIS_PREV = "0" * 64


class Blockchain:
    """Cadena de bloques lineal con estado canónico."""

    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = config or Config.default()
        self.blocks: List[Block] = []
        self.state = ChainState()

    def create_genesis(self, faucet_address: str):
        """Crea y añade bloque genesis. Retorna (block, faucet_note)."""
        from .notes import create_note

        faucet_note = create_note(
            faucet_address,
            self.config.block_reward,
            self.config.default_asset_id,
            nonce=hash_hex("genesis"),
            secret="genesis_faucet_secret_mvp",
        )
        coinbase_commitment = faucet_note.commitment()
        block = mine_block(
            prev_hash=GENESIS_PREV,
            merkle_root=hash_hex(""),
            timestamp=0,
            difficulty=self.config.difficulty,
            transactions=[],
            coinbase_commitment=coinbase_commitment,
            coinbase_amount=self.config.block_reward,
        )
        ok, err = self.add_block(block, coinbase_owner=faucet_address)
        if not ok:
            raise RuntimeError(f"Genesis falló: {err}")
        return block, faucet_note

    def tip_hash(self) -> str:
        """Hash del último bloque."""
        if not self.blocks:
            return GENESIS_PREV
        return self.blocks[-1].block_hash()

    def add_block(
        self,
        block: Block,
        coinbase_owner: Optional[str] = None,
    ) -> tuple[bool, Optional[str]]:
        """
        Añade bloque si es válido.
        coinbase_owner: para índice auxiliar en demos.
        """
        # Prev hash
        expected_prev = self.tip_hash()
        if block.header.prev_hash != expected_prev:
            return False, f"prev_hash mismatch: expected {expected_prev[:16]}..."

        # PoW
        if not validate_block_pow(block, self.config.difficulty):
            return False, "PoW inválido"

        # Transacciones
        for tx in block.transactions:
            ok, err = validate_transaction_basic(tx)
            if not ok:
                return False, f"Tx inválida: {err}"
            ok, err = self.state.can_apply_transaction(tx)
            if not ok:
                return False, f"Tx no aplicable: {err}"
            self.state.apply_transaction(tx)

        # Coinbase
        self.state.add_commitment(
            block.coinbase_commitment,
            owner=coinbase_owner,
            amount=block.coinbase_amount,
        )

        self.blocks.append(block)
        return True, None

    def validate_chain(self) -> tuple[bool, Optional[str]]:
        """Valida toda la cadena. Estado debe ser reproducible."""
        state = ChainState()
        for i, block in enumerate(self.blocks):
            prev = GENESIS_PREV if i == 0 else self.blocks[i - 1].block_hash()
            if block.header.prev_hash != prev:
                return False, f"Block {i}: prev_hash inválido"
            if not validate_block_pow(block, self.config.difficulty):
                return False, f"Block {i}: PoW inválido"
            for tx in block.transactions:
                ok, err = validate_transaction_basic(tx)
                if not ok:
                    return False, f"Block {i}: {err}"
                ok, err = state.can_apply_transaction(tx)
                if not ok:
                    return False, f"Block {i}: {err}"
                state.apply_transaction(tx)
            state.add_commitment(block.coinbase_commitment, amount=block.coinbase_amount)
        return True, None

    def reorg_to(self, blocks: List[Block]) -> tuple[bool, Optional[str]]:
        """
        Reorg corto: reemplaza la cadena actual por blocks si es más pesada.
        Peso = longitud (MVP simple).
        """
        if len(blocks) <= len(self.blocks):
            return False, "Cadena alternativa no más larga"
        # Validar cadena alternativa
        state = ChainState()
        prev_hash = GENESIS_PREV
        for block in blocks:
            if block.header.prev_hash != prev_hash:
                return False, "Cadena alternativa inválida"
            if not validate_block_pow(block, self.config.difficulty):
                return False, "Cadena alternativa PoW inválido"
            for tx in block.transactions:
                ok, _ = state.can_apply_transaction(tx)
                if not ok:
                    return False, "Cadena alternativa con tx conflictiva"
                state.apply_transaction(tx)
            state.add_commitment(block.coinbase_commitment, amount=block.coinbase_amount)
            prev_hash = block.block_hash()
        self.blocks = blocks
        self.state = state
        return True, None
