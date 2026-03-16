"""
Bloques: header + transacciones.

Cadena lineal PoW, no blockDAG.
"""

from dataclasses import dataclass, field
from typing import List

from .crypto_primitives import hash_hex
from .transactions import PrivateTransaction
from .types import BlockHash


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
