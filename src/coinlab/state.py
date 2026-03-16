"""
Estado canónico: notas (commitment->amount,asset), nullifiers usados.

Cada nota almacenada tiene amount y asset_id para validar gastos.
El estado NO tiene balances por cuenta en cadena (privacidad).
Índice auxiliar solo para demos/tests.
"""

from typing import Dict, List, Optional, Set, Tuple

from .crypto_primitives import nullifier_for_note
from .transactions import PrivateTransaction


def tx_inputs_exist_in_state(
    tx: PrivateTransaction,
    available_commitments: Set[str],
) -> tuple[bool, Optional[str]]:
    """
    Verifica que todos los inputs de la tx existan en el conjunto de commitments disponibles.
    Retorna (ok, error_message). NO valida witness ni amount real.
    """
    for inp in tx.inputs:
        comm = inp.commitment if isinstance(inp.commitment, str) else str(inp.commitment)
        if comm not in available_commitments:
            return False, f"Input commitment inexistente: {comm[:16]}..."
    return True, None


class ChainState:
    """
    Estado de la cadena: notas (commitment->amount,asset), nullifiers gastados.
    notes permite validar amount y asset_id real al gastar.
    Índice owner->amount solo para demos; no es parte del protocolo.
    """

    commitments: Set[str]
    notes: Dict[str, Tuple[int, str]]  # commitment -> (amount, asset_id)
    nullifiers_used: Set[str]
    _owner_index: Dict[str, int]

    def __init__(self) -> None:
        self.commitments = set()
        self.notes = {}
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
        known_notes: Optional[Dict[str, Tuple[int, str]]] = None,
    ) -> tuple[bool, Optional[str]]:
        """
        Verifica si la tx puede aplicarse.
        Valida: commitment existe, amount/asset coinciden con nota, nullifier derivado correctamente.
        """
        notes = known_notes if known_notes is not None else self.notes
        available = known_commitments if known_commitments is not None else self.commitments

        for nf in tx.nullifiers():
            if self.has_nullifier_used(nf):
                return False, f"Nullifier ya usado: {nf[:16]}..."

        for inp in tx.inputs:
            comm = inp.commitment if isinstance(inp.commitment, str) else str(inp.commitment)
            if comm not in available:
                return False, f"Input commitment inexistente: {comm[:16]}..."
            if comm not in notes:
                return False, f"Nota sin amount/asset para commitment: {comm[:16]}..."
            stored_amount, stored_asset = notes[comm]
            if inp.amount != stored_amount:
                return False, f"Amount falsificado: declarado={inp.amount}, real={stored_amount}"
            if inp.asset_id != stored_asset:
                return False, f"Asset falsificado: {inp.asset_id} != {stored_asset}"
            expected_nf = nullifier_for_note(inp.secret, comm)
            if inp.nullifier != expected_nf:
                return False, f"Nullifier no deriva de witness: {inp.nullifier[:16]}..."

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
            comm = inp.commitment if isinstance(inp.commitment, str) else str(inp.commitment)
            self.nullifiers_used.add(inp.nullifier)
            self.commitments.discard(comm)
            self.notes.pop(comm, None)

        for out in tx.outputs:
            c = out.commitment if isinstance(out.commitment, str) else str(out.commitment)
            self.commitments.add(c)
            self.notes[c] = (out.amount, out.asset_id)

        if output_owners is not None and len(output_owners) == len(tx.outputs):
            for owner, out in zip(output_owners, tx.outputs):
                self._owner_index[owner] = self._owner_index.get(owner, 0) + out.amount

    def add_commitment(
        self,
        comm: str,
        owner: Optional[str] = None,
        amount: int = 0,
        asset_id: str = "BASE",
    ) -> None:
        """Añade un commitment (ej. coinbase) con amount y asset_id."""
        self.commitments.add(comm)
        self.notes[comm] = (amount, asset_id)
        if owner is not None:
            self._owner_index[owner] = self._owner_index.get(owner, 0) + amount

    def get_owner_balance(self, owner: str) -> int:
        """Balance según índice auxiliar (solo demos). No resta gastos."""
        return self._owner_index.get(owner, 0)

    def copy(self) -> "ChainState":
        """Copia profunda del estado. Para staged application atómica."""
        other = ChainState()
        other.commitments = self.commitments.copy()
        other.notes = self.notes.copy()
        other.nullifiers_used = self.nullifiers_used.copy()
        other._owner_index = self._owner_index.copy()
        return other