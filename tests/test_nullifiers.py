"""Tests para nullifiers."""

import pytest

from coinlab.notes import create_note
from coinlab.nullifiers import add_nullifier, is_nullifier_used, nullifier_set


def test_nullifier_stable():
    """Un input genera nullifier estable."""
    n = create_note("alice", 50, "BASE", nonce="n", secret="s")
    nf1 = n.nullifier()
    nf2 = n.nullifier()
    assert nf1 == nf2


def test_nullifier_set():
    nfs = nullifier_set()
    assert not is_nullifier_used(nfs, "abc")
    add_nullifier(nfs, "abc")
    assert is_nullifier_used(nfs, "abc")
