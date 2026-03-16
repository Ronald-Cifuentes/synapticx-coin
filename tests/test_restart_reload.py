"""
Tests de restart y recarga: persistencia, validate_chain tras reinicio.
"""

import pytest
from pathlib import Path

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block
from coinlab.store import Store
from coinlab.transactions import create_transfer_with_output_notes


def test_restart_preserves_config_and_chain(tmp_path: Path):
    """Tras crear cadena y persistir, recarga usa config correcta y validate_chain pasa."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    mempool = Mempool()
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    loaded_config = store.load_config()
    assert loaded_config is not None
    assert loaded_config.difficulty == config.difficulty
    ok, err = store.config_compatible_with_blocks(loaded_config, store.load_blocks())
    assert ok, err
    chain2 = Blockchain(loaded_config)
    for block in store.load_blocks():
        ok, err = chain2.add_block(block)
        assert ok, err
    ok, err = chain2.validate_chain()
    assert ok, err


def test_restart_with_different_default_config_fails_if_incompatible(tmp_path: Path):
    """Si se persiste con difficulty X y se carga con difficulty Y, falla compatibilidad."""
    store = Store(tmp_path)
    config = Config(difficulty=3)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    wrong_config = Config(difficulty=2)
    ok, err = store.config_compatible_with_blocks(wrong_config, store.load_blocks())
    assert not ok
