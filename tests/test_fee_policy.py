"""
Tests de política de fees: fees quemadas, minero recibe solo block_reward.
"""

import pytest

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block
from coinlab.transactions import create_transfer_with_output_notes


def test_tx_with_fee_validates_and_miner_gets_only_block_reward():
    """Fee se quema; minero recibe solo block_reward, nunca fees."""
    config = Config(difficulty=2, block_reward=100)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, out_notes = create_transfer_with_output_notes(
        [faucet_note], [40, 60], ["alice", "bob"], fee=0
    )
    mempool = Mempool()
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    tx_with_fee, _ = create_transfer_with_output_notes(
        [out_notes[0]], [30], ["bob"], fee=10
    )
    mempool = Mempool()
    ok, err = mempool.add_transaction_validated(tx_with_fee, chain.state)
    assert ok, err
    build_and_mine_block(chain, mempool, "miner")
    total_coinbase = sum(b.coinbase_amount for b in chain.blocks)
    total_fees = sum(tx.fee for b in chain.blocks for tx in b.transactions)
    assert total_fees == 10
    assert total_coinbase == 3 * config.block_reward
    for b in chain.blocks:
        assert b.coinbase_amount == config.block_reward
    ok, _ = chain.validate_chain()
    assert ok


def test_fee_burned_reduces_supply_in_commitments():
    """Fee quemada: supply en commitments = minted - fees."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, out_notes = create_transfer_with_output_notes(
        [faucet_note], [45, 55], ["alice", "bob"], fee=0
    )
    chain.state.apply_transaction(tx)
    tx_fee, _ = create_transfer_with_output_notes(
        [out_notes[0]], [40], ["bob"], fee=5
    )
    ok, err = chain.state.can_apply_transaction(tx_fee)
    assert ok, err
    chain.state.apply_transaction(tx_fee)
    total_in_notes = sum(r.amount for r in chain.state.notes.values())
    assert total_in_notes == 95
