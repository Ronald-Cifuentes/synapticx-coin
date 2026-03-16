# Consensus geometry — Research item

## Question

¿Un PoW blockDAG con transacciones privadas y ordering determinístico es implementable con complejidad manejable y coste de verificación razonable?

## Why it matters

blockDAG permitiría throughput paralelo. Cadena lineal ya implementada es fallback. Si DAG no sobrevive, se degrada a lineal sin perder invariantes.

## Cadena lineal (implementada)

| Aspecto | Estado |
|---------|--------|
| PoW | `src/coinlab/pow.py` |
| Bloques en orden | `chain.py`, `add_block` |
| Reorg por trabajo | `reorg_to`, `cumulative_work` |
| Nullifier único | Segundo bloque con mismo nullifier rechazado |

## blockDAG (hipótesis abierta)

| Aspecto | Estado |
|---------|--------|
| Geometría DAG | No implementada |
| Ordering determinístico | No implementada |
| Conflictos nullifier | Harness define caso; DAG debe resolver |

## Criterios para degradar a lineal

| Condición | Decisión |
|-----------|----------|
| Divergencia en ordering entre implementaciones | Downgrade |
| Conflictos de nullifiers no resolubles | Downgrade |
| Tiempo ordenación >200 ms/bloque | Downgrade |
| Verificación >500 ms/bloque | Downgrade |

## Simulations/harnesses mínimos

| Harness | Ubicación | Qué hace |
|---------|-----------|----------|
| Nullifier conflict | `simulations/dag-ordering/run_nullifier_conflict_simulator.py` | Verifica que lineal rechaza segundo bloque con mismo nullifier; define caso que DAG debe resolver |

## Tasks

1. [ ] Implementar DAG (no existe)
2. [ ] Dos implementaciones independientes del ordering (no existe)
3. [ ] 10k bloques con conflictos simulados (no existe)
4. [ ] Benchmark ordenación y verificación

## Deliverables

- `conformance/vectors/ordering-*.json` — bloqueado hasta DAG
- `conformance/fixtures/dag-conflicts/` — bloqueado hasta DAG
- Informe de benchmark
- Documento de downgrade a lineal (path ya definido)

## Acceptance criteria

| Métrica | Éxito | Aborto |
|---------|-------|--------|
| Consistencia ordering | Idéntico entre implementaciones | Divergencia |
| Conflictos no resolubles | 0 | Cualquiera |
| Tiempo ordenación/bloque | <50 ms | >200 ms |
| Verificación/bloque | <100 ms | >500 ms |

## Kill / downgrade trigger

- **Kill:** DAG inviable (ordering ambiguo, coste prohibitivo)
- **Downgrade:** Cadena lineal (ya implementada). Mismo modelo de notas y nullifiers.

## Dependencies

- MVP lineal (existe)
- Harness conflicto nullifier (existe)

## Priority

P1 — Mejora de throughput. No bloqueante; lineal es suficiente para MVP.

## Harness ejecutable

```bash
python simulations/dag-ordering/run_nullifier_conflict_simulator.py
```

**Resultado actual:** MVP lineal. Segundo bloque con mismo nullifier RECHAZADO. DAG no implementado. Harness define caso de conflicto a resolver.
