"""
Transacciones privadas: consumen notas, revelan nullifiers, crean nuevos commitments.

Conservación: sum(inputs desde estado) == sum(outputs) + fee. Input.amount/asset_id no son fuente de verdad.
tx_id = H(payload canónico) para que alterar blocks.json invalide merkle/block_hash.
"""

import json
from dataclasses import dataclass
from typing import List, Optional

from .crypto_primitives import hash_hex, nullifier_for_note, owner_secret_hash
from .notes import Note, create_note
from .types import CommitmentHash, TxId


def _tx_canonical_payload(tx: "PrivateTransaction") -> str:
    """
    Serialización canónica determinística del payload de la tx.
    Incluye todo lo que afecta validez y estado.
    """
    inp = [
        {
            "c": str(i.commitment),
            "n": i.nullifier,
            "a": i.amount,
            "as": i.asset_id,
            "s": i.secret,
        }
        for i in tx.inputs
    ]
    out = [
        {
            "c": str(o.commitment),
            "a": o.amount,
            "as": o.asset_id,
            "o": o.owner_secret_hash,
        }
        for o in tx.outputs
    ]
    obj = {"fee": tx.fee, "inputs": inp, "outputs": out}
    return json.dumps(obj, sort_keys=True)


def tx_id_from_payload(tx: "PrivateTransaction") -> TxId:
    """tx_id = H(payload canónico). Compromiso criptográfico del payload."""
    return TxId(hash_hex(_tx_canonical_payload(tx)))


def verify_tx_id(tx: "PrivateTransaction") -> tuple[bool, Optional[str]]:
    """
    Verifica que tx.tx_id coincida con H(payload).
    Si no coincide: payload alterado o formato legacy (tx_id aleatorio).
    """
    expected = tx_id_from_payload(tx)
    if tx.tx_id != expected:
        return False, (
            f"Tx payload alterado o formato legacy: tx_id no deriva del payload. "
            f"Esperado {expected[:16]}..., actual {tx.tx_id[:16]}..."
        )
    return True, None


@dataclass
class TransactionInput:
    """Input: commitment + nullifier + amount + asset_id + witness (secret).
    El secret permite derivar nullifier; amount y asset se resuelven desde la nota en estado, no desde el input.
    """

    commitment: CommitmentHash
    nullifier: str
    amount: int
    asset_id: str
    secret: str  # Witness mínimo: para verificar nullifier = H(secret|commitment)


@dataclass
class TransactionOutput:
    """Output: nuevo commitment de nota creada.
    owner_secret_hash: obligatorio para que el output sea gastable.
    amount/asset_id: metadata; la verdad para gasto sale del NoteRecord en estado.
    """

    commitment: CommitmentHash
    amount: int
    asset_id: str
    owner_secret_hash: str  # hash(secret) del receptor; obligatorio para autorización


@dataclass
class PrivateTransaction:
    """Transacción privada: inputs, outputs, fee."""

    tx_id: TxId
    inputs: List[TransactionInput]
    outputs: List[TransactionOutput]
    fee: int

    def input_amount(self) -> int:
        return sum(i.amount for i in self.inputs)

    def output_amount(self) -> int:
        return sum(o.amount for o in self.outputs)

    def nullifiers(self) -> List[str]:
        return [i.nullifier for i in self.inputs]


def create_transfer_transaction(
    input_notes: List[Note],
    output_amounts: List[int],
    output_owners: List[str],
    fee: int = 0,
    tx_id: Optional[TxId] = None,
) -> PrivateTransaction:
    """
    Crea una transacción de transferencia.
    input_notes: notas a consumir
    output_amounts: montos para cada output
    output_owners: dueño de cada output
    fee: se quema en conservación; el minero recibe solo block_reward (no fees)
    """
    if len(output_amounts) != len(output_owners):
        raise ValueError("output_amounts y output_owners deben tener misma longitud")

    total_in = sum(n.amount for n in input_notes)
    total_out = sum(output_amounts) + fee
    if total_in != total_out:
        raise ValueError(
            f"Desbalance: inputs={total_in}, outputs+fee={total_out}"
        )

    inputs: List[TransactionInput] = []
    for note in input_notes:
        comm = note.commitment()
        nf = nullifier_for_note(note.secret, comm)
        inputs.append(
            TransactionInput(
                commitment=comm,
                nullifier=nf,
                amount=note.amount,
                asset_id=note.asset_id,
                secret=note.secret,
            )
        )

    output_notes = [
        create_note(owner, amount, input_notes[0].asset_id)
        for owner, amount in zip(output_owners, output_amounts)
    ]
    outputs = [
        TransactionOutput(
            commitment=n.commitment(),
            amount=n.amount,
            asset_id=n.asset_id,
            owner_secret_hash=owner_secret_hash(n.secret),
        )
        for n in output_notes
    ]

    tx = PrivateTransaction(
        tx_id=TxId(""),
        inputs=inputs,
        outputs=outputs,
        fee=fee,
    )
    tx.tx_id = tx_id or tx_id_from_payload(tx)
    return tx


def create_transfer_with_output_notes(
    input_notes: List[Note],
    output_amounts: List[int],
    output_owners: List[str],
    fee: int = 0,
    tx_id: Optional[TxId] = None,
) -> tuple[PrivateTransaction, List[Note]]:
    """
    Crea transfer y retorna las notas de salida (con secret) para el receptor.
    El emisor crea las notas y las entrega off-chain al receptor.
    """
    output_notes = [
        create_note(owner, amount, input_notes[0].asset_id)
        for owner, amount in zip(output_owners, output_amounts)
    ]
    outputs = [
        TransactionOutput(
            commitment=n.commitment(),
            amount=n.amount,
            asset_id=n.asset_id,
            owner_secret_hash=owner_secret_hash(n.secret),
        )
        for n in output_notes
    ]
    total_in = sum(n.amount for n in input_notes)
    total_out = sum(output_amounts) + fee
    if total_in != total_out:
        raise ValueError(f"Desbalance: inputs={total_in}, outputs+fee={total_out}")

    inputs = []
    for note in input_notes:
        comm = note.commitment()
        nf = nullifier_for_note(note.secret, comm)
        inputs.append(
            TransactionInput(
                commitment=comm,
                nullifier=nf,
                amount=note.amount,
                asset_id=note.asset_id,
                secret=note.secret,
            )
        )

    tx = PrivateTransaction(tx_id=TxId(""), inputs=inputs, outputs=outputs, fee=fee)
    tx.tx_id = tx_id or tx_id_from_payload(tx)
    return tx, output_notes


def validate_transaction_basic(tx: PrivateTransaction) -> tuple[bool, Optional[str]]:
    """
    Valida transacción estructural: presencia, cardinalidad, fee, formato.
    NO valida propiedad ni amount/asset real (eso depende del estado).
    """
    if not tx.inputs:
        return False, "Sin inputs"

    if not tx.outputs:
        return False, "Sin outputs"

    if tx.fee < 0:
        return False, "Fee negativa"

    total_out = tx.output_amount() + tx.fee
    if total_out < 0:
        return False, "Outputs+fee inválido"

    asset = tx.inputs[0].asset_id
    for i in tx.inputs:
        if i.asset_id != asset:
            return False, "Asset mezclado en inputs"
    seen: set = set()
    for o in tx.outputs:
        if o.asset_id != asset:
            return False, "Asset mezclado en outputs"
        c = o.commitment if isinstance(o.commitment, str) else str(o.commitment)
        if c in seen:
            return False, f"Output duplicado en misma tx: {c[:16]}..."
        seen.add(c)

    return True, None
