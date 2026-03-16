#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
pip install -e ".[dev]" -q
pytest tests/ -v
