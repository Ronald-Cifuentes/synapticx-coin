"""
Tests de integridad del bloque: alterar blocks.json invalida hash/validación.
Todos los campos state-relevant están en block_hash(); alterarlos rompe prev_hash chain o PoW.
"""

import json
import pytest
from pathlib import Path

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.store import Store
from coinlab.cli import _load_chain
from coinlab.miner import build_and_mine_block
from coinlab.mempool import Mempool


def test_alter_chain_params_hash_breaks_prev_hash_chain(tmp_path: Path):
    """Alterar genesis.chain_params_hash: prev_hash del bloque 1 ya no coincide."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    build_and_mine_block(chain, Mempool(), "miner")
    build_and_mine_block(chain, Mempool(), "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    blocks_data = json.loads(store.blocks_file.read_text())
    blocks_data[0]["chain_params_hash"] = "f" * 64
    store.blocks_file.write_text(json.dumps(blocks_data, indent=2))
    with pytest.raises(RuntimeError, match="prev_hash|Error cargando|incoherente|Config alterada|hash no coincide"):
        _load_chain(store)


def test_alter_coinbase_commitment_breaks_prev_hash(tmp_path: Path):
    """Alterar genesis.coinbase_commitment: block_hash cambia, prev_hash del siguiente no coincide."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    build_and_mine_block(chain, Mempool(), "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    blocks_data = json.loads(store.blocks_file.read_text())
    blocks_data[0]["coinbase_commitment"] = "a" * 64
    store.blocks_file.write_text(json.dumps(blocks_data, indent=2))
    with pytest.raises(RuntimeError, match="prev_hash|Error cargando"):
        _load_chain(store)


def test_alter_coinbase_amount_breaks_prev_hash(tmp_path: Path):
    """Alterar genesis.coinbase_amount: block_hash cambia."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    build_and_mine_block(chain, Mempool(), "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    blocks_data = json.loads(store.blocks_file.read_text())
    blocks_data[0]["coinbase_amount"] = 999
    store.blocks_file.write_text(json.dumps(blocks_data, indent=2))
    with pytest.raises(RuntimeError, match="prev_hash|Error cargando|incoherente"):
        _load_chain(store)


def test_alter_coinbase_owner_secret_hash_breaks_prev_hash(tmp_path: Path):
    """Alterar genesis.coinbase_owner_secret_hash: block_hash cambia."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    build_and_mine_block(chain, Mempool(), "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    blocks_data = json.loads(store.blocks_file.read_text())
    blocks_data[0]["coinbase_owner_secret_hash"] = "b" * 64
    store.blocks_file.write_text(json.dumps(blocks_data, indent=2))
    with pytest.raises(RuntimeError, match="prev_hash|Error cargando"):
        _load_chain(store)


def test_legitimate_chain_loads_and_validates(tmp_path: Path):
    """Cadena legítima: carga y validate_chain pasa."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    build_and_mine_block(chain, Mempool(), "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    chain2 = _load_chain(store)
    ok, _ = chain2.validate_chain()
    assert ok


def test_restart_reload_legitimate(tmp_path: Path):
    """Restart/reload legítimo sigue funcionando."""
    store = Store(tmp_path)
    config = Config(difficulty=3, block_reward=150)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    build_and_mine_block(chain, Mempool(), "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    chain2 = _load_chain(store)
    assert chain2.config.difficulty == 3
    assert chain2.config.block_reward == 150
    ok, _ = chain2.validate_chain()
    assert ok


def test_legacy_block_format_fails_prev_hash(tmp_path: Path):
    """
    Formato legacy (block_hash sin coinbase): rechazo al cargar.
    Bloques viejos tienen block_hash distinto; prev_hash chain se rompe.
    """
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    build_and_mine_block(chain, Mempool(), "miner")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    blocks_data = json.loads(store.blocks_file.read_text())
    for b in blocks_data:
        b.pop("chain_params_hash", None)
        b.pop("coinbase_owner_secret_hash", None)
    store.blocks_file.write_text(json.dumps(blocks_data, indent=2))
    with pytest.raises(RuntimeError, match="prev_hash|Error cargando|Formato legacy|chain_params|no tiene"):
        _load_chain(store)


def test_block_hash_includes_coinbase_fields():
    """block_hash() incluye coinbase; alterar cualquiera cambia el hash."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    block = chain.blocks[0]
    h1 = block.block_hash()
    block.coinbase_commitment = "x" * 64
    h2 = block.block_hash()
    assert h1 != h2
