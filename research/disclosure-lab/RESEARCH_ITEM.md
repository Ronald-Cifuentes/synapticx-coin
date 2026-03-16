# Disclosure composition — Research item

## Question

¿Las pruebas estrechas (pago, recibo, factura, nómina, reserva) pueden usarse en flujos comerciales sin que la composición de N pruebas permita a un adversario reconstruir >20% del grafo financiero del usuario?

## Why it matters

Disclosure acotado es requisito para interoperabilidad legal (pago, recibo, factura). Si la composición de pruebas es leaky, cada prueba adicional revela más de lo previsto. Nómina, auditoría, reservas amplían el riesgo.

## Hipótesis

Con 20 pruebas típicas en 1 año, adversario que recibe todas reconstruye ≤20% del grafo con confianza >80%.

## Tasks

1. [ ] Modelo formal de 5 tipos de prueba (scope: tiempo, audiencia, granularidad)
2. [ ] Simulación: usuario genera 20 pruebas según distribución típica
3. [ ] Adversario que intenta reconstruir grafo
4. [ ] Métrica: % grafo reconstruible

## Deliverables

- Modelo formal en `research/disclosure-lab/`
- Resultados en `simulations/disclosure-composition/` (harness pendiente)
- Catálogo combinaciones seguras vs. leaky

## Acceptance criteria

| Métrica | Éxito | Aborto |
|---------|-------|--------|
| Grafo reconstruible (20 pruebas) | ≤20% | >60% |
| Grafo reconstruible (10 pruebas) | ≤15% | >50% |

## Kill / downgrade trigger

- **Kill:** 10+ pruebas comunes permiten reconstrucción >60%
- **Downgrade:** Reducir a pago, recibo, factura únicamente

## Dependencies

- Modelo formal (no existe)
- Simulador composición (no existe — ver nota)

## Priority

P1 — Disclosure amplio (nómina, auditoría) es ambicioso. Esencial: pago, recibo, factura.

## Experimento razonable

**No existe harness ejecutable aún.** `simulations/disclosure-composition/` tiene solo README. Para cerrar la hipótesis se requiere:
- Definir estructura de prueba (scope, audiencia, granularidad)
- Simulador que genere N pruebas y estime % grafo reconstruible
- Adversario que recibe pruebas y reconstruye

Se declara explícitamente: **no hay experimento ejecutable para este frente.**
