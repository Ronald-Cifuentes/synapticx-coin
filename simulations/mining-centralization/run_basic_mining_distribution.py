#!/usr/bin/env python3
"""
Simulación básica: distribución de minería entre varios mineros.
MVP: simula N mineros con distinta potencia (probabilidad de minar).
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block


def main():
    config = Config(difficulty=2, block_reward=100)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    mempool = Mempool()

    miners = ["miner_a", "miner_b", "miner_c"]
    weights = [0.5, 0.3, 0.2]
    blocks_mined = {m: 0 for m in miners}

    for _ in range(20):
        miner = random.choices(miners, weights=weights)[0]
        build_and_mine_block(chain, mempool, miner)
        blocks_mined[miner] += 1

    print("Distribución de bloques minados:")
    for m in miners:
        pct = 100 * blocks_mined[m] / 20
        print(f"  {m}: {blocks_mined[m]} ({pct:.0f}%)")
    print(f"Total bloques: {len(chain.blocks)}")


if __name__ == "__main__":
    main()
