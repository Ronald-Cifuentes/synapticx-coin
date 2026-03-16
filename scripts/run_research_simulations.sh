#!/bin/bash
# Ejecuta simuladores de investigación (light client, provider correlation, DAG)
set -e
cd "$(dirname "$0")/.."
echo "=== Light Client Leakage ==="
python simulations/light-client-leakage/run_leakage_simulator.py
echo ""
echo "=== Provider Correlation ==="
python simulations/provider-correlation/run_correlation_simulator.py
echo ""
echo "=== DAG Nullifier Conflict ==="
python simulations/dag-ordering/run_nullifier_conflict_simulator.py
