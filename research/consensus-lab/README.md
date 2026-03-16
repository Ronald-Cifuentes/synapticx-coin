# consensus-lab

**Bloqueante:** B3 — Viabilidad blockDAG + ordering + estado privado.

**Test plan:** TP-001.

## Hipótesis

PoW blockDAG + transacciones privadas + ordering determinístico es implementable con complejidad manejable.

## Harness ejecutable

```bash
python simulations/dag-ordering/run_nullifier_conflict_simulator.py
```

## Caso de conflicto definido

Dos bloques con mismo nullifier (doble gasto). Lineal: segundo rechazado. DAG: ordering debe elegir uno.

## Métricas (cuando DAG exista)

| Métrica | Éxito | Aborto |
|---------|-------|--------|
| Consistencia ordering | Idéntico entre implementaciones | Divergencia |
| Tiempo ordenación/bloque | <50 ms | >200 ms |
| Conflictos no resolubles | 0 | Cualquiera |

## Decisión

- **Sigue vivo:** DAG aporta valor sin volver todo inmanejable
- **Downgrade:** Cadena lineal (ya implementada)
- **Falta evidencia:** No hay DAG aún para medir
