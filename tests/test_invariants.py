"""
Tests de invariantes de seguridad.
Comportamiento real: autorización contra estado, amount/asset resueltos desde estado,
unicidad de commitments, difficulty policy.
"""

import pytest

from coinlab.blocks import compute_merkle_root, expected_block_difficulty
from coinlab.chain import Blockchain, validate_block
from coinlab.config import Config
from coinlab.crypto_primitives import hash_hex, owner_secret_hash
from coinlab.notes import create_note
from coinlab.pow import block_work, cumulative_work, mine_block
from coinlab.transactions import (
    PrivateTransaction,
    TransactionInput,
    TransactionOutput,
    create_transfer_with_output_notes,
)
from coinlab.types import CommitmentHash, TxId


def test_forged_input_amount_on_existing_commitment_fails():
    """Input amount declarado no gobierna; conservation usa amount del estado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    real_comm = faucet_note.commitment()
    real_nf = faucet_note.nullifier()
    forged_input = TransactionInput(
        commitment=CommitmentHash(real_comm),
        nullifier=real_nf,
        amount=1000,
        asset_id="BASE",
        secret=faucet_note.secret,
    )
    tx = PrivateTransaction(
        tx_id=TxId("forged_amt"),
        inputs=[forged_input],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out")),
                amount=1000,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash(""),
            )
        ],
        fee=0,
    )
    ok, err = chain.state.can_apply_transaction(tx)
    assert not ok
    assert "Desbalance" in err or "desde estado" in err.lower()


def test_forged_nullifier_for_existing_commitment_fails():
    """Nullifier debe derivar de witness; secret inválido rechazado por autorización."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    real_comm = faucet_note.commitment()
    forged_nf = hash_hex("nullifier_fake")
    forged_input = TransactionInput(
        commitment=CommitmentHash(real_comm),
        nullifier=forged_nf,
        amount=100,
        asset_id="BASE",
        secret="wrong_secret",
    )
    tx = PrivateTransaction(
        tx_id=TxId("forged_nf"),
        inputs=[forged_input],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out")),
                amount=100,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash(""),
            )
        ],
        fee=0,
    )
    ok, err = chain.state.can_apply_transaction(tx)
    assert not ok
    assert "Nullifier" in err or "deriva" in err.lower() or "Secret no autorizado" in err


def test_spend_requires_valid_note_witness():
    """Gasto requiere secret que coincida con owner_secret_hash en estado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    block = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([tx]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[tx],
        coinbase_commitment=hash_hex("cb"),
        coinbase_amount=config.block_reward,
        coinbase_owner_secret_hash=owner_secret_hash("miner_secret"),
    )
    chain.add_block(block, coinbase_owner="miner")
    alice_note = out_notes[0]
    tx_attack = PrivateTransaction(
        tx_id=TxId("attack"),
        inputs=[
            TransactionInput(
                commitment=alice_note.commitment(),
                nullifier=hash_hex("wrong_nf"),
                amount=50,
                asset_id="BASE",
                secret="wrong_secret",
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("eve_out")),
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash(""),
            )
        ],
        fee=0,
    )
    ok, err = chain.state.can_apply_transaction(tx_attack)
    assert not ok


def test_validate_chain_rejects_forged_commitment_spend():
    """Cadena con input inexistente: validate_chain rechaza."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    forged_tx = PrivateTransaction(
        tx_id=TxId("forged"),
        inputs=[
            TransactionInput(
                commitment=CommitmentHash(hash_hex("fake")),
                nullifier=hash_hex("nf"),
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
    block = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([forged_tx]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[forged_tx],
        coinbase_commitment=hash_hex("cb"),
        coinbase_amount=config.block_reward,
    )
    ok, err = chain.add_block(block)
    assert not ok
    chain.blocks.append(block)
    ok, err = chain.validate_chain()
    assert not ok


def test_block_with_forged_header_difficulty_fails():
    """Bloque con header.difficulty distinto a policy: rechazado."""
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


def test_block_work_does_not_trust_free_header_difficulty():
    """block_work usa difficulty de policy, no del header."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    block = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=hash_hex(""),
        timestamp=1,
        difficulty=2,
        transactions=[],
        coinbase_commitment=hash_hex("x"),
        coinbase_amount=config.block_reward,
    )
    block.header.difficulty = 8
    work = block_work(block, expected_block_difficulty(1, config))
    assert work == 16 ** 2
    assert work != 16 ** 8


def test_reorg_rejects_fake_heavier_chain_with_invalid_difficulty():
    """Cadena con bloque de difficulty incoherente con policy: reorg rechaza."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    from coinlab.mempool import Mempool
    from coinlab.miner import build_and_mine_block

    build_and_mine_block(chain, Mempool(), "miner")
    chain_alt = Blockchain(config)
    chain_alt.create_genesis("faucet")
    build_and_mine_block(chain_alt, Mempool(), "miner")
    block_bad = mine_block(
        prev_hash=chain_alt.tip_hash(),
        merkle_root=hash_hex(""),
        timestamp=2,
        difficulty=4,
        transactions=[],
        coinbase_commitment=hash_hex("y"),
        coinbase_amount=config.block_reward,
    )
    chain_alt.blocks.append(block_bad)
    ok, err = chain.reorg_to(chain_alt.blocks)
    assert not ok
    assert "Difficulty" in err or "difficulty" in err.lower() or "policy" in err.lower()


def test_conservation_uses_validated_input_amounts_not_claimed_amounts():
    """Conservation usa amount resuelto desde estado; input.amount no es fuente de verdad."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    ok, _ = chain.state.can_apply_transaction(tx)
    assert ok
    chain.state.apply_transaction(tx)
    bad_tx = PrivateTransaction(
        tx_id=TxId("bad"),
        inputs=[
            TransactionInput(
                commitment=out_notes[0].commitment(),
                nullifier=out_notes[0].nullifier(),
                amount=200,
                asset_id="BASE",
                secret=out_notes[0].secret,
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out")),
                amount=200,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash(""),
            )
        ],
        fee=0,
    )
    ok, err = chain.state.can_apply_transaction(bad_tx)
    assert not ok
    assert "Desbalance" in err or "desde estado" in err.lower()
