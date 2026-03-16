"""
Tests de persistencia y recarga de config.
"""

import pytest
from pathlib import Path

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.store import Store


def test_config_save_load_roundtrip(tmp_path: Path):
    """Config se persiste y carga correctamente."""
    store = Store(tmp_path)
    config = Config(difficulty=3, block_reward=150)
    store.save_config(config)
    loaded = store.load_config()
    assert loaded is not None
    assert loaded.difficulty == 3
    assert loaded.block_reward == 150


def test_config_compatible_with_blocks_empty(tmp_path: Path):
    """Config vacía es compatible con bloques vacíos."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    ok, err = store.config_compatible_with_blocks(config, [])
    assert ok
    assert err is None


def test_config_incompatible_with_blocks_fails(tmp_path: Path):
    """Config con difficulty distinta a persistida falla."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    store = Store(tmp_path)
    store.save_config(config)
    store.save_blocks(chain.blocks)
    wrong_config = Config(difficulty=4)
    ok, err = store.config_compatible_with_blocks(wrong_config, store.load_blocks())
    assert not ok
    assert "incoherente" in err or "difficulty" in err.lower()


def test_chain_load_uses_persisted_config(tmp_path: Path):
    """Al cargar cadena, se usa config persistida."""
    store = Store(tmp_path)
    config = Config(difficulty=3, block_reward=200)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    loaded_chain = Blockchain(None)
    blocks = store.load_blocks()
    stored_config = store.load_config()
    assert stored_config is not None
    assert stored_config.difficulty == 3
    loaded_chain = Blockchain(stored_config)
    for block in blocks:
        ok, err = loaded_chain.add_block(block)
        assert ok, err
    ok, err = loaded_chain.validate_chain()
    assert ok, err
