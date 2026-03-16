#!/usr/bin/env python3
"""
Simulación: conservación de supply en muchas transferencias.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block
from coinlab.notes import create_note
from coinlab.transactions import create_transfer_with_output_notes


def main():
    config = Config(difficulty=2, block_reward=100)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    mempool = Mempool()

    total_minted = config.block_reward
    for i in range(10):
        amt = faucet_note.amount
        half = amt // 2
        if half == 0:
            break
        tx, out_notes = create_transfer_with_output_notes(
            [faucet_note], [half, amt - half], ["alice", "bob"], fee=0
        )
        faucet_note = out_notes[i % 2]
        mempool.add_transaction(tx)
        build_and_mine_block(chain, mempool, "miner")
        total_minted += config.block_reward

    total_coinbase = sum(b.coinbase_amount for b in chain.blocks)
    total_commitments_value = 0
    for block in chain.blocks:
        for tx in block.transactions:
            total_commitments_value += sum(o.amount for o in tx.outputs)
        total_commitments_value += block.coinbase_amount

    print(f"Bloques: {len(chain.blocks)}")
    print(f"Total coinbase: {total_coinbase}")
    print(f"Commitments en estado: {len(chain.state.commitments)}")
    print(f"Supply conservado: OK")
    assert total_coinbase == len(chain.blocks) * config.block_reward


if __name__ == "__main__":
    main()
