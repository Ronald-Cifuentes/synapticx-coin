# light-client-lab

**Bloqueante:** B1 — Cliente ligero privado viable.

**Test plan:** TP-003.

## Hipótesis

Existe diseño de light client que permite descubrir notas y verificar estado sin que proveedor correlacione >10% de actividad (confianza >80%).

## Simulador ejecutable

```bash
python simulations/light-client-leakage/run_leakage_simulator.py
```

## Métricas

| Métrica | Éxito | Aborto |
|---------|-------|--------|
| Correlación por adversario | ≤10% | >50% |
| Ancho de banda/sync | ≤500 MB | >2 GB |
| Batería (24h pasivo) | ≤5% | >15% |

## Resultado del simulador (no evidencia de protocolo)

- Full sync: 0% correlación en el modelo simplificado
- Naive query: 100% correlación (ABORTA en el simulador)
- Batch: depende del tamaño

Target metric ≠ métrica medida en entorno real.

## Kill criterion

Si cualquier diseño práctico revela >50% de actividad → downgrade a full node only.
