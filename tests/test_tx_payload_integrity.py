"""
Tests de integridad del payload de tx: alterar blocks.json invalida merkle/validación.
tx_id = H(payload canónico); alterar payload cambia tx_id, merkle_root, block_hash.
"""

import json
import pytest
from pathlib import Path

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.store import Store
from coinlab.cli import _load_chain
from coinlab.miner import build_and_mine_block
from coinlab.mempool import Mempool
from coinlab.notes import create_note
from coinlab.transactions import create_transfer_with_output_notes, tx_id_from_payload
from coinlab.types import TxId


def test_alter_output_owner_secret_hash_breaks_validation(tmp_path: Path):
    """Alterar output.owner_secret_hash: tx_id cambia, merkle cambia, fallo al cargar."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, out_notes = create_transfer_with_output_notes([faucet_note], [50, 50], ["alice", "bob"], fee=0)
    mempool = Mempool()
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)

    blocks_data = json.loads(store.blocks_file.read_text())
    tx0 = blocks_data[1]["transactions"][0]
    tx0["outputs"][0]["owner_secret_hash"] = "f" * 64
    store.blocks_file.write_text(json.dumps(blocks_data, indent=2))

    with pytest.raises(RuntimeError, match="merkle|payload|tx_id|Error cargando"):
        _load_chain(store)


def test_alter_output_amount_breaks_validation(tmp_path: Path):
    """Alterar output.amount: tx_id cambia, merkle cambia."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes([faucet_note], [50, 50], ["alice", "bob"], fee=0)
    mempool = Mempool()
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)

    blocks_data = json.loads(store.blocks_file.read_text())
    tx0 = blocks_data[1]["transactions"][0]
    tx0["outputs"][0]["amount"] = 80
    tx0["outputs"][1]["amount"] = 20
    store.blocks_file.write_text(json.dumps(blocks_data, indent=2))

    with pytest.raises(RuntimeError, match="merkle|payload|tx_id|Error cargando"):
        _load_chain(store)


def test_alter_fee_breaks_validation(tmp_path: Path):
    """Alterar fee: tx_id cambia, merkle cambia."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes([faucet_note], [45, 45], ["alice", "bob"], fee=10)
    mempool = Mempool()
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)

    blocks_data = json.loads(store.blocks_file.read_text())
    tx0 = blocks_data[1]["transactions"][0]
    tx0["fee"] = 5
    tx0["outputs"][0]["amount"] = 48
    tx0["outputs"][1]["amount"] = 47
    store.blocks_file.write_text(json.dumps(blocks_data, indent=2))

    with pytest.raises(RuntimeError, match="merkle|payload|tx_id|Error cargando"):
        _load_chain(store)


def test_alter_input_nullifier_breaks_validation(tmp_path: Path):
    """Alterar input.nullifier: tx_id cambia, merkle cambia."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes([faucet_note], [50, 50], ["alice", "bob"], fee=0)
    mempool = Mempool()
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)

    blocks_data = json.loads(store.blocks_file.read_text())
    tx0 = blocks_data[1]["transactions"][0]
    tx0["inputs"][0]["nullifier"] = "a" * 64
    store.blocks_file.write_text(json.dumps(blocks_data, indent=2))

    with pytest.raises(RuntimeError, match="merkle|payload|tx_id|Error cargando"):
        _load_chain(store)


def test_legitimate_chain_loads_and_validates(tmp_path: Path):
    """Cadena legítima con txs: carga y validate_chain pasa."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes([faucet_note], [50, 50], ["alice", "bob"], fee=0)
    mempool = Mempool()
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)

    chain2 = _load_chain(store)
    ok, _ = chain2.validate_chain()
    assert ok


def test_legacy_tx_id_random_fails_validation(tmp_path: Path):
    """
    Formato legacy: tx con tx_id aleatorio (no derivado de payload) falla verify_tx_id.
    """
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes([faucet_note], [50, 50], ["alice", "bob"], fee=0)
    mempool = Mempool()
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)

    blocks_data = json.loads(store.blocks_file.read_text())
    tx0 = blocks_data[1]["transactions"][0]
    tx0["tx_id"] = "a" * 64
    store.blocks_file.write_text(json.dumps(blocks_data, indent=2))

    with pytest.raises(RuntimeError, match="payload|tx_id|legacy|Merkle|Error cargando"):
        _load_chain(store)


def test_tx_id_derives_from_payload():
    """tx_id = H(payload); mismo payload -> mismo tx_id."""
    from coinlab.transactions import PrivateTransaction, TransactionInput, TransactionOutput
    from coinlab.types import CommitmentHash, TxId

    tx = PrivateTransaction(
        tx_id=TxId(""),
        inputs=[
            TransactionInput(
                commitment=CommitmentHash("c1"),
                nullifier="n1",
                amount=100,
                asset_id="BASE",
                secret="s1",
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash("o1"),
                amount=50,
                asset_id="BASE",
                owner_secret_hash="h1",
            ),
            TransactionOutput(
                commitment=CommitmentHash("o2"),
                amount=50,
                asset_id="BASE",
                owner_secret_hash="h2",
            ),
        ],
        fee=0,
    )
    tid = tx_id_from_payload(tx)
    assert len(tid) == 64
    assert tid == tx_id_from_payload(tx)
    tx.outputs[0].amount = 51
    assert tx_id_from_payload(tx) != tid
