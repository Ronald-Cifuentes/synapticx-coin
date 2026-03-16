#!/usr/bin/env python3
"""Genera fixture válido para conformance."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.store import Store


def main():
    out_dir = Path(__file__).resolve().parents[1] / "conformance" / "fixtures" / "valid_chain"
    out_dir.mkdir(parents=True, exist_ok=True)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    store = Store(out_dir)
    store.save_config(config)
    store.save_blocks(chain.blocks)
    print(f"Fixture generado en {out_dir}")
    print(f"  config.json, blocks.json ({len(chain.blocks)} bloque(s))")


if __name__ == "__main__":
    main()
