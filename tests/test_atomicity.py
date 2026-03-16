"""
Tests de atomicidad: add_block, reorg, mempool seguro.
"""

import pytest

from coinlab.blocks import Block, BlockHeader, compute_merkle_root
from coinlab.chain import Blockchain, validate_block
from coinlab.config import Config
from coinlab.crypto_primitives import hash_hex, owner_secret_hash
from coinlab.mempool import Mempool
from coinlab.notes import create_note
from coinlab.pow import mine_block
from coinlab.transactions import (
    PrivateTransaction,
    TransactionInput,
    TransactionOutput,
    create_transfer_with_output_notes,
    tx_id_from_payload,
)
from coinlab.types import CommitmentHash, TxId


def test_add_block_is_atomic_on_failure():
    """Bloque con tx1 válida y tx2 inválida: add_block falla, estado no cambia."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx1, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    from coinlab.miner import build_and_mine_block

    build_and_mine_block(chain, Mempool(), "miner")
    tx2_valid, _ = create_transfer_with_output_notes(
        [out_notes[0]], [50], ["bob"], fee=0
    )
    tx2_invalid = PrivateTransaction(
        tx_id=TxId("bad_tx"),
        inputs=[
            TransactionInput(
                commitment=out_notes[1].commitment(),
                nullifier=out_notes[1].nullifier(),
                amount=50,
                asset_id="BASE",
                secret=out_notes[1].secret,
            )
        ],
            outputs=[
                TransactionOutput(
                    commitment=CommitmentHash(hash_hex("out")),
                    amount=60,
                    asset_id="BASE",
                    owner_secret_hash=owner_secret_hash(""),
                    nonce="x",
                )
            ],
        fee=0,
    )
    blocks_before = len(chain.blocks)
    commitments_before = chain.state.commitments.copy()
    nullifiers_before = chain.state.nullifiers_used.copy()

    cb_note = create_note("miner", config.block_reward, "BASE")
    bad_block = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([tx2_valid, tx2_invalid]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[tx2_valid, tx2_invalid],
        coinbase_commitment=cb_note.commitment(),
        coinbase_amount=config.block_reward,
        coinbase_owner_secret_hash=owner_secret_hash(cb_note.secret),
        coinbase_nonce=cb_note.nonce,
    )
    ok, err = chain.add_block(bad_block)
    assert not ok
    assert len(chain.blocks) == blocks_before
    assert chain.state.commitments == commitments_before
    assert chain.state.nullifiers_used == nullifiers_before


def test_reorg_rejects_unbalanced_transaction_chain():
    """Cadena alternativa con tx desbalanceada: reorg falla, original intacta."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    from coinlab.miner import build_and_mine_block

    for _ in range(2):
        build_and_mine_block(chain, Mempool(), "miner")
    chain_alt = Blockchain(config)
    chain_alt.create_genesis("faucet")
    for _ in range(3):
        build_and_mine_block(chain_alt, Mempool(), "miner")
    unbalanced_tx = PrivateTransaction(
        tx_id=TxId("unbal"),
        inputs=[
            TransactionInput(
                commitment=CommitmentHash(hash_hex("x")),
                nullifier=hash_hex("nf"),
                amount=100,
                asset_id="BASE",
                secret="fake",
            )
        ],
        outputs=[
                TransactionOutput(
                    commitment=CommitmentHash(hash_hex("y")),
                    amount=150,
                    asset_id="BASE",
                    owner_secret_hash=owner_secret_hash(""),
                    nonce="x",
                )
        ],
        fee=0,
    )
    cb_note = create_note("miner", config.block_reward, "BASE")
    bad_block = mine_block(
        prev_hash=chain_alt.tip_hash(),
        merkle_root=compute_merkle_root([unbalanced_tx]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[unbalanced_tx],
        coinbase_commitment=cb_note.commitment(),
        coinbase_amount=config.block_reward,
        coinbase_owner_secret_hash=owner_secret_hash(cb_note.secret),
        coinbase_nonce=cb_note.nonce,
    )
    chain_alt.blocks.append(bad_block)

    blocks_before = list(chain.blocks)
    state_commitments_before = chain.state.commitments.copy()
    state_nullifiers_before = chain.state.nullifiers_used.copy()

    ok, err = chain.reorg_to(chain_alt.blocks)
    assert not ok
    assert chain.blocks == blocks_before
    assert chain.state.commitments == state_commitments_before
    assert chain.state.nullifiers_used == state_nullifiers_before


def test_reorg_is_atomic_on_failure():
    """Cadena alternativa falla a mitad: ni cadena ni estado quedan mutados."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx1, _ = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    from coinlab.miner import build_and_mine_block

    build_and_mine_block(chain, Mempool(), "miner")
    chain_alt = Blockchain(config)
    chain_alt.create_genesis("faucet")
    build_and_mine_block(chain_alt, Mempool(), "miner")
    fake_tx = PrivateTransaction(
        tx_id=TxId("fake"),
        inputs=[
            TransactionInput(
                commitment=CommitmentHash(hash_hex("nonexistent")),
                nullifier=hash_hex("nf"),
                amount=50,
                asset_id="BASE",
                secret="fake",
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("o")),
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash(""),
                nonce="x",
            )
        ],
        fee=0,
    )
    cb_note = create_note("miner", config.block_reward, "BASE")
    bad_block = mine_block(
        prev_hash=chain_alt.tip_hash(),
        merkle_root=compute_merkle_root([fake_tx]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[fake_tx],
        coinbase_commitment=cb_note.commitment(),
        coinbase_amount=config.block_reward,
        coinbase_owner_secret_hash=owner_secret_hash(cb_note.secret),
        coinbase_nonce=cb_note.nonce,
    )
    chain_alt.blocks.append(bad_block)

    blocks_before = list(chain.blocks)
    state_before = chain.state.copy()

    ok, err = chain.reorg_to(chain_alt.blocks)
    assert not ok
    assert len(chain.blocks) == len(blocks_before)
    assert chain.state.commitments == state_before.commitments
    assert chain.state.nullifiers_used == state_before.nullifiers_used


def test_validate_block_rejects_internal_nullifier_conflict():
    """Dos tx del mismo bloque usan el mismo nullifier: validate_block falla."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx1, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    tx2a, _ = create_transfer_with_output_notes(
        [out_notes[0]], [50], ["miner"], fee=0
    )
    tx2b = PrivateTransaction(
        tx_id=TxId("dup"),
        inputs=tx2a.inputs,
        outputs=[
                TransactionOutput(
                    commitment=CommitmentHash(hash_hex("other")),
                    amount=50,
                    asset_id="BASE",
                    owner_secret_hash=owner_secret_hash(""),
                    nonce="x",
                )
        ],
        fee=0,
    )
    cb_note = create_note("miner", config.block_reward, "BASE")
    block_with_conflict = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([tx2a, tx2b]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[tx2a, tx2b],
        coinbase_commitment=cb_note.commitment(),
        coinbase_amount=config.block_reward,
        coinbase_owner_secret_hash=owner_secret_hash(cb_note.secret),
        coinbase_nonce=cb_note.nonce,
    )
    ok, err = validate_block(block_with_conflict, 1, config)
    assert not ok
    assert "Nullifier" in err or "duplicado" in err.lower()


def test_mempool_safe_path_rejects_nonexistent_input_without_optional_magic():
    """Flujo normal add_transaction_validated rechaza input inexistente sin parámetros opcionales."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    out_note = create_note("recipient", 50, "BASE", secret="")
    fake_tx = PrivateTransaction(
        tx_id=TxId(""),
        inputs=[
            TransactionInput(
                commitment=CommitmentHash(hash_hex("inexistente")),
                nullifier=hash_hex("nf"),
                amount=50,
                asset_id="BASE",
                secret="fake",
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=out_note.commitment(),
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash(out_note.secret),
                nonce=out_note.nonce,
            )
        ],
        fee=0,
    )
    fake_tx.tx_id = tx_id_from_payload(fake_tx)
    mempool = Mempool()
    ok, err = mempool.add_transaction_validated(fake_tx, chain.state)
    assert not ok
    assert "inexistente" in err or "Input" in err
