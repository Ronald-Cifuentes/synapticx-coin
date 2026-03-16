"""
Tests de semántica de commitment de output.

Output commitment debe derivar de metadata: commitment = H(owner_secret_hash|amount|asset_id|nonce).
"""

import json
import pytest
from pathlib import Path

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.crypto_primitives import commitment_for_output, hash_hex, nullifier_for_note, owner_secret_hash
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block
from coinlab.notes import create_note
from coinlab.store import Store
from coinlab.transactions import (
    PrivateTransaction,
    TransactionInput,
    TransactionOutput,
    create_transfer_with_output_notes,
    tx_id_from_payload,
    validate_transaction_basic,
)
from coinlab.types import CommitmentHash, TxId


def test_arbitrary_output_commitment_rejected():
    """
    Output con commitment arbitrario (no derivado de metadata) es rechazado.
    Antes del fix: mempool aceptaba, se minaba, output gastable.
    Después del fix: validate_transaction_basic rechaza por commitment no verificable.
    """
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")

    # Atacante elige secret; owner_secret_hash lo hace dueño del output
    attacker_secret = "attacker_owns_arbitrary_output"
    attacker_osh = owner_secret_hash(attacker_secret)

    # Output con commitment ARBITRARIO; nonce vacío o no coherente
    arbitrary_commitment = hash_hex("arbitrary_commitment_not_from_note")
    fake_output = TransactionOutput(
        commitment=CommitmentHash(arbitrary_commitment),
        amount=100,
        asset_id="BASE",
        owner_secret_hash=attacker_osh,
        nonce="",  # Sin nonce válido: commitment no verificable
    )

    valid_input = TransactionInput(
        commitment=faucet_note.commitment(),
        nullifier=faucet_note.nullifier(),
        amount=100,
        asset_id="BASE",
        secret=faucet_note.secret,
    )

    tx = PrivateTransaction(
        tx_id=TxId(""),
        inputs=[valid_input],
        outputs=[fake_output],
        fee=0,
    )
    tx.tx_id = tx_id_from_payload(tx)

    # Mempool rechaza: output sin nonce válido
    mempool = Mempool()
    ok, err = mempool.add_transaction_validated(tx, chain.state)
    assert not ok, f"Mempool debe rechazar tx con commitment arbitrario; err={err}"
    assert "nonce" in err.lower() or "commitment" in err.lower()


def test_output_commitment_mismatch_rejected():
    """Output con commitment que no coincide con H(owner_secret_hash|amount|asset_id|nonce): rechazado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    out_note = create_note("recipient", 50, "BASE", secret="")
    wrong_comm = hash_hex("wrong_commitment")
    tx = PrivateTransaction(
        tx_id=TxId(""),
        inputs=[
            TransactionInput(
                commitment=faucet_note.commitment(),
                nullifier=faucet_note.nullifier(),
                amount=100,
                asset_id="BASE",
                secret=faucet_note.secret,
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(wrong_comm),
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash(out_note.secret),
                nonce=out_note.nonce,
            )
        ],
        fee=0,
    )
    tx.tx_id = tx_id_from_payload(tx)
    ok, err = validate_transaction_basic(tx)
    assert not ok
    assert "commitment" in err.lower() or "deriva" in err.lower()


def test_legitimate_tx_still_passes():
    """Tx legítima con outputs verificables sigue pasando."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    ok, err = validate_transaction_basic(tx)
    assert ok, err
    ok, err = chain.state.can_apply_transaction(tx)
    assert ok, err
    mempool = Mempool()
    ok, err = mempool.add_transaction_validated(tx, chain.state)
    assert ok, err


def test_legitimate_block_still_passes():
    """Bloque legítimo con tx válidas sigue pasando."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes([faucet_note], [50, 50], ["alice", "bob"], fee=0)
    mempool = Mempool()
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    ok, err = chain.validate_chain()
    assert ok, err


def test_restart_reload_preserves_commitment_semantics(tmp_path: Path):
    """Restart/reload: cadena con outputs verificables persiste y validate_chain pasa."""
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
    chain2 = Blockchain(store.load_config())
    for b in store.load_blocks():
        ok, err = chain2.add_block(b)
        assert ok, err
    ok, err = chain2.validate_chain()
    assert ok, err


def test_legacy_blocks_without_coinbase_nonce_fail_explicitly(tmp_path: Path):
    """Formato legado: blocks sin coinbase_nonce fallan en validate_block con error explícito."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    blocks_data = json.loads(store.blocks_file.read_text())
    del blocks_data[0]["coinbase_nonce"]
    store.blocks_file.write_text(json.dumps(blocks_data, indent=2))
    blocks = store.load_blocks()
    chain2 = Blockchain(config)
    ok, err = chain2.add_block(blocks[0])
    assert not ok
    assert "nonce" in err.lower() or "commitment" in err.lower() or "legado" in err.lower()
