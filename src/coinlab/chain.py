"""
Cadena lineal PoW: bloques en orden, reorg por trabajo acumulado.
"""

from typing import List, Optional

from .blocks import Block, BlockHeader, compute_merkle_root, expected_block_reward
from .config import Config
from .crypto_primitives import hash_hex
from .pow import cumulative_work, mine_block, validate_block_pow
from .state import ChainState
from .transactions import PrivateTransaction, validate_transaction_basic
from .types import BlockHash


GENESIS_PREV = "0" * 64


def validate_block(
    block: Block,
    height: int,
    config: Config,
) -> tuple[bool, Optional[str]]:
    """
    Valida bloque: PoW, merkle root, coinbase policy.
    No valida transacciones contra estado (eso se hace al aplicar).
    """
    if not validate_block_pow(block, config.difficulty):
        return False, "PoW inválido"
    expected_root = compute_merkle_root(block.transactions)
    if block.header.merkle_root != expected_root:
        return False, f"Merkle root inválido: esperado {expected_root[:16]}..."
    expected_reward = expected_block_reward(height, config)
    if block.coinbase_amount != expected_reward:
        return False, f"Coinbase inválida: {block.coinbase_amount} != {expected_reward}"
    return True, None


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
        Valida: prev_hash, PoW, merkle root, coinbase policy, inputs existen.
        """
        height = len(self.blocks)
        expected_prev = self.tip_hash()
        if block.header.prev_hash != expected_prev:
            return False, f"prev_hash mismatch: expected {expected_prev[:16]}..."

        ok, err = validate_block(block, height, self.config)
        if not ok:
            return False, err

        for tx in block.transactions:
            ok, err = validate_transaction_basic(tx)
            if not ok:
                return False, f"Tx inválida: {err}"
            ok, err = self.state.can_apply_transaction(tx)
            if not ok:
                return False, f"Tx no aplicable: {err}"
            self.state.apply_transaction(tx)

        self.state.add_commitment(
            block.coinbase_commitment,
            owner=coinbase_owner,
            amount=block.coinbase_amount,
        )

        self.blocks.append(block)
        return True, None

    def validate_chain(self) -> tuple[bool, Optional[str]]:
        """Valida toda la cadena: PoW, merkle, coinbase, inputs existen."""
        state = ChainState()
        for i, block in enumerate(self.blocks):
            prev = GENESIS_PREV if i == 0 else self.blocks[i - 1].block_hash()
            if block.header.prev_hash != prev:
                return False, f"Block {i}: prev_hash inválido"
            ok, err = validate_block(block, i, self.config)
            if not ok:
                return False, f"Block {i}: {err}"
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
        Reorg: reemplaza por blocks si tiene MAYOR trabajo acumulado.
        No basta con ser más larga; debe tener más trabajo.
        """
        our_work = cumulative_work(self.blocks)
        their_work = cumulative_work(blocks)
        if their_work <= our_work:
            return False, f"Cadena alternativa no más pesada: {their_work} <= {our_work}"
        state = ChainState()
        prev_hash = GENESIS_PREV
        for i, block in enumerate(blocks):
            if block.header.prev_hash != prev_hash:
                return False, "Cadena alternativa inválida"
            ok, err = validate_block(block, i, self.config)
            if not ok:
                return False, f"Cadena alternativa: {err}"
            for tx in block.transactions:
                ok, err = state.can_apply_transaction(tx)
                if not ok:
                    return False, f"Cadena alternativa: {err}"
                state.apply_transaction(tx)
            state.add_commitment(block.coinbase_commitment, amount=block.coinbase_amount)
            prev_hash = block.block_hash()
        self.blocks = blocks
        self.state = state
        return True, None
