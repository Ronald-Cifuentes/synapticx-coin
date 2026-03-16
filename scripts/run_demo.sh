#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
pip install -e . -q
python -m coinlab.cli run-demo
