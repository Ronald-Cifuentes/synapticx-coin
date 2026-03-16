"""Tests para reorg corto."""

import pytest

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block
from coinlab.notes import create_note
from coinlab.transactions import create_transfer_with_output_notes


def test_short_reorg_to_heavier_chain():
    """Reorg corto a cadena más pesada funciona."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    mempool = Mempool()
    build_and_mine_block(chain, mempool, "miner")
    len_before = len(chain.blocks)
    build_and_mine_block(chain, mempool, "miner")
    len_after = len(chain.blocks)
    assert len_after == 3
    chain_alt = Blockchain(config)
    chain_alt.create_genesis("faucet")
    mp2 = Mempool()
    for _ in range(3):
        build_and_mine_block(chain_alt, mp2, "miner")
    assert len(chain_alt.blocks) == 4
    ok, err = chain.reorg_to(chain_alt.blocks)
    assert ok, err
    assert len(chain.blocks) == 4
