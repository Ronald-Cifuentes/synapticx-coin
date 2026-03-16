"""
Bloques: header + transacciones.

Cadena lineal PoW, no blockDAG.
"""

from dataclasses import dataclass
from typing import List, Optional, Set

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


def block_has_internal_nullifier_conflict(
    transactions: List[PrivateTransaction],
) -> tuple[bool, Optional[str]]:
    """
    Detecta si dos tx del mismo bloque usan el mismo nullifier.
    Retorna (has_conflict, error_message).
    """
    seen: Set[str] = set()
    for tx in transactions:
        for nf in tx.nullifiers():
            if nf in seen:
                return True, f"Nullifier duplicado en bloque: {nf[:16]}..."
            seen.add(nf)
    return False, None


def expected_block_reward(height: int, config: Config) -> int:
    """
    Recompensa esperada para un bloque a la altura dada.
    MVP: constante config.block_reward para toda altura.
    """
    return config.block_reward


def expected_block_difficulty(height: int, config: Config) -> int:
    """
    Dificultad esperada para un bloque a la altura dada.
    MVP: constante config.difficulty. Obligatorio: el header NO puede declarar otra.
    """
    return config.difficulty


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
    coinbase_commitment: str
    coinbase_amount: int
    coinbase_owner_secret_hash: str = ""  # hash(secret) para autorización de gasto

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
