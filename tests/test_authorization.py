"""
Tests de autorización real: commitment ajeno no gastable con secret arbitrario.
"""

import pytest

from coinlab.blocks import compute_merkle_root
from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.crypto_primitives import hash_hex, nullifier_for_note, owner_secret_hash
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block
from coinlab.notes import create_note
from coinlab.pow import mine_block
from coinlab.transactions import (
    PrivateTransaction,
    TransactionInput,
    TransactionOutput,
    create_transfer_with_output_notes,
)
from coinlab.types import CommitmentHash, TxId


def test_existing_commitment_cannot_be_spent_with_attacker_secret():
    """Exploit: commitment real + secret arbitrario + nullifier coherente. Rechazado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    rec = chain.state.notes[str(faucet_note.commitment())]
    attacker_secret = "attacker_stole"
    attacker_nf = nullifier_for_note(attacker_secret, str(faucet_note.commitment()))
    tx = PrivateTransaction(
        tx_id=TxId("stolen"),
        inputs=[
            TransactionInput(
                commitment=faucet_note.commitment(),
                nullifier=attacker_nf,
                amount=rec.amount,
                asset_id=rec.asset_id,
                secret=attacker_secret,
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out")),
                amount=rec.amount,
                asset_id=rec.asset_id,
                owner_secret_hash=owner_secret_hash(""),
            )
        ],
        fee=0,
    )
    ok, err = chain.state.can_apply_transaction(tx)
    assert not ok
    assert "Secret no autorizado" in err or "autorizado" in err.lower()


def test_existing_commitment_cannot_be_stolen_even_with_real_amount():
    """Exploit: commitment real, amount real del estado, secret falso. Rechazado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    rec = chain.state.notes[str(faucet_note.commitment())]
    tx = PrivateTransaction(
        tx_id=TxId("stolen2"),
        inputs=[
            TransactionInput(
                commitment=faucet_note.commitment(),
                nullifier=nullifier_for_note("wrong_secret", str(faucet_note.commitment())),
                amount=rec.amount,
                asset_id=rec.asset_id,
                secret="wrong_secret",
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out")),
                amount=rec.amount,
                asset_id=rec.asset_id,
                owner_secret_hash=owner_secret_hash(""),
            )
        ],
        fee=0,
    )
    ok, err = chain.state.can_apply_transaction(tx)
    assert not ok


def test_input_amount_is_taken_from_state_not_from_claimed_field():
    """Amount real sale del estado; input.amount es metadata no confiable."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    chain.state.apply_transaction(tx)
    bad_tx = PrivateTransaction(
        tx_id=TxId("bad"),
        inputs=[
            TransactionInput(
                commitment=out_notes[0].commitment(),
                nullifier=out_notes[0].nullifier(),
                amount=999,
                asset_id="BASE",
                secret=out_notes[0].secret,
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
    ok, err = chain.state.can_apply_transaction(bad_tx)
    assert ok
    rec = chain.state.notes[str(out_notes[0].commitment())]
    assert rec.amount == 50


def test_input_asset_is_taken_from_state_not_from_claimed_field():
    """Asset real sale del estado; input.asset_id es metadata no confiable."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    chain.state.apply_transaction(tx)
    legit_tx = PrivateTransaction(
        tx_id=TxId("legit_asset"),
        inputs=[
            TransactionInput(
                commitment=out_notes[0].commitment(),
                nullifier=out_notes[0].nullifier(),
                amount=50,
                asset_id="FAKE",
                secret=out_notes[0].secret,
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
    ok, err = chain.state.can_apply_transaction(legit_tx)
    assert ok
    chain.state.apply_transaction(legit_tx)
    out_comm = str(legit_tx.outputs[0].commitment)
    rec = chain.state.notes[out_comm]
    assert rec.asset_id == "BASE"


def test_validate_chain_rejects_stolen_commitment_spend():
    """validate_chain rechaza cadena con gasto robado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    rec = chain.state.notes[str(faucet_note.commitment())]
    stolen_tx = PrivateTransaction(
        tx_id=TxId("stolen"),
        inputs=[
            TransactionInput(
                commitment=faucet_note.commitment(),
                nullifier=nullifier_for_note("attacker", str(faucet_note.commitment())),
                amount=rec.amount,
                asset_id=rec.asset_id,
                secret="attacker",
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out")),
                amount=rec.amount,
                asset_id=rec.asset_id,
                owner_secret_hash=owner_secret_hash(""),
            )
        ],
        fee=0,
    )
    blk = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([stolen_tx]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[stolen_tx],
        coinbase_commitment=hash_hex("cb"),
        coinbase_amount=config.block_reward,
    )
    blk.coinbase_owner_secret_hash = owner_secret_hash("miner")
    ok, err = chain.add_block(blk)
    assert not ok
    chain.blocks.append(blk)
    ok, err = chain.validate_chain()
    assert not ok


def test_add_block_rejects_stolen_commitment_spend():
    """add_block rechaza bloque con gasto robado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    rec = chain.state.notes[str(faucet_note.commitment())]
    stolen_tx = PrivateTransaction(
        tx_id=TxId("stolen"),
        inputs=[
            TransactionInput(
                commitment=faucet_note.commitment(),
                nullifier=nullifier_for_note("attacker", str(faucet_note.commitment())),
                amount=rec.amount,
                asset_id=rec.asset_id,
                secret="attacker",
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out")),
                amount=rec.amount,
                asset_id=rec.asset_id,
                owner_secret_hash=owner_secret_hash(""),
            )
        ],
        fee=0,
    )
    blk = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([stolen_tx]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[stolen_tx],
        coinbase_commitment=hash_hex("cb"),
        coinbase_amount=config.block_reward,
    )
    blk.coinbase_owner_secret_hash = owner_secret_hash("miner")
    ok, err = chain.add_block(blk)
    assert not ok
    assert "Secret" in err or "autorizado" in err.lower() or "Tx no aplicable" in err


def test_reorg_rejects_chain_with_stolen_commitment_spend():
    """reorg rechaza cadena alternativa con gasto robado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    build_and_mine_block(chain, Mempool(), "miner")
    chain_alt = Blockchain(config)
    block, faucet_note = chain_alt.create_genesis("faucet")
    rec = chain_alt.state.notes[str(faucet_note.commitment())]
    stolen_tx = PrivateTransaction(
        tx_id=TxId("stolen"),
        inputs=[
            TransactionInput(
                commitment=faucet_note.commitment(),
                nullifier=nullifier_for_note("attacker", str(faucet_note.commitment())),
                amount=rec.amount,
                asset_id=rec.asset_id,
                secret="attacker",
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out")),
                amount=rec.amount,
                asset_id=rec.asset_id,
                owner_secret_hash=owner_secret_hash(""),
            )
        ],
        fee=0,
    )
    blk = mine_block(
        prev_hash=chain_alt.tip_hash(),
        merkle_root=compute_merkle_root([stolen_tx]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[stolen_tx],
        coinbase_commitment=hash_hex("cb"),
        coinbase_amount=config.block_reward,
    )
    blk.coinbase_owner_secret_hash = owner_secret_hash("miner")
    chain_alt.blocks.append(blk)
    for _ in range(2):
        build_and_mine_block(chain_alt, Mempool(), "miner")
    ok, err = chain.reorg_to(chain_alt.blocks)
    assert not ok


def test_new_outputs_are_spendable_only_with_legitimate_secret():
    """Outputs nuevos requieren secret legítimo (owner_secret_hash correcto)."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    chain.state.apply_transaction(tx)
    alice_note = out_notes[0]
    ok, _ = chain.state.can_apply_transaction(
        PrivateTransaction(
            tx_id=TxId("legit"),
            inputs=[
                TransactionInput(
                    commitment=alice_note.commitment(),
                    nullifier=alice_note.nullifier(),
                    amount=50,
                    asset_id="BASE",
                    secret=alice_note.secret,
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
    )
    assert ok
    ok2, _ = chain.state.can_apply_transaction(
        PrivateTransaction(
            tx_id=TxId("attack"),
            inputs=[
                TransactionInput(
                    commitment=alice_note.commitment(),
                    nullifier=nullifier_for_note("attacker", str(alice_note.commitment())),
                    amount=50,
                    asset_id="BASE",
                    secret="attacker",
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
    )
    assert not ok2
