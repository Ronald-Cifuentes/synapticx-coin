"""
Tests de integridad tx_id en mempool.

add_transaction_validated debe verificar tx_id == H(payload) antes de aceptar;
mismo contrato que validate_block para rechazar temprano.
"""

import pytest

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block
from coinlab.store import Store
from coinlab.transactions import create_transfer_with_output_notes
from coinlab.types import TxId


def test_mempool_rejects_tx_with_fake_tx_id():
    """Tx con tx_id falso: mempool rechaza; no llega a minado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    tx.tx_id = TxId("a" * 64)  # tx_id falso; payload correcto

    mempool = Mempool()
    ok, err = mempool.add_transaction_validated(tx, chain.state)
    assert not ok
    assert "tx_id" in err.lower() or "payload" in err.lower() or "legacy" in err.lower()


def test_mempool_accepts_valid_tx():
    """Tx válida con tx_id correcto: mempool acepta."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )

    mempool = Mempool()
    ok, err = mempool.add_transaction_validated(tx, chain.state)
    assert ok, err


def test_mining_works_after_mempool_fix(tmp_path):
    """Minado con txs del mempool sigue funcionando."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    mempool = Mempool()
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    assert len(chain.blocks) == 2
    ok, _ = chain.validate_chain()
    assert ok


def test_restart_reload_after_mempool_fix(tmp_path):
    """Restart/reload sigue funcionando."""
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
    chain2 = Blockchain(store.load_config())
    for b in store.load_blocks():
        ok, err = chain2.add_block(b)
        assert ok, err
    ok, _ = chain2.validate_chain()
    assert ok


def test_conformance_fixture_still_valid():
    """Fixture de conformance sigue cargando y validando."""
    from pathlib import Path
    from coinlab.store import Store
    fixture_dir = Path(__file__).resolve().parents[1] / "conformance" / "fixtures" / "valid_chain"
    if not fixture_dir.exists():
        pytest.skip("Ejecutar scripts/generate_conformance_fixture.py primero")
    store = Store(fixture_dir)
    blocks = store.load_blocks()
    config = store.config_for_chain(blocks)
    chain = Blockchain(config)
    for block in blocks:
        ok, err = chain.add_block(block)
        assert ok, err
    ok, err = chain.validate_chain()
    assert ok, err
