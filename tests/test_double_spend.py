"""Tests para doble gasto."""

import pytest

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.mempool import Mempool
from coinlab.notes import create_note
from coinlab.transactions import create_transfer_with_output_notes


def test_double_spend_same_nullifier_fails():
    """Doble gasto con mismo nullifier falla en mempool."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx1, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    mempool = Mempool()
    ok, _ = mempool.add_transaction(tx1)
    assert ok
    tx2, _ = create_transfer_with_output_notes(
        [out_notes[0]], [50], ["miner"], fee=0
    )
    tx3, _ = create_transfer_with_output_notes(
        [out_notes[0]], [50], ["eve"], fee=0
    )
    ok2, _ = mempool.add_transaction(tx2)
    assert ok2
    ok3, err3 = mempool.add_transaction(tx3)
    assert not ok3
    assert "Nullifier" in err3 or "competidora" in err3 or "competid" in err3.lower()
