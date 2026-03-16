"""
Cadena lineal PoW: bloques en orden, reorg por trabajo acumulado.
"""

from typing import List, Optional

from .blocks import (
    Block,
    BlockHeader,
    block_has_internal_nullifier_conflict,
    compute_merkle_root,
    expected_block_difficulty,
    expected_block_reward,
)
from .config import Config
from .crypto_primitives import hash_hex, owner_secret_hash
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
    Validación ESTRUCTURAL del bloque (sin estado).
    Cubre: difficulty policy, PoW, merkle root, coinbase policy, conflictos internos,
    validez estructural de cada tx (validate_transaction_basic).
    NO cubre: existencia de inputs en estado (eso es contextual, se hace al aplicar).
    """
    exp_diff = expected_block_difficulty(height, config)
    if block.header.difficulty != exp_diff:
        return False, f"Difficulty incoherente: header={block.header.difficulty}, policy={exp_diff}"
    if not validate_block_pow(block, exp_diff):
        return False, "PoW inválido"
    expected_root = compute_merkle_root(block.transactions)
    if block.header.merkle_root != expected_root:
        return False, f"Merkle root inválido: esperado {expected_root[:16]}..."
    expected_reward = expected_block_reward(height, config)
    if block.coinbase_amount != expected_reward:
        return False, f"Coinbase inválida: {block.coinbase_amount} != {expected_reward}"
    has_conflict, err = block_has_internal_nullifier_conflict(block.transactions)
    if has_conflict:
        return False, err or "Nullifier duplicado en bloque"
    for tx in block.transactions:
        ok, err = validate_transaction_basic(tx)
        if not ok:
            return False, f"Tx estructural inválida: {err}"
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
        block.coinbase_owner_secret_hash = owner_secret_hash(faucet_note.secret)
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
        Añade bloque si es válido. ATÓMICO: si falla, estado no cambia.
        Valida y aplica sobre estado temporal; solo al final promueve.
        """
        height = len(self.blocks)
        expected_prev = self.tip_hash()
        if block.header.prev_hash != expected_prev:
            return False, f"prev_hash mismatch: expected {expected_prev[:16]}..."

        ok, err = validate_block(block, height, self.config)
        if not ok:
            return False, err

        temp_state = self.state.copy()
        for tx in block.transactions:
            ok, err = temp_state.can_apply_transaction(tx)
            if not ok:
                return False, f"Tx no aplicable: {err}"
            temp_state.apply_transaction(tx)

        temp_state.add_commitment(
            block.coinbase_commitment,
            owner=coinbase_owner,
            amount=block.coinbase_amount,
            asset_id=self.config.default_asset_id,
            owner_secret_hash_val=block.coinbase_owner_secret_hash or None,
        )

        self.state = temp_state
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
            state.add_commitment(
                block.coinbase_commitment,
                amount=block.coinbase_amount,
                asset_id=self.config.default_asset_id,
                owner_secret_hash_val=block.coinbase_owner_secret_hash or None,
            )
        return True, None

    def reorg_to(self, blocks: List[Block]) -> tuple[bool, Optional[str]]:
        """
        Reorg: reemplaza por blocks si tiene MAYOR trabajo acumulado.
        ATÓMICO: valida cadena alternativa completa en estado temporal;
        solo al final reemplaza. No muta nada si falla.
        Valida monetariamente (validate_transaction_basic) y contextualmente.
        """
        our_work = cumulative_work(self.blocks, self.config)
        their_work = cumulative_work(blocks, self.config)
        if their_work <= our_work:
            return False, f"Cadena alternativa no más pesada: {their_work} <= {our_work}"
        temp_state = ChainState()
        prev_hash = GENESIS_PREV
        for i, block in enumerate(blocks):
            if block.header.prev_hash != prev_hash:
                return False, "Cadena alternativa inválida"
            ok, err = validate_block(block, i, self.config)
            if not ok:
                return False, f"Cadena alternativa: {err}"
            for tx in block.transactions:
                ok, err = temp_state.can_apply_transaction(tx)
                if not ok:
                    return False, f"Cadena alternativa: {err}"
                temp_state.apply_transaction(tx)
            temp_state.add_commitment(
                block.coinbase_commitment,
                amount=block.coinbase_amount,
                asset_id=self.config.default_asset_id,
                owner_secret_hash_val=block.coinbase_owner_secret_hash or None,
            )
            prev_hash = block.block_hash()
        self.blocks = blocks
        self.state = temp_state
        return True, None
