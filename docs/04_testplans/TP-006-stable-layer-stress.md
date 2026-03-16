# TP-006: Stable layer stress

## Hipótesis

Existe diseño de unidad estable overcollateralizada que sobrevive estrés (colapso de colateral 50% en 24h, corrida de redención 80% del supply) sin recentralización, sin custodio único, con auditoría agregada posible.

## Setup

- Diseño formal de stable unit: colateral privado, liquidaciones, redención, oráculos mínimos
- Simulador de estrés: colapso de colateral 50% en 24h
- Simulador de corrida: 80% del supply intenta redimir en ventana corta
- Verificar: ¿sobrevive sin custodio único? ¿solvencia auditable en agregado?

## Métrica

| Métrica | Umbral éxito | Umbral aborto |
|---------|--------------|---------------|
| Sobrevive estrés | Sí, sin recentralización | Requiere intervención central |
| Custodio único | No requerido | Requerido como trust anchor |
| Auditoría agregada | Posible | Imposible sin exponer grafos |
| Oráculo central | Mínimo o distribuido | Único y central |

## Criterio de éxito

- Diseño sobrevive estrés sin recentralización
- Sin custodio único
- Solvencia auditable en agregado
- Oráculos acotados o distribuidos

## Criterio de aborto

- Todo diseño creíble requiere custodio único
- Todo diseño creíble requiere oráculo central
- Estrés revela insolvencia oculta o colapso no manejable

## Artifacts esperados

- Diseño formal en `research/stable-unit-lab/`
- Resultados de simulación en `simulations/` (si existe directorio dedicado)
- Informe de estrés y de auditoría
- Si aborto: posponer capa estable; lanzar con base + pagos rápidos únicamente
