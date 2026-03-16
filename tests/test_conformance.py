"""
Tests de conformance: fixture válido e invalid-cases.
"""

import json
import pytest
from pathlib import Path

from coinlab.blocks import compute_merkle_root
from coinlab.chain import Blockchain, validate_block
from coinlab.config import Config
from coinlab.crypto_primitives import hash_hex, owner_secret_hash
from coinlab.mempool import Mempool
from coinlab.notes import create_note
from coinlab.pow import mine_block
from coinlab.store import Store, deserialize_tx
from coinlab.transactions import (
    PrivateTransaction,
    TransactionInput,
    TransactionOutput,
    create_transfer_with_output_notes,
)
from coinlab.types import CommitmentHash, TxId


FIXTURE_DIR = Path(__file__).resolve().parents[1] / "conformance" / "fixtures" / "valid_chain"


def test_valid_fixture_loads_and_validates():
    """Fixture válido: carga con config_for_chain (como _load_chain) y validate_chain pasa."""
    if not FIXTURE_DIR.exists():
        pytest.skip("Ejecutar scripts/generate_conformance_fixture.py primero")
    store = Store(FIXTURE_DIR)
    blocks = store.load_blocks()
    assert len(blocks) >= 1
    config = store.config_for_chain(blocks)
    chain = Blockchain(config)
    for block in blocks:
        ok, err = chain.add_block(block)
        assert ok, err
    ok, err = chain.validate_chain()
    assert ok, err


def test_invalid_input_inexistente_rejected():
    """Invalid-case: tx con input commitment inexistente debe rechazarse."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    mempool = Mempool()
    fake_tx = PrivateTransaction(
        tx_id=TxId("fake"),
        inputs=[
            TransactionInput(
                commitment=CommitmentHash(hash_hex("input_inexistente")),
                nullifier=hash_hex("nf_fake"),
                amount=50,
                asset_id="BASE",
                secret="fake",
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out")),
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash(""),
            )
        ],
        fee=0,
    )
    ok, err = mempool.add_transaction_validated(fake_tx, chain.state)
    assert not ok
    assert "inexistente" in err or "Input" in err


def test_invalid_reuse_commitment_rejected():
    """Invalid-case: output que reutiliza commitment existente debe rechazarse."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    chain.state.apply_transaction(tx)
    bob_comm = out_notes[1].commitment()
    hijack_tx = PrivateTransaction(
        tx_id=TxId("hijack"),
        inputs=[
            TransactionInput(
                commitment=out_notes[0].commitment(),
                nullifier=out_notes[0].nullifier(),
                amount=50,
                asset_id="BASE",
                secret=out_notes[0].secret,
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=bob_comm,
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash("attacker"),
            )
        ],
        fee=0,
    )
    ok, err = chain.state.can_apply_transaction(hijack_tx)
    assert not ok
    assert "reutilizado" in err or "Commitment" in err


INVALID_CASES_DIR = Path(__file__).resolve().parents[1] / "conformance" / "invalid-cases"


def test_invalid_case_input_inexistente_from_json():
    """Invalid-case JSON: tx con input inexistente debe rechazarse por mempool."""
    path = INVALID_CASES_DIR / "input_inexistente.json"
    if not path.exists():
        pytest.skip("Ejecutar scripts/generate_invalid_cases.py primero")
    data = json.loads(path.read_text())
    tx = deserialize_tx(data["tx"])
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    mempool = Mempool()
    ok, err = mempool.add_transaction_validated(tx, chain.state)
    assert not ok
    assert "inexistente" in err or "Input" in err


def test_invalid_block_header_difficulty_rejected():
    """Invalid-case: bloque con header.difficulty distinto a policy debe rechazarse."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    block = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=hash_hex(""),
        timestamp=1,
        difficulty=4,
        transactions=[],
        coinbase_commitment=hash_hex("x"),
        coinbase_amount=config.block_reward,
    )
    ok, err = validate_block(block, 1, config)
    assert not ok
    assert "Difficulty" in err or "difficulty" in err.lower()
