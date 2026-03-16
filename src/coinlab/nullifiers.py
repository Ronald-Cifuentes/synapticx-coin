"""
Nullifiers: conjunto de nullifiers usados para evitar doble gasto.

Un nullifier se revela cuando se gasta una nota.
Si el mismo nullifier aparece dos veces, la segunda transacción es inválida.
"""

from typing import Set


def nullifier_set() -> Set[str]:
    """Crea un conjunto vacío de nullifiers usados."""
    return set()


def is_nullifier_used(nullifiers: Set[str], nullifier: str) -> bool:
    """Verifica si un nullifier ya fue usado."""
    return nullifier in nullifiers


def add_nullifier(nullifiers: Set[str], nullifier: str) -> None:
    """Registra un nullifier como usado."""
    nullifiers.add(nullifier)
