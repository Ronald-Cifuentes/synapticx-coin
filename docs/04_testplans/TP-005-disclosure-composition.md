# TP-005: Disclosure composition

## Hipótesis

Las pruebas estrechas (pago, recibo, factura, nómina, reserva) pueden usarse en flujos comerciales sin que la composición de N pruebas permita a un adversario reconstruir >20% del grafo financiero del usuario. Con combinaciones típicas (ej. 20 pruebas en 1 año), el leak es acotado.

## Setup

- Modelo formal de 5 tipos de prueba con scope (tiempo, audiencia, granularidad)
- Simulación: usuario genera 20 pruebas en 1 año según distribución típica
- Adversario que recibe todas las pruebas y intenta reconstruir el grafo
- Métrica: % del grafo reconstruible con confianza >80%

## Métrica

| Métrica | Umbral éxito | Umbral aborto |
|---------|--------------|---------------|
| Grafo reconstruible (20 pruebas típicas) | ≤20% | >60% |
| Grafo reconstruible (10 pruebas comunes) | ≤15% | >50% |

## Criterio de éxito

- Con 20 pruebas de tipos típicos, adversario reconstruye ≤20% del grafo
- Con 10 pruebas comunes, ≤15%

## Criterio de aborto

- Con 10+ pruebas comunes, adversario reconstruye >60% del grafo
- Cualquier combinación razonable permite reconstrucción amplia

## Artifacts esperados

- Modelo formal en `research/disclosure-lab/`
- Resultados de simulación en `simulations/disclosure-composition/`
- Catálogo de combinaciones seguras vs. leaky
- Si aborto: reducir tipos de prueba a mínimos (pago, recibo, factura)
