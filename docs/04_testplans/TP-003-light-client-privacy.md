# TP-003: Light client privacy

## Hipótesis

Existe diseño de light client que permite a un usuario móvil descubrir sus notas y verificar estado sin que un proveedor malicioso pueda correlacionar >10% de su actividad con confianza >80%. El coste de ancho de banda y batería es aceptable para uso móvil.

## Setup

- Light client que solicita lotes de note commitments a 1–3 proveedores
- Descifrado local de notas propias
- Simulador de proveedor adversario que registra patrones de solicitud
- Dispositivo móvil real o emulador con restricciones de batería
- 100+ transacciones de prueba por usuario simulado

## Métrica

| Métrica | Umbral éxito | Umbral aborto |
|---------|--------------|---------------|
| Correlación por adversario | ≤10% de tx correlacionables | >50% |
| Ancho de banda por sync | ≤500 MB | >2 GB |
| Batería (24h uso pasivo) | ≤5% | >15% |
| Batería (1h uso activo) | ≤3% | >8% |

## Criterio de éxito

- Proveedor adversario no puede correlacionar >10% de transacciones con confianza >80%
- Sync completo ≤500 MB
- Batería ≤5%/día en uso pasivo, ≤3%/h en uso activo

## Criterio de aborto

- Cualquier diseño práctico revela >50% de actividad
- Ancho de banda >2 GB por sync
- Batería >15%/día o >8%/h

## Artifacts esperados

- Prototipo en `research/light-client-lab/`
- Informe de métricas de correlación
- Informe de ancho de banda y batería
- Si aborto: documento de downgrade (lanzamiento restringido a full node)
