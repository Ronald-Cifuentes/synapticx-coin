"""Tests para conservación de supply."""

import pytest

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block
from coinlab.notes import create_note
from coinlab.transactions import create_transfer_with_output_notes


def test_supply_aggregate_conserved():
    """Supply agregado se conserva salvo recompensa explícita."""
    config = Config(difficulty=2, block_reward=100)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    initial_supply = 100  # genesis coinbase
    tx1, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    mempool = Mempool()
    mempool.add_transaction_validated(tx1, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    supply_after = initial_supply + config.block_reward
    total_commitments = sum(
        sum(o.amount for tx in b.transactions for o in tx.outputs) + b.coinbase_amount
        for b in chain.blocks
    )
    total_inputs = sum(
        i.amount for b in chain.blocks for tx in b.transactions for i in tx.inputs
    )
    total_outputs = sum(
        o.amount for b in chain.blocks for tx in b.transactions for o in tx.outputs
    )
    total_fees = sum(tx.fee for b in chain.blocks for tx in b.transactions)
    total_coinbase = sum(b.coinbase_amount for b in chain.blocks)
    assert total_coinbase == 200
    assert total_inputs + total_coinbase == total_outputs + total_fees + total_coinbase
    assert len(chain.state.commitments) > 0
