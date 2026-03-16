"""
Tests de integridad constitucional: config.json alterada no puede reconstruir estado.
Fuente de verdad: genesis.chain_params_hash anclado en ledger.
"""

import json
import pytest
from pathlib import Path

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.store import Store
from coinlab.cli import _load_chain


def test_manipulation_config_json_fails_explicitly(tmp_path: Path):
    """
    Alterar config.json manualmente: _load_chain falla con RuntimeError explícito.
    No corrupción silenciosa.
    """
    store = Store(tmp_path)
    config_orig = Config(difficulty=2, block_reward=100, default_asset_id="BASE")
    chain = Blockchain(config_orig)
    chain.create_genesis("faucet")
    store.save_config(config_orig)
    store.save_blocks(chain.blocks)
    genesis_comm = str(chain.blocks[0].coinbase_commitment)
    assert chain.state.notes[genesis_comm].asset_id == "BASE"

    data = json.loads(store.config_file.read_text())
    data["default_asset_id"] = "FAKE"
    store.config_file.write_text(json.dumps(data, indent=2))

    with pytest.raises(RuntimeError, match="Config alterada|hash no coincide"):
        _load_chain(store)


def test_legacy_format_rejected_explicitly(tmp_path: Path):
    """
    Genesis sin chain_params_hash (formato legado): rechazo explícito.
    """
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    store.save_config(config)
    blocks = list(chain.blocks)
    blocks[0].chain_params_hash = None
    store.save_blocks(blocks)

    with pytest.raises(RuntimeError, match="Formato legacy|chain_params_hash"):
        _load_chain(store)


def test_same_dataset_altered_config_fails_no_silent_corruption(tmp_path: Path):
    """
    Mismo blocks.json, config.json alterada: fallo explícito, no reconstrucción corrupta.
    """
    store = Store(tmp_path)
    config = Config(difficulty=2, block_reward=100, default_asset_id="BASE")
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    store.save_config(config)
    store.save_blocks(chain.blocks)

    data = json.loads(store.config_file.read_text())
    data["difficulty"] = 4
    store.config_file.write_text(json.dumps(data, indent=2))

    with pytest.raises(RuntimeError, match="Config alterada|hash no coincide"):
        _load_chain(store)


def test_load_correct_with_unchanged_config(tmp_path: Path):
    """Carga correcta con config idéntica a la usada al crear genesis."""
    store = Store(tmp_path)
    config = Config(difficulty=3, block_reward=150, default_asset_id="BASE")
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    store.save_config(config)
    store.save_blocks(chain.blocks)

    chain2 = _load_chain(store)
    assert chain2.config.difficulty == 3
    assert chain2.config.block_reward == 150
    ok, _ = chain2.validate_chain()
    assert ok
    genesis_comm = str(chain2.blocks[0].coinbase_commitment)
    assert chain2.state.notes[genesis_comm].asset_id == "BASE"


def test_config_for_chain_verifies_hash(tmp_path: Path):
    """config_for_chain rechaza config alterada."""
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    store.save_config(config)
    store.save_blocks(chain.blocks)

    data = json.loads(store.config_file.read_text())
    data["block_reward"] = 999
    store.config_file.write_text(json.dumps(data, indent=2))

    with pytest.raises(RuntimeError, match="Config alterada|hash no coincide"):
        store.config_for_chain(store.load_blocks())
