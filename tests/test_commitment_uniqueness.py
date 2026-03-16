"""
Tests de unicidad de commitments: no reuse, no overwrite.
"""

import pytest

from coinlab.blocks import compute_merkle_root
from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.crypto_primitives import hash_hex, owner_secret_hash
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


def test_output_cannot_reuse_existing_commitment_with_new_owner_secret_hash():
    """Output con commitment existente y owner_secret_hash distinto: rechazado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx1, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    chain.state.apply_transaction(tx1)
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


def test_add_block_rejects_reused_existing_commitment_output():
    """Bloque con tx que reutiliza commitment existente: add_block falla."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx1, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    chain.state.apply_transaction(tx1)
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
                commitment=out_notes[1].commitment(),
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash("attacker"),
            )
        ],
        fee=0,
    )
    blk = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([hijack_tx]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[hijack_tx],
        coinbase_commitment=hash_hex("cb"),
        coinbase_amount=config.block_reward,
    )
    blk.coinbase_owner_secret_hash = owner_secret_hash("miner")
    ok, err = chain.add_block(blk)
    assert not ok
    assert "reutilizado" in err or "Commitment" in err or "aplicable" in err


def test_validate_chain_rejects_reused_existing_commitment_output():
    """Cadena forzada con reuse: validate_chain falla."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx1, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    blk1 = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([tx1]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[tx1],
        coinbase_commitment=hash_hex("cb1"),
        coinbase_amount=config.block_reward,
    )
    blk1.coinbase_owner_secret_hash = owner_secret_hash("miner")
    ok1, _ = chain.add_block(blk1, coinbase_owner="miner")
    assert ok1
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
                commitment=out_notes[1].commitment(),
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash("attacker"),
            )
        ],
        fee=0,
    )
    blk2 = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([hijack_tx]),
        timestamp=2,
        difficulty=config.difficulty,
        transactions=[hijack_tx],
        coinbase_commitment=hash_hex("cb2"),
        coinbase_amount=config.block_reward,
    )
    blk2.coinbase_owner_secret_hash = owner_secret_hash("miner")
    ok2, _ = chain.add_block(blk2)
    assert not ok2
    chain.blocks.append(blk2)
    ok, err = chain.validate_chain()
    assert not ok


def test_reorg_rejects_chain_with_reused_existing_commitment_output():
    """Cadena alternativa con reuse: reorg falla."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    build_and_mine_block(chain, Mempool(), "miner")
    chain_alt = Blockchain(config)
    block, faucet_note = chain_alt.create_genesis("faucet")
    tx1, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    chain_alt.state.apply_transaction(tx1)
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
                commitment=out_notes[1].commitment(),
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash("attacker"),
            )
        ],
        fee=0,
    )
    blk = mine_block(
        prev_hash=chain_alt.tip_hash(),
        merkle_root=compute_merkle_root([hijack_tx]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[hijack_tx],
        coinbase_commitment=hash_hex("cb"),
        coinbase_amount=config.block_reward,
    )
    blk.coinbase_owner_secret_hash = owner_secret_hash("miner")
    chain_alt.blocks.append(blk)
    for _ in range(2):
        build_and_mine_block(chain_alt, Mempool(), "miner")
    ok, err = chain.reorg_to(chain_alt.blocks)
    assert not ok


def test_coinbase_cannot_reuse_existing_commitment():
    """Coinbase con commitment ya existente: rechazado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx1, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    chain.state.apply_transaction(tx1)
    blk = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([tx1]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[tx1],
        coinbase_commitment=str(out_notes[0].commitment()),
        coinbase_amount=config.block_reward,
    )
    blk.coinbase_owner_secret_hash = owner_secret_hash("miner")
    ok, err = chain.add_block(blk)
    assert not ok
    assert "reutilizado" in err or "Coinbase" in err


def test_transaction_cannot_contain_duplicate_output_commitments():
    """Dos outputs en misma tx con mismo commitment: rechazado."""
    from coinlab.transactions import validate_transaction_basic

    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    comm = hash_hex("dup_out")
    dup_tx = PrivateTransaction(
        tx_id=TxId("dup"),
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
                commitment=CommitmentHash(comm),
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash(""),
            ),
            TransactionOutput(
                commitment=CommitmentHash(comm),
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash(""),
            ),
        ],
        fee=0,
    )
    ok_basic, err_basic = validate_transaction_basic(dup_tx)
    assert not ok_basic
    assert "duplicado" in (err_basic or "")
    ok, err = chain.state.can_apply_transaction(dup_tx)
    assert not ok


def test_block_cannot_contain_duplicate_output_commitments_across_transactions():
    """Dos tx del mismo bloque con mismo commitment en outputs: rechazado."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx1, out1 = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    shared_comm = out1[0].commitment()
    tx2 = PrivateTransaction(
        tx_id=TxId("tx2"),
        inputs=[
            TransactionInput(
                commitment=out1[1].commitment(),
                nullifier=out1[1].nullifier(),
                amount=50,
                asset_id="BASE",
                secret=out1[1].secret,
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=shared_comm,
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash("eve"),
            )
        ],
        fee=0,
    )
    blk = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([tx1, tx2]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[tx1, tx2],
        coinbase_commitment=hash_hex("cb"),
        coinbase_amount=config.block_reward,
    )
    blk.coinbase_owner_secret_hash = owner_secret_hash("miner")
    ok, err = chain.add_block(blk)
    assert not ok
    assert "reutilizado" in err or "duplicado" in err or "aplicable" in err
