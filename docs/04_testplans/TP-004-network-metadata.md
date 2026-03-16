# TP-004: Network metadata privacy

## Hipótesis

Un relay staging (Dandelion-like o mixnet simplificado) reduce la inferencia de origen de forma material (vs. gossip plano) sin destruir latencia ni consumo de batería en móvil. Un adversario con visibilidad parcial no puede identificar el origen con confianza >30%.

## Setup

- Relay staging integrado con wallet
- 100 nodos, 10% adversarios (spy nodes)
- Medición de inferencia de origen: probabilidad de que adversario identifique origen correcto
- Dispositivo móvil o emulador para latencia y batería
- Comparación con baseline: gossip plano (~90% inferencia en condiciones típicas)

## Métrica

| Métrica | Umbral éxito | Umbral aborto |
|---------|--------------|---------------|
| Inferencia de origen | ≤30% | >60% |
| Latencia p99 | <30 s | >2 min |
| Batería (1h uso) | <3% | >8% |

## Criterio de éxito

- Inferencia ≤30% (reducción material vs. 90% en gossip)
- Latencia p99 <30 s
- Batería <3%/h en uso típico

## Criterio de aborto

- Inferencia >60% (protección insuficiente)
- Latencia p99 >2 min (inusable)
- Batería >8%/h (inusable en móvil)

## Artifacts esperados

- Prototipo en `research/network-lab/`
- Resultados de simulación en `simulations/provider-correlation/`
- Informe de inferencia, latencia y batería
- Si aborto: documento de modos degradados explícitos; no fingir protección fuerte
