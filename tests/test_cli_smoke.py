"""Tests smoke para CLI."""

import tempfile
from pathlib import Path

import pytest

from coinlab.chain import Blockchain
from coinlab.cli import _run_demo_in_memory
from coinlab.config import Config
from coinlab.store import Store


def test_run_demo():
    """Demo ejecuta sin error."""
    _run_demo_in_memory()


def test_init_chain_persists(tmp_path):
    """init-chain persiste bloques."""
    from coinlab.cli import init_chain

    init_chain(data_dir=tmp_path, difficulty=2)
    store = Store(tmp_path)
    blocks = store.load_blocks()
    assert len(blocks) == 1
    assert blocks[0].header.prev_hash == "0" * 64
