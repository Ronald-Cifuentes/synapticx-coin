"""
Modelo de notas privadas.

Cada nota representa un UTXO privado: owner, amount, nonce, asset.
El commitment es público; el secret permite generar el nullifier al gastar.
"""

import json
import secrets
from dataclasses import dataclass, field
from typing import Optional

from .crypto_primitives import commitment_for_note, nullifier_for_note
from .types import CommitmentHash, NoteId


@dataclass
class Note:
    """
    Nota privada: UTXO con owner, amount, nonce, asset.
    El secret se usa para generar nullifier al gastar.
    """

    note_id: NoteId
    owner_key: str
    amount: int
    nonce: str
    asset_id: str
    secret: str  # Para nullifier; en producción sería material de clave

    def commitment(self) -> CommitmentHash:
        """Commitment público de la nota."""
        return CommitmentHash(
            commitment_for_note(
                self.owner_key,
                self.amount,
                self.nonce,
                self.asset_id,
            )
        )

    def nullifier(self) -> str:
        """Nullifier para gastar (evitar doble gasto)."""
        return nullifier_for_note(self.secret, self.commitment())


@dataclass
class NoteCommitment:
    """Referencia a un commitment en el estado (sin datos privados)."""

    commitment_hash: CommitmentHash
    amount: int
    asset_id: str


def create_note(
    owner_key: str,
    amount: int,
    asset_id: str = "BASE",
    nonce: Optional[str] = None,
    secret: Optional[str] = None,
    note_id: Optional[NoteId] = None,
) -> Note:
    """Crea una nota con nonce y secret aleatorios si no se proveen."""
    nonce = nonce or secrets.token_hex(16)
    secret = secret or secrets.token_hex(32)
    note_id = note_id or NoteId(secrets.token_hex(8))
    return Note(
        note_id=note_id,
        owner_key=owner_key,
        amount=amount,
        nonce=nonce,
        asset_id=asset_id,
        secret=secret,
    )


def note_commitment(note: Note) -> NoteCommitment:
    """Extrae el commitment público de una nota."""
    return NoteCommitment(
        commitment_hash=note.commitment(),
        amount=note.amount,
        asset_id=note.asset_id,
    )


def serialize_note(note: Note) -> str:
    """Serializa nota a JSON (para persistencia local; no para red)."""
    return json.dumps({
        "note_id": note.note_id,
        "owner_key": note.owner_key,
        "amount": note.amount,
        "nonce": note.nonce,
        "asset_id": note.asset_id,
        "secret": note.secret,
    })


def deserialize_note(data: str) -> Note:
    """Deserializa nota desde JSON."""
    d = json.loads(data)
    return Note(
        note_id=NoteId(d["note_id"]),
        owner_key=d["owner_key"],
        amount=d["amount"],
        nonce=d["nonce"],
        asset_id=d["asset_id"],
        secret=d["secret"],
    )
