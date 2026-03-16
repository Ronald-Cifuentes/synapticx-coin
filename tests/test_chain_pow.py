"""Tests para cadena y PoW."""

import pytest

from coinlab.blocks import Block, BlockHeader
from coinlab.chain import Blockchain, GENESIS_PREV
from coinlab.config import Config
from coinlab.pow import meets_difficulty, validate_block_pow, mine_block


def test_meets_difficulty():
    assert meets_difficulty("00abc", 2)
    assert meets_difficulty("000abc", 3)
    assert not meets_difficulty("0abc", 2)
    assert not meets_difficulty("0abc", 3)


def test_chain_with_valid_block_passes():
    """Cadena con bloque válido pasa validación."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, _ = chain.create_genesis("faucet")
    ok, err = chain.validate_chain()
    assert ok, err


def test_chain_pow_invalid_fails():
    """Bloque con PoW inválido falla."""
    from coinlab.blocks import Block
    from coinlab.crypto_primitives import hash_hex

    config = Config(difficulty=4)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    # Bloque con nonce 0 no cumplirá difficulty 4
    bad_header = BlockHeader(
        prev_hash=chain.tip_hash(),
        merkle_root=hash_hex(""),
        timestamp=1,
        nonce=0,
        difficulty=4,
    )
    bad_block = Block(
        header=bad_header,
        transactions=[],
        coinbase_commitment=hash_hex("x"),
        coinbase_amount=100,
    )
    assert not validate_block_pow(bad_block, 4)


def test_short_reorg():
    """Reorg corto a cadena más pesada funciona."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    tip1 = chain.tip_hash()
    blocks1 = list(chain.blocks)
    # Crear cadena alternativa más larga (mismo genesis, otro bloque)
    from coinlab.miner import build_and_mine_block
    from coinlab.mempool import Mempool

    chain2 = Blockchain(config)
    chain2.create_genesis("faucet")
    mempool = Mempool()
    build_and_mine_block(chain2, mempool, "miner")
    ok, err = chain.reorg_to(chain2.blocks)
    assert ok, err
    assert len(chain.blocks) == len(chain2.blocks)
