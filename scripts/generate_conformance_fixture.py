#!/usr/bin/env python3
"""Genera fixture válido para conformance: 2+ bloques con tx para ejercitar prev_hash chain."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block
from coinlab.store import Store
from coinlab.transactions import create_transfer_with_output_notes


def main():
    out_dir = Path(__file__).resolve().parents[1] / "conformance" / "fixtures" / "valid_chain"
    out_dir.mkdir(parents=True, exist_ok=True)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    mempool = Mempool()
    tx, _ = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "faucet"], fee=0
    )
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    store = Store(out_dir)
    store.save_config(config)
    store.save_blocks(chain.blocks)
    print(f"Fixture generado en {out_dir}")
    print(f"  config.json, blocks.json ({len(chain.blocks)} bloque(s))")


if __name__ == "__main__":
    main()
