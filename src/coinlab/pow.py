"""
PoW simple: encontrar nonce tal que hash(block) empiece con N ceros (hex).

MVP: no es minería real, solo modela la semántica.
"""

from .blocks import Block, BlockHeader
from .crypto_primitives import hash_hex
from .types import BlockHash


def meets_difficulty(h: str, difficulty: int) -> bool:
    """Verifica si el hash cumple la dificultad (N ceros al inicio en hex)."""
    prefix = "0" * difficulty
    return h.startswith(prefix)


def mine_block(
    prev_hash: str,
    merkle_root: str,
    timestamp: int,
    difficulty: int,
    transactions: list,
    coinbase_commitment: str,
    coinbase_amount: int,
) -> Block:
    """
    Mina un bloque: busca nonce hasta cumplir dificultad.
    """
    nonce = 0
    while True:
        header = BlockHeader(
            prev_hash=prev_hash,
            merkle_root=merkle_root,
            timestamp=timestamp,
            nonce=nonce,
            difficulty=difficulty,
        )
        block = Block(
            header=header,
            transactions=transactions,
            coinbase_commitment=coinbase_commitment,
            coinbase_amount=coinbase_amount,
        )
        h = block.block_hash()
        if meets_difficulty(h, difficulty):
            return block
        nonce += 1


def validate_block_pow(block: Block, difficulty: int) -> bool:
    """Valida que el PoW del bloque sea correcto."""
    h = block.block_hash()
    return meets_difficulty(h, difficulty)
