# Research labs

## Propósito

Cada lab investiga un bloqueante o hipótesis. **No** contiene implementación de protocolo final. Contiene prototipos, experimentos y harnesses para validar viabilidad.

## Labs

| Lab | Bloqueante/Hipótesis | Test plan |
|-----|----------------------|-----------|
| consensus-lab | blockDAG + ordering + privado | TP-001 |
| privacy-lab | Supply correctness, circuitos ZK | TP-002 |
| light-client-lab | Cliente ligero privado viable | TP-003 |
| network-lab | Privacidad de red usable | TP-004 |
| disclosure-lab | Composición de pruebas | TP-005 |
| stable-unit-lab | Unidad estable sin recentralización | TP-006 |

## Qué se investiga aquí

- **Viabilidad:** ¿Existe solución que cumpla criterios?
- **Diseño:** Especificaciones y prototipos mínimos
- **Métricas:** Correlación, latencia, batería, coste de verificación

## Qué NO debe meterse aquí

- Código que parezca "mainnet-ready"
- Implementación de protocolo final antes de cerrar bloqueantes
- Features que asumen que los bloqueantes están resueltos

## Estado

Los labs están vacíos o con stubs. **No hay implementación de protocolo.** El código que se añada debe ser scaffold o harness para validar hipótesis. Código que parezca mainnet-ready antes de cerrar bloqueantes es engañoso.
