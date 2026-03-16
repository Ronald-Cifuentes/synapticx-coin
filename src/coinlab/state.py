"""
Estado canónico: commitments conocidos, nullifiers usados.

El estado NO tiene balances por cuenta en cadena (privacidad).
Índice auxiliar solo para demos/tests.
"""

from typing import Dict, List, Optional, Set

from .transactions import PrivateTransaction


class ChainState:
    """
    Estado de la cadena: commitments activos, nullifiers gastados.
    Índice owner->amount solo para demos; no es parte del protocolo.
    """

    commitments: Set[str]  # hashes de commitments conocidos
    nullifiers_used: Set[str]
    # Índice auxiliar: owner -> suma de amounts en commitments que "posee"
    # En producción el usuario no revela esto; es solo para tests/demos
    _owner_index: Dict[str, int]

    def __init__(self) -> None:
        self.commitments = set()
        self.nullifiers_used = set()
        self._owner_index = {}

    def has_commitment(self, c: str) -> bool:
        return c in self.commitments

    def has_nullifier_used(self, nf: str) -> bool:
        return nf in self.nullifiers_used

    def can_apply_transaction(
        self,
        tx: PrivateTransaction,
        known_commitments: Optional[Set[str]] = None,
    ) -> tuple[bool, Optional[str]]:
        """
        Verifica si la tx puede aplicarse.
        known_commitments: si None, asumimos que los inputs existen.
        """
        # Nullifiers no usados
        for nf in tx.nullifiers():
            if self.has_nullifier_used(nf):
                return False, f"Nullifier ya usado: {nf[:16]}..."

        # Inputs deben existir como commitments
        if known_commitments is not None:
            for inp in tx.inputs:
                if inp.commitment not in known_commitments and inp.commitment not in self.commitments:
                    return False, f"Commitment no conocido: {inp.commitment[:16]}..."

        return True, None

    def apply_transaction(
        self,
        tx: PrivateTransaction,
        output_owners: Optional[List[str]] = None,
    ) -> None:
        """
        Aplica la transacción al estado.
        output_owners: solo para índice auxiliar en demos; None = no indexar.
        """
        for inp in tx.inputs:
            self.nullifiers_used.add(inp.nullifier)
            self.commitments.discard(inp.commitment)

        for out in tx.outputs:
            self.commitments.add(out.commitment)

        # Índice auxiliar (solo demos)
        if output_owners is not None and len(output_owners) == len(tx.outputs):
            for owner, out in zip(output_owners, tx.outputs):
                self._owner_index[owner] = self._owner_index.get(owner, 0) + out.amount

    def add_commitment(self, comm: str, owner: Optional[str] = None, amount: int = 0) -> None:
        """Añade un commitment (ej. coinbase)."""
        self.commitments.add(comm)
        if owner is not None:
            self._owner_index[owner] = self._owner_index.get(owner, 0) + amount

    def get_owner_balance(self, owner: str) -> int:
        """Balance según índice auxiliar (solo demos). No resta gastos."""
        return self._owner_index.get(owner, 0)