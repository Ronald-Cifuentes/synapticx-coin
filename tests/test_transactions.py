"""Tests para transacciones."""

import pytest

from coinlab.notes import create_note
from coinlab.transactions import (
    create_transfer_transaction,
    create_transfer_with_output_notes,
    validate_transaction_basic,
    PrivateTransaction,
)


def test_valid_transaction_conserves_value():
    """Transacción válida conserva valor."""
    n1 = create_note("alice", 100, "BASE", nonce="a", secret="s")
    tx = create_transfer_transaction([n1], [60, 40], ["bob", "alice"], fee=0)
    ok, err = validate_transaction_basic(tx)
    assert ok, err
    assert tx.input_amount() == tx.output_amount() + tx.fee


def test_invalid_transaction_unbalanced_fails():
    """Transacción inválida por desbalance falla."""
    n1 = create_note("alice", 100, "BASE", nonce="a", secret="s")
    with pytest.raises(ValueError, match="Desbalance"):
        create_transfer_transaction([n1], [60, 50], ["bob", "alice"], fee=0)


def test_transfer_with_output_notes():
    """create_transfer_with_output_notes retorna tx y notas de salida."""
    n1 = create_note("alice", 100, "BASE", nonce="a", secret="s")
    tx, out_notes = create_transfer_with_output_notes(
        [n1], [60, 40], ["bob", "alice"], fee=0
    )
    assert len(out_notes) == 2
    assert out_notes[0].amount == 60
    assert out_notes[0].owner_key == "bob"
    assert out_notes[1].amount == 40
    ok, _ = validate_transaction_basic(tx)
    assert ok
