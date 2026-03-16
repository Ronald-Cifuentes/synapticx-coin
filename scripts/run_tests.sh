#!/usr/bin/env bash
# Requiere: pip install -e ".[dev]" desde raíz del repo (antes de ejecutar)
set -e
cd "$(dirname "$0")/.."
pytest tests/ -v
