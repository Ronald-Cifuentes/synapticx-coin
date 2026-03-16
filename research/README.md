# Research labs

## Propósito

Cada lab investiga un bloqueante o hipótesis. **No** contiene implementación de protocolo final. Contiene prototipos, experimentos y harnesses para validar viabilidad.

**Rebaja epistemológica:** Simulador ≠ solución. Harness ≠ prototipo de protocolo. Target metric ≠ métrica medida. Hipótesis ≠ evidencia. Los resultados de los simuladores informan diseño, no cierran bloqueantes.

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

Cada lab tiene:
- Hipótesis explícita
- Simulador o harness ejecutable (ver README de cada lab)
- Métricas y umbrales (TP-001 a TP-006)
- Kill criteria y downgrade paths

Simuladores en `simulations/` (harnesses, no prototipos de protocolo):
- `light-client-leakage/` — correlación por patrón de consulta
- `provider-correlation/` — inferencia de origen (gossip vs relay)
- `dag-ordering/` — conflicto de nullifier (harness para DAG futuro)
