# Conformance Vectors

## Propósito

Vectores de prueba para validación de implementaciones. **No asumen protocolo cerrado.**

## Estructura

- `supply-*.json` — Conservación válida (pendiente: formato con proofs)
- `ordering-*.json` — Ordenación canónica para DAG (pendiente: DAG no implementado)

## Estado

El MVP actual tiene fixtures en `conformance/fixtures/valid_chain/`. Los vectores de supply con ZK están bloqueados hasta tener construcción criptográfica. Los vectores de ordering para DAG están bloqueados hasta implementar DAG.

## Harness actual

Los tests en `tests/test_conformance.py` y `tests/test_supply_correctness.py` ejercitan los invariantes sin vectores JSON externos.
