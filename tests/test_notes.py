"""Tests para notas y commitments."""

import pytest

from coinlab.notes import (
    Note,
    NoteCommitment,
    create_note,
    note_commitment,
    serialize_note,
    deserialize_note,
)
from coinlab.types import NoteId


def test_create_note():
    n = create_note("alice", 100, "BASE")
    assert n.owner_key == "alice"
    assert n.amount == 100
    assert n.asset_id == "BASE"
    assert n.nonce
    assert n.secret


def test_note_commitment_stable():
    """Una nota genera commitment estable (determinístico con mismos params)."""
    n = create_note("alice", 50, "BASE", nonce="abc", secret="xyz")
    c1 = n.commitment()
    c2 = n.commitment()
    assert c1 == c2


def test_note_commitment_different_for_different_params():
    n1 = create_note("alice", 50, "BASE", nonce="a", secret="x")
    n2 = create_note("bob", 50, "BASE", nonce="a", secret="x")
    assert n1.commitment() != n2.commitment()


def test_note_commitment_helper():
    n = create_note("alice", 100, "BASE")
    nc = note_commitment(n)
    assert nc.commitment_hash == n.commitment()
    assert nc.amount == 100
    assert nc.asset_id == "BASE"


def test_serialize_deserialize():
    n = create_note("alice", 100, "BASE")
    s = serialize_note(n)
    n2 = deserialize_note(s)
    assert n2.owner_key == n.owner_key
    assert n2.amount == n.amount
    assert n2.commitment() == n.commitment()
