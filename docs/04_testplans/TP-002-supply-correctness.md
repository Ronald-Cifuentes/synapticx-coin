# TP-002: Supply correctness

## Hipótesis

Existe construcción criptográfica que prueba conservación de valor oculta + range validity + nullifiers + issuance compliance, permitiendo auditoría agregada sin exponer montos ni grafos. Un auditor independiente puede derivar la emisión total en tiempo razonable.

## Setup

- Circuito ZK (o equivalente) que implemente: conservación, range, nullifiers, issuance
- Test vectors con inflación maliciosa que debe ser rechazada
- Implementación de auditoría agregada (derivación de emisión total desde estado público)
- Auditor independiente (persona o equipo distinto al desarrollador)
- Hardware: commodity para verificación

## Métrica

| Métrica | Umbral éxito | Umbral aborto |
|---------|--------------|---------------|
| Auditoría reproducible | Sí, en <1h | No reproducible |
| Verificación por tx | <100 ms | >500 ms |
| Inflación maliciosa | Rechazada en todos los vectores | Cualquier vector pasa |
| Revelación de grafos | Ninguna | Cualquier filtración de montos/grafos |

## Criterio de éxito

- Auditoría independiente deriva emisión total correctamente
- Verificación <100 ms por tx en hardware commodity
- Todos los vectores de inflación maliciosa son rechazados
- No se revelan montos ni grafos en el proceso

## Criterio de aborto

- No existe construcción que cumpla sin revelar más de lo permitido
- Verificación >500 ms por tx (centraliza validación)
- Cualquier vector de inflación pasa

## Artifacts esperados

- `conformance/vectors/supply-*.json` — Vectores de conservación válida
- `conformance/invalid-cases/inflation-*.json` — Casos de inflación que deben rechazarse
- Especificación del circuito y de la auditoría agregada
- Informe de auditoría independiente
- Si aborto: kill criterion; no hay downgrade para supply correctness
