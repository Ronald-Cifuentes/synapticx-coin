"""
Estado canónico: notas con NoteRecord (amount, asset_id, owner_secret_hash), nullifiers usados.

Cada nota almacenada permite verificar autorización real: hash(secret) == owner_secret_hash.
El estado NO tiene balances por cuenta en cadena (privacidad).
Índice auxiliar solo para demos/tests.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from .crypto_primitives import nullifier_for_note, owner_secret_hash
from .transactions import PrivateTransaction


@dataclass
class NoteRecord:
    """Registro persistido de nota. Fuente de verdad para gasto."""

    amount: int
    asset_id: str
    owner_secret_hash: str


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
    Estado de la cadena: notas con NoteRecord (amount, asset_id, owner_secret_hash).
    Valida autorización real: hash(secret) == owner_secret_hash.
    all_commitments_seen: commitments históricos (no reutilizables).
    Índice owner->amount solo para demos; no es parte del protocolo.
    """

    commitments: Set[str]
    notes: Dict[str, NoteRecord]  # commitment -> NoteRecord
    nullifiers_used: Set[str]
    all_commitments_seen: Set[str]  # histórico: ningún commitment puede reaparecer
    _owner_index: Dict[str, int]

    def __init__(self) -> None:
        self.commitments = set()
        self.notes = {}
        self.nullifiers_used = set()
        self.all_commitments_seen = set()
        self._owner_index = {}

    def has_commitment(self, c: str) -> bool:
        return c in self.commitments

    def has_nullifier_used(self, nf: str) -> bool:
        return nf in self.nullifiers_used

    def can_apply_transaction(
        self,
        tx: PrivateTransaction,
        known_commitments: Optional[Set[str]] = None,
        known_notes: Optional[Dict[str, NoteRecord]] = None,
    ) -> tuple[bool, Optional[str]]:
        """
        Verifica si la tx puede aplicarse.
        Valida: commitment existe, autorización real (hash(secret)==owner_secret_hash),
        nullifier derivado, amount/asset desde estado para conservation.
        """
        notes = known_notes if known_notes is not None else self.notes
        available = known_commitments if known_commitments is not None else self.commitments

        for nf in tx.nullifiers():
            if self.has_nullifier_used(nf):
                return False, f"Nullifier ya usado: {nf[:16]}..."

        total_in_from_state = 0
        asset_from_state: Optional[str] = None

        for inp in tx.inputs:
            comm = inp.commitment if isinstance(inp.commitment, str) else str(inp.commitment)
            if comm not in available:
                return False, f"Input commitment inexistente: {comm[:16]}..."
            if comm not in notes:
                return False, f"Nota sin registro para commitment: {comm[:16]}..."
            rec = notes[comm]
            if owner_secret_hash(inp.secret) != rec.owner_secret_hash:
                return False, f"Secret no autorizado: commitment ajeno no puede gastarse con secret arbitrario"
            expected_nf = nullifier_for_note(inp.secret, comm)
            if inp.nullifier != expected_nf:
                return False, f"Nullifier no deriva de witness: {inp.nullifier[:16]}..."
            total_in_from_state += rec.amount
            if asset_from_state is None:
                asset_from_state = rec.asset_id
            elif asset_from_state != rec.asset_id:
                return False, "Asset mezclado en inputs"

        total_out_plus_fee = sum(o.amount for o in tx.outputs) + tx.fee
        if total_in_from_state != total_out_plus_fee:
            return False, f"Desbalance: in={total_in_from_state} (desde estado), out+fee={total_out_plus_fee}"

        outputs_seen: Set[str] = set()
        all_seen = getattr(self, "all_commitments_seen", set()) or set()
        for out in tx.outputs:
            if asset_from_state is not None and out.asset_id != asset_from_state:
                return False, f"Asset falsificado en output: {out.asset_id} != {asset_from_state}"
            c = out.commitment if isinstance(out.commitment, str) else str(out.commitment)
            if c in all_seen:
                return False, f"Commitment reutilizado: {c[:16]}... ya existe"
            if c in outputs_seen:
                return False, f"Output duplicado en misma tx: {c[:16]}..."
            outputs_seen.add(c)

        return True, None

    def apply_transaction(
        self,
        tx: PrivateTransaction,
        output_owners: Optional[List[str]] = None,
    ) -> None:
        """
        Aplica la transacción al estado.
        Rechaza overwrite: no permite commitment reutilizado.
        output_owners: solo para índice auxiliar en demos; None = no indexar.
        """
        for inp in tx.inputs:
            comm = inp.commitment if isinstance(inp.commitment, str) else str(inp.commitment)
            self.nullifiers_used.add(inp.nullifier)
            self.commitments.discard(comm)
            self.notes.pop(comm, None)

        for out in tx.outputs:
            c = out.commitment if isinstance(out.commitment, str) else str(out.commitment)
            if c in self.all_commitments_seen:
                raise ValueError(f"Commitment reutilizado: {c[:16]}... ya existe")
            self.all_commitments_seen.add(c)
            self.commitments.add(c)
            self.notes[c] = NoteRecord(
                amount=out.amount,
                asset_id=out.asset_id,
                owner_secret_hash=out.owner_secret_hash,
            )

        if output_owners is not None and len(output_owners) == len(tx.outputs):
            for owner, out in zip(output_owners, tx.outputs):
                self._owner_index[owner] = self._owner_index.get(owner, 0) + out.amount

    def add_commitment(
        self,
        comm: str,
        owner: Optional[str] = None,
        amount: int = 0,
        asset_id: str = "BASE",
        owner_secret_hash_val: Optional[str] = None,
    ) -> tuple[bool, Optional[str]]:
        """Añade un commitment (ej. coinbase) con NoteRecord completo. Rechaza reuse."""
        if comm in self.all_commitments_seen:
            return False, f"Coinbase commitment reutilizado: {comm[:16]}..."
        self.all_commitments_seen.add(comm)
        self.commitments.add(comm)
        self.notes[comm] = NoteRecord(
            amount=amount,
            asset_id=asset_id,
            owner_secret_hash=owner_secret_hash_val or owner_secret_hash(""),
        )
        if owner is not None:
            self._owner_index[owner] = self._owner_index.get(owner, 0) + amount
        return True, None

    def get_owner_balance(self, owner: str) -> int:
        """Balance según índice auxiliar (solo demos). No resta gastos."""
        return self._owner_index.get(owner, 0)

    def copy(self) -> "ChainState":
        """Copia profunda del estado. Para staged application atómica."""
        other = ChainState()
        other.commitments = self.commitments.copy()
        other.notes = {k: NoteRecord(v.amount, v.asset_id, v.owner_secret_hash) for k, v in self.notes.items()}
        other.nullifiers_used = self.nullifiers_used.copy()
        other.all_commitments_seen = self.all_commitments_seen.copy()
        other._owner_index = self._owner_index.copy()
        return other