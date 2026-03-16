"""
Miner: construye bloque candidato, incluye coinbase, mina PoW.
"""

import time
from typing import List, Optional

from .blocks import Block, compute_merkle_root
from .chain import Blockchain
from .config import Config
from .crypto_primitives import commitment_for_note, hash_hex
from .mempool import Mempool
from .pow import mine_block
from .transactions import PrivateTransaction


def build_and_mine_block(
    chain: Blockchain,
    mempool: Mempool,
    miner_address: str,
    txs: Optional[List[PrivateTransaction]] = None,
    config: Optional[Config] = None,
) -> Block:
    """
    Construye bloque con txs del mempool (o las dadas), coinbase, y mina.
    """
    cfg = config or chain.config
    if txs is None:
        txs = mempool.select_for_block()

    # Coinbase
    nonce = hash_hex(str(time.time_ns()))
    coinbase_commitment = commitment_for_note(
        miner_address, cfg.block_reward, nonce, cfg.default_asset_id
    )

    merkle_root = compute_merkle_root(txs)

    block = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=merkle_root,
        timestamp=int(time.time()),
        difficulty=cfg.difficulty,
        transactions=txs,
        coinbase_commitment=coinbase_commitment,
        coinbase_amount=cfg.block_reward,
    )

    ok, err = chain.add_block(block, coinbase_owner=miner_address)
    if not ok:
        raise RuntimeError(f"Block rechazado: {err}")

    for tx in txs:
        mempool.remove_transaction(tx.tx_id)

    return block
