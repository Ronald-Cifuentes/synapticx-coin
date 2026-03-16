"""
Tests que documentan el estado PARCIAL del wallet local.

wallets.json es cache de demo. No hay reconcile ni rescan.
Si la cache se desincroniza de la cadena, no se corrige automáticamente.
"""

import json
from pathlib import Path

import pytest

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.notes import create_note, deserialize_note, serialize_note
from coinlab.store import Store


def test_wallet_cache_not_reconciled_on_load(tmp_path: Path):
    """
    Documenta: al cargar, wallets.json se usa tal cual. No hay rescan desde cadena.
    Si wallets.json está desincronizado, el estado mostrado es incorrecto.
    """
    store = Store(tmp_path)
    config = Config(difficulty=2)
    chain = Blockchain(config)
    chain.create_genesis("faucet")
    faucet_note = create_note("faucet", 100, "BASE")
    alice_note = create_note("alice", 50, "BASE")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    # Cache inicial: alice tiene 50
    store.save_wallets({"faucet": [serialize_note(faucet_note)], "alice": [serialize_note(alice_note)]})

    # Simular desincronización: alguien edita wallets.json y borra la nota de alice
    wallets = store.load_wallets()
    wallets["alice"] = []
    store.save_wallets(wallets)

    # Al cargar wallets, se usa el JSON tal cual. No hay rescan desde cadena.
    loaded = store.load_wallets()
    assert loaded["alice"] == []
    # La cadena/estado real podría tener notas de alice en outputs, pero wallets.json
    # no se reconcilia. Estado PARCIAL: la cache puede estar mal.
    assert "reconcile" not in dir(store)
    assert "rescan" not in dir(store)


def test_wallet_cache_is_demo_helper_not_canonical(tmp_path: Path):
    """
    Documenta: wallets.json no es fuente canónica. La cadena lo es.
    """
    store = Store(tmp_path)
    # Podemos tener wallets.json con datos que no existen en cadena
    fake_note = serialize_note(create_note("ghost", 999, "BASE"))
    store.save_wallets({"ghost": [fake_note]})
    # La cadena está vacía - no hay genesis
    assert not store.load_blocks()
    # wallets.json dice ghost tiene 999, pero la cadena no lo respalda
    # No hay validación cruzada. Cache de demo, no verdad.
    wallets = store.load_wallets()
    assert wallets["ghost"] == [fake_note]
