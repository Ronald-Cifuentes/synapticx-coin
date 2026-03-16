# Stable unit — Research item

## Question

¿Existe diseño de unidad estable overcollateralizada que sobrevive estrés (colapso colateral 50% en 24h, corrida 80% supply) sin recentralización, sin custodio único, con auditoría agregada posible?

## Why it matters

Unidad estable permite comercio diario sin volatilidad. Si todo diseño creíble requiere custodio único u oráculo central, la capa estable contamina soberanía. Mejor posponer.

## Hipótesis

Diseño overcollateralizado privado sobrevive estrés sin recentralización.

## Tasks

1. [ ] Diseño formal: colateral privado, liquidaciones, redención, oráculos
2. [ ] Simulador estrés: colapso 50% colateral en 24h
3. [ ] Simulador corrida: 80% supply redime en ventana corta
4. [ ] Verificar: ¿sobrevive sin custodio único? ¿solvencia auditable?

## Deliverables

- Diseño formal en `research/stable-unit-lab/`
- Resultados de simulación (directorio dedicado pendiente)
- Informe de estrés y auditoría

## Acceptance criteria

| Métrica | Éxito | Aborto |
|---------|-------|--------|
| Sobrevive estrés | Sí, sin recentralización | Requiere intervención central |
| Custodio único | No requerido | Requerido |
| Auditoría agregada | Posible | Imposible sin exponer grafos |
| Oráculo | Mínimo o distribuido | Único y central |

## Kill / downgrade trigger

- **Kill:** Todo diseño creíble requiere custodio único u oráculo central
- **Downgrade:** Posponer capa estable; lanzar con base + pagos rápidos únicamente

## Dependencies

- L1 base (existe)
- Diseño formal (no existe)
- Simulador estrés (no existe)

## Priority

P2 — Capa estable es ambiciosa. No bloqueante para MVP.

## Experimento razonable

**No existe harness ejecutable.** Para cerrar la hipótesis se requiere:
- Diseño formal de mecanismo
- Simulador de colapso de colateral
- Simulador de corrida de redención

Se declara explícitamente: **no hay experimento ejecutable para este frente.**
