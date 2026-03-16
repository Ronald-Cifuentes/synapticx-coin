# Simulations

## Propósito

Simulaciones para validar hipótesis y medir comportamiento bajo condiciones adversas. **No** son tests de integración de producción. Son experimentos controlados.

## Directorios

| Directorio | Bloqueante/Hipótesis | Objetivo |
|------------|----------------------|----------|
| dag-ordering | blockDAG + privado | Ordering determinístico, conflictos de nullifiers |
| supply-correctness | Supply auditable | Conservación, detección de inflación |
| mining-centralization | PoW, pools | Concentración de hashrate, ventana de participación |
| provider-correlation | Light client, red | Qué puede inferir un proveedor adversario |
| disclosure-composition | Disclosure acotado | Reconstrucción de grafo con N pruebas |

## Qué se simula aquí

- Comportamiento bajo minería paralela
- Ataques de inferencia (origen, correlación)
- Estrés económico (colapso de colateral, corridas)
- Concentración de poder (mining, providers)

## Qué NO debe meterse aquí

- Datos de mainnet real (no existe)
- Simulaciones que asumen protocolo cerrado
- Resultados sin criterios de éxito/aborto definidos

## Artefacts

Los resultados deben alimentar `conformance/vectors` y `conformance/invalid-cases` cuando corresponda. Ver `docs/04_testplans/`.
