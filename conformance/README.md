# Conformance

## Propósito

Vectores de prueba, fixtures y casos inválidos. **No hay implementaciones de protocolo.** Este directorio alimenta prototipos de investigación y, si los bloqueantes se cierran, futuras implementaciones. Hoy está vacío o con placeholders.

## Estructura

```
conformance/
  vectors/       — Casos válidos: ordering, supply, proofs
  fixtures/     — Datos de prueba reutilizables
  invalid-cases/ — Casos que deben rechazarse: inflación, conflictos, etc.
```

## Qué contiene

- **vectors:** Resultados esperados de ordenación canónica, conservación de valor, auditoría agregada
- **fixtures:** DAGs de prueba, transacciones con nullifiers, bloques con conflictos
- **invalid-cases:** Inflación maliciosa, nullifiers duplicados, proofs inválidos

## Qué NO debe meterse aquí

- Vectores que asumen protocolo cerrado sin validación previa
- Casos sin criterio de aceptación/rechazo definido
- Datos de producción (no existe mainnet)

## Bloqueante que intenta cerrar

Los vectores alimentan la validación de:
- TP-001 (consensus ordering)
- TP-002 (supply correctness)
- TP-003 a TP-006 (según corresponda)

Cuando un test plan produce evidencia favorable, los artifacts van aquí. Si un test plan aborta, los invalid-cases documentan por qué.
