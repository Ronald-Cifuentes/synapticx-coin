"""
Tests críticos de validación: inputs existentes, coinbase, merkle, trabajo acumulado.
"""

import pytest

from coinlab.blocks import Block, BlockHeader, compute_merkle_root
from coinlab.chain import Blockchain, validate_block
from coinlab.config import Config
from coinlab.crypto_primitives import hash_hex
from coinlab.mempool import Mempool
from coinlab.notes import create_note
from coinlab.pow import block_work, cumulative_work, mine_block
from coinlab.transactions import (
    PrivateTransaction,
    TransactionInput,
    TransactionOutput,
    create_transfer_with_output_notes,
)
from coinlab.types import CommitmentHash, TxId


def test_tx_with_nonexistent_input_commitment_fails():
    """Tx balanceada con input commitment inexistente debe fallar."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    # Crear tx con input inventado (commitment que no está en el estado)
    fake_commitment = CommitmentHash(hash_hex("fake_input_123"))
    fake_input = TransactionInput(
        commitment=fake_commitment,
        nullifier=hash_hex("fake_nullifier"),
        amount=50,
        asset_id="BASE",
        secret="fake",
    )
    real_output = TransactionOutput(
        commitment=CommitmentHash(hash_hex("real_out")),
        amount=50,
        asset_id="BASE",
    )
    tx = PrivateTransaction(
        tx_id=TxId("fake_tx_1"),
        inputs=[fake_input],
        outputs=[real_output],
        fee=0,
    )
    ok, err = chain.state.can_apply_transaction(tx)
    assert not ok
    assert "inexistente" in err or "Input" in err


def test_block_with_inflated_coinbase_fails():
    """Bloque con coinbase inflada debe fallar."""
    config = Config(difficulty=2, block_reward=100)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    # Bloque válido en PoW pero con coinbase 999
    block = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=hash_hex(""),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[],
        coinbase_commitment=hash_hex("x"),
        coinbase_amount=999,
    )
    ok, err = chain.add_block(block)
    assert not ok
    assert "Coinbase" in err or "999" in err


def test_block_with_wrong_merkle_root_fails():
    """Bloque con merkle_root alterado debe fallar."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    correct_root = compute_merkle_root([tx])
    wrong_root = hash_hex("wrong_merkle")
    block2 = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=wrong_root,
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[tx],
        coinbase_commitment=hash_hex("y"),
        coinbase_amount=config.block_reward,
    )
    ok, err = chain.add_block(block2)
    assert not ok
    assert "Merkle" in err or "merkle" in err.lower()


def test_heavier_chain_wins_over_longer_chain_when_applicable():
    """Cadena con más trabajo gana. Misma policy: más bloques = más trabajo."""
    config = Config(difficulty=2)
    chain_short = Blockchain(config)
    chain_short.create_genesis("faucet")
    from coinlab.mempool import Mempool
    from coinlab.miner import build_and_mine_block

    for _ in range(2):
        build_and_mine_block(chain_short, Mempool(), "miner")
    work_short = cumulative_work(chain_short.blocks, config)

    chain_heavy = Blockchain(config)
    chain_heavy.create_genesis("faucet")
    for _ in range(3):
        build_and_mine_block(chain_heavy, Mempool(), "miner")
    work_heavy = cumulative_work(chain_heavy.blocks, config)

    assert work_heavy > work_short
    ok, err = chain_short.reorg_to(chain_heavy.blocks)
    assert ok, err
    assert len(chain_short.blocks) == 4
    assert cumulative_work(chain_short.blocks, config) == work_heavy


def test_validate_chain_rejects_hidden_monetary_invalidity():
    """Cadena con tx balanceada pero input inexistente NO debe validar."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    fake_input = TransactionInput(
        commitment=CommitmentHash(hash_hex("nonexistent")),
        nullifier=hash_hex("nf1"),
        amount=50,
        asset_id="BASE",
        secret="fake",
    )
    fake_tx = PrivateTransaction(
        tx_id=TxId("fake"),
        inputs=[fake_input],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out1")),
                amount=50,
                asset_id="BASE",
            )
        ],
        fee=0,
    )
    bad_block = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([fake_tx]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[fake_tx],
        coinbase_commitment=hash_hex("cb"),
        coinbase_amount=config.block_reward,
    )
    ok, _ = chain.add_block(bad_block)
    assert not ok
    chain.blocks.append(bad_block)
    ok, err = chain.validate_chain()
    assert not ok


def test_mempool_rejects_nonexistent_input_tx():
    """Mempool no debe aceptar tx con input inexistente."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    fake_input = TransactionInput(
        commitment=CommitmentHash(hash_hex("fake")),
        nullifier=hash_hex("nf"),
        amount=50,
        asset_id="BASE",
        secret="fake",
    )
    tx = PrivateTransaction(
        tx_id=TxId("fake_tx"),
        inputs=[fake_input],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("o")),
                amount=50,
                asset_id="BASE",
            )
        ],
        fee=0,
    )
    mempool = Mempool()
    ok, err = mempool.add_transaction_validated(tx, chain.state)
    assert not ok
    assert "inexistente" in err or "Input" in err


def test_coinbase_total_matches_policy_over_chain():
    """Suma de rewards debe corresponder con política."""
    config = Config(difficulty=2, block_reward=100)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    from coinlab.mempool import Mempool
    from coinlab.miner import build_and_mine_block

    for _ in range(5):
        build_and_mine_block(chain, Mempool(), "miner")
    total = sum(b.coinbase_amount for b in chain.blocks)
    expected = len(chain.blocks) * config.block_reward
    assert total == expected


def test_merkle_root_is_recomputed_during_validation():
    """Merkle root debe recomputarse en validación, no confiar en header."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx, _ = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["a", "b"], fee=0
    )
    real_root = compute_merkle_root([tx])
    block2 = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=real_root,
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[tx],
        coinbase_commitment=hash_hex("x"),
        coinbase_amount=config.block_reward,
    )
    ok, err = validate_block(block2, 1, config)
    assert ok
    assert block2.header.merkle_root == real_root
    block2.header.merkle_root = hash_hex("tampered")
    ok, err = validate_block(block2, 1, config)
    assert not ok
