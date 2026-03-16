"""
Bloques: header + transacciones.

Cadena lineal PoW, no blockDAG.
"""

from dataclasses import dataclass
from typing import List

from .config import Config
from .crypto_primitives import hash_hex
from .transactions import PrivateTransaction
from .types import BlockHash


def compute_merkle_root(transactions: List[PrivateTransaction]) -> str:
    """
    Merkle root de las transacciones del bloque.
    MVP: hash de tx_ids concatenados. Root vacío si no hay txs.
    """
    tx_ids = [tx.tx_id for tx in transactions]
    return hash_hex("|".join(tx_ids) if tx_ids else "")


def expected_block_reward(height: int, config: Config) -> int:
    """
    Recompensa esperada para un bloque a la altura dada.
    MVP: constante config.block_reward para toda altura.
    """
    return config.block_reward


@dataclass
class BlockHeader:
    """Header del bloque."""

    prev_hash: str
    merkle_root: str  # MVP: hash de tx_ids concatenados
    timestamp: int
    nonce: int
    difficulty: int


@dataclass
class Block:
    """Bloque completo."""

    header: BlockHeader
    transactions: List[PrivateTransaction]
    coinbase_commitment: str  # Commitment de recompensa al minero
    coinbase_amount: int

    def block_hash(self) -> BlockHash:
        """Hash del bloque (header)."""
        payload = (
            f"{self.header.prev_hash}|"
            f"{self.header.merkle_root}|"
            f"{self.header.timestamp}|"
            f"{self.header.nonce}|"
            f"{self.header.difficulty}"
        )
        return BlockHash(hash_hex(payload))
