# network-lab

**Bloqueante:** B4 — Privacidad de red usable.

**Test plan:** TP-004.

## Hipótesis

Relay staging (Dandelion-like) reduce inferencia de origen vs gossip plano sin destruir latencia.

## Simulador ejecutable

```bash
python simulations/provider-correlation/run_correlation_simulator.py
```

## Métricas

| Métrica | Éxito | Aborto |
|---------|-------|--------|
| Inferencia de origen | ≤30% | >60% |
| Latencia p99 | <30 s | >2 min |
| Batería (1h) | <3% | >8% |

## Resultado del simulador (modelo simplificado)

- Gossip + spy vecino: ~100% inferencia
- Gossip + spy lejano: ~0%
- Relay stem=2: diluye señal

## Kill criterion

Inferencia >60% → modos degradados explícitos; no fingir protección fuerte.
