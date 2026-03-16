# Network metadata privacy — Research item

## Question

¿Un relay staging (Dandelion-like) reduce la inferencia de origen de forma material vs. gossip plano sin destruir latencia ni consumo de batería en móvil?

## Why it matters

Gossip plano: el primer nodo que recibe un mensaje suele ser vecino del origen. Un adversario con spy nodes puede inferir origen con alta probabilidad. Privacidad de red es obligatoria; sin mitigación, metadatos revelan grafos.

## Adversary model

| Elemento | Descripción |
|----------|-------------|
| Spy nodes | Nodos adversarios que registran cuándo reciben cada tx |
| Visibilidad | Parcial: spy no controla toda la red |
| Objetivo | Identificar nodo origen dado el orden de recepción |

## Spy-node model

- Grafo: anillo (simplificado) o topología realista
- Spy como vecino del origen: recibe en ronda 1 → inferencia ~100%
- Spy lejano: inferencia ~0% (en modelo actual)
- Relay stem: origen envía por cadena de 1 nodo; broadcast desde último

## Timing correlation model

- Cada spy registra: (tx_id, round_received)
- Inferencia: primer spy en recibir es vecino del origen (gossip) o del relay (stem)
- Relay diluye: quien recibe en fase stem no sabe si es origen o relay

## Mobile constraints

| Métrica | Éxito | Aborto |
|---------|-------|--------|
| Latencia p99 | <30 s | >2 min |
| Batería 1h uso | <3% | >8% |
| Inferencia origen | ≤30% | >60% |

## Degraded mode policy

Si inferencia >60% o latencia/batería inusable:
- **No fingir** protección fuerte
- Modos degradados explícitos: "Privacidad reducida en esta configuración"
- Comunicar honestamente cuándo la privacidad está debilitada

## Tasks

1. [ ] Integrar relay staging con wallet (no existe)
2. [ ] Medir latencia y batería en dispositivo real
3. [ ] Topología más realista (no solo anillo)
4. [ ] Documentar modos degradados

## Deliverables

- Resultados de simulación (ya en `simulations/provider-correlation/`)
- Informe de inferencia, latencia, batería
- Especificación de modos degradados

## Acceptance criteria

| Métrica | Éxito | Aborto |
|---------|-------|--------|
| Inferencia | ≤30% | >60% |
| Latencia p99 | <30 s | >2 min |
| Batería 1h | <3% | >8% |

## Kill / downgrade trigger

- **Kill:** Inferencia >60% con cualquier diseño práctico
- **Downgrade:** Modos degradados explícitos; no fingir protección

## Dependencies

- Simulador `simulations/provider-correlation/` (existe)
- Wallet integrado (no existe para medición real)

## Priority

P0 — Privacidad de red obligatoria. Sin mitigación, metadatos revelan.

## Harness ejecutable

```bash
python simulations/provider-correlation/run_correlation_simulator.py
```

**Resultado actual:** Gossip + spy vecino ~100% inferencia (ABORTA). Relay stem=2 reduce. Modelo simplificado; métricas reales requieren integración con wallet.
