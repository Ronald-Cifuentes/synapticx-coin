"""
Transacciones privadas: consumen notas, revelan nullifiers, crean nuevos commitments.

Conservación: sum(inputs) == sum(outputs) + fee
"""

import secrets
from dataclasses import dataclass
from typing import List, Optional

from .crypto_primitives import commitment_for_note, nullifier_for_note
from .notes import Note, create_note
from .types import CommitmentHash, TxId


@dataclass
class TransactionInput:
    """Input: commitment + nullifier + amount + asset_id + witness (secret).
    El secret permite derivar nullifier; el estado valida amount/asset contra la nota almacenada.
    """

    commitment: CommitmentHash
    nullifier: str
    amount: int
    asset_id: str
    secret: str  # Witness mínimo: para verificar nullifier = H(secret|commitment)


@dataclass
class TransactionOutput:
    """Output: nuevo commitment de nota creada."""

    commitment: CommitmentHash
    amount: int
    asset_id: str


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
    fee: fee para el minero
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

    outputs: List[TransactionOutput] = []
    for amount, owner in zip(output_amounts, output_owners):
        # Crear nota efímera para commitment; el receptor la reconstruirá
        nonce = secrets.token_hex(16)
        comm = CommitmentHash(
            commitment_for_note(owner, amount, nonce, input_notes[0].asset_id)
        )
        outputs.append(
            TransactionOutput(
                commitment=comm,
                amount=amount,
                asset_id=input_notes[0].asset_id,
            )
        )

    tx_id = tx_id or TxId(secrets.token_hex(16))
    return PrivateTransaction(
        tx_id=tx_id,
        inputs=inputs,
        outputs=outputs,
        fee=fee,
    )


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

    tx_id = tx_id or TxId(secrets.token_hex(16))
    tx = PrivateTransaction(tx_id=tx_id, inputs=inputs, outputs=outputs, fee=fee)
    return tx, output_notes


def validate_transaction_basic(tx: PrivateTransaction) -> tuple[bool, Optional[str]]:
    """
    Valida transacción básica: conservación de valor.
    Retorna (ok, error_message).
    """
    total_in = tx.input_amount()
    total_out = tx.output_amount() + tx.fee
    if total_in != total_out:
        return False, f"Desbalance: in={total_in}, out+fee={total_out}"

    if not tx.inputs:
        return False, "Sin inputs"

    if not tx.outputs:
        return False, "Sin outputs"

    asset = tx.inputs[0].asset_id
    for i in tx.inputs:
        if i.asset_id != asset:
            return False, "Asset mezclado en inputs"
    for o in tx.outputs:
        if o.asset_id != asset:
            return False, "Asset mezclado en outputs"

    return True, None
