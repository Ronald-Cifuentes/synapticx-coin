# TP-001: Consensus ordering (blockDAG + privado)

## Hipótesis

Un PoW blockDAG con transacciones privadas, ordering determinístico, nullifiers y reorgs puede implementarse con complejidad manejable y coste de verificación razonable. Dos implementaciones independientes producen el mismo ordering canónico.

## Setup

- Consenso blockDAG con 4+ mineros paralelos
- Transacciones con nullifiers y commitments
- 10k bloques con conflictos simulados (mismo nullifier en bloques concurrentes)
- Dos implementaciones independientes del algoritmo de ordenación
- Hardware: commodity (ej. 4 cores, 8 GB RAM)

## Métrica

| Métrica | Umbral éxito | Umbral aborto |
|---------|--------------|---------------|
| Consistencia de ordering | Ambas implementaciones producen mismo orden canónico | Divergencia en cualquier caso |
| Ambiguidad en conflictos | 0 conflictos no resolubles | Cualquier ambigüedad |
| Tiempo ordenación/bloque | <50 ms | >200 ms |
| Coste verificación/bloque | <100 ms | >500 ms |

## Criterio de éxito

- Ordering idéntico entre implementaciones en 10k bloques
- Sin ambigüedad en resolución de nullifiers
- Tiempo de ordenación <50 ms por bloque
- Verificación completa <100 ms por bloque

## Criterio de aborto

- Divergencia en ordering
- Conflictos de nullifiers no resolubles de forma determinística
- Tiempo >200 ms por bloque (ordenación o verificación)

## Artifacts esperados

- `conformance/vectors/ordering-*.json` — Vectores de ordenación canónica
- `conformance/fixtures/dag-conflicts/` — Casos de conflicto con resultado esperado
- `conformance/invalid-cases/` — Casos que deben rechazarse
- Informe de benchmark en `research/consensus-lab/`
- Si aborto: documento de downgrade a cadena lineal
