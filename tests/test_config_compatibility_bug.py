"""
Tests que DEMUESTRAN el bug de compatibilidad config/estado y verifican la corrección.
"""

import pytest
from pathlib import Path

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.store import Store


def test_bug_default_asset_id_mismatch_corrupts_state_BEFORE_FIX(tmp_path: Path):
    """
    BUG (antes de corrección): Recargar con default_asset_id distinto reconstruye
    coinbase con asset incorrecto. validate_chain pasa; estado corrupto.
    """
    store = Store(tmp_path)
    config_orig = Config(difficulty=2, block_reward=100, default_asset_id="BASE")
    chain = Blockchain(config_orig)
    chain.create_genesis("faucet")
    store.save_config(config_orig)
    store.save_blocks(chain.blocks)
    genesis_comm = str(chain.blocks[0].coinbase_commitment)
    assert chain.state.notes[genesis_comm].asset_id == "BASE"

    config_wrong = Config(difficulty=2, block_reward=100, default_asset_id="FAKE")
    store.save_config(config_wrong)
    chain2 = Blockchain(config_wrong)
    for block in store.load_blocks():
        ok, err = chain2.add_block(block)
        assert ok, err
    asset_after = chain2.state.notes[genesis_comm].asset_id
    assert asset_after == "FAKE"
    assert asset_after != "BASE"


def test_FIX_reject_config_override_with_different_default_asset_id(tmp_path: Path):
    """Tras corrección: _load_chain con config distinta a persistida debe fallar."""
    store = Store(tmp_path)
    config_orig = Config(difficulty=2, block_reward=100, default_asset_id="BASE")
    chain = Blockchain(config_orig)
    chain.create_genesis("faucet")
    store.save_config(config_orig)
    store.save_blocks(chain.blocks)

    from coinlab.cli import _load_chain
    config_wrong = Config(difficulty=2, block_reward=100, default_asset_id="FAKE")
    with pytest.raises(RuntimeError, match="Config pasada difiere|Config incoherente"):
        _load_chain(store, config=config_wrong)


def test_FIX_config_compatible_rejects_block_reward_mismatch(tmp_path: Path):
    """config_compatible rechaza block_reward distinto al persistido."""
    store = Store(tmp_path)
    config_orig = Config(difficulty=2, block_reward=100)
    chain = Blockchain(config_orig)
    chain.create_genesis("faucet")
    store.save_config(config_orig)
    store.save_blocks(chain.blocks)
    config_wrong = Config(difficulty=2, block_reward=999)
    ok, err = store.config_compatible_with_blocks(config_wrong, store.load_blocks())
    assert not ok
    assert "block_reward" in err.lower()


def test_FIX_config_compatible_rejects_default_asset_id_mismatch(tmp_path: Path):
    """config_compatible rechaza default_asset_id distinto al persistido."""
    store = Store(tmp_path)
    config_orig = Config(difficulty=2, default_asset_id="BASE")
    chain = Blockchain(config_orig)
    chain.create_genesis("faucet")
    store.save_config(config_orig)
    store.save_blocks(chain.blocks)
    config_wrong = Config(difficulty=2, default_asset_id="FAKE")
    ok, err = store.config_compatible_with_blocks(config_wrong, store.load_blocks())
    assert not ok
    assert "default_asset_id" in err.lower() or "asset" in err.lower()


def test_FIX_reload_with_identical_config_succeeds(tmp_path: Path):
    """Recarga con config idéntica a persistida: éxito."""
    store = Store(tmp_path)
    config = Config(difficulty=3, block_reward=150, default_asset_id="BASE")
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    from coinlab.cli import _load_chain
    chain2 = _load_chain(store)
    assert chain2.config.difficulty == 3
    assert chain2.config.block_reward == 150
    ok, _ = chain2.validate_chain()
    assert ok


def test_FIX_blocks_without_config_fails(tmp_path: Path):
    """Bloques sin config persistida: fallo explícito."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    store.save_blocks(chain.blocks)
    if store.config_file.exists():
        store.config_file.unlink()
    from coinlab.cli import _load_chain
    with pytest.raises(RuntimeError, match="Config no persistida"):
        _load_chain(store)
