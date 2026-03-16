# Light-client privacy and note discovery — Research item

## Question

¿Existe diseño de light client que permita descubrir notas propias y verificar estado sin que un proveedor adversario pueda correlacionar >10% de la actividad del usuario con confianza >80%?

## Why it matters

Adopción móvil masiva con query directa "¿tienes commitment C?" = privacidad suicida. Si no hay ruta viable, el lanzamiento queda restringido a full node o infra comunitaria. Es bloqueante constitucional.

## Threat model

| Elemento | Descripción |
|----------|-------------|
| Adversario | Proveedor que registra qué commitments solicita cada cliente |
| Leakage | Si cliente pide C → proveedor infiere que posee C |
| Confianza | Adversario asigna probabilidad a ownership por patrón de consulta |

## Leakage model

| Patrón | Correlación (simulador) | Riesgo |
|--------|-------------------------|--------|
| Full sync | 0% | Descarga todo; no pide nada específico |
| Naive query | 100% | Cada consulta revela ownership |
| Batch pequeño | ~71% (size=5) | Depende del tamaño |
| Batch = all | 0% | Equivale a full sync |

## Provider assumptions

- Proveedor ve: qué commitments se solicitan, cuándo, en qué orden
- Proveedor no ve (por diseño): contenido de notas, montos, grafos
- Proveedor puede: correlacionar solicitudes con identidad de sesión

## Local verification target

- Cliente verifica: merkle proofs, block headers, supply agregado (cuando exista)
- Cliente no revela: qué commitments posee al solicitar datos
- Objetivo: sync ≤500 MB, batería ≤5%/día pasivo, ≤3%/h activo

## Tasks

1. [ ] Extender simulador con modelo de batch + padding
2. [ ] Medir correlación en función de batch size y ruido
3. [ ] Prototipo de diseño (si existe) con métricas reales
4. [ ] Documentar si full sync es única opción viable

## Deliverables

- Informe de correlación por patrón (ya existe en simulador)
- Especificación de diseño candidato (si existe)
- Métricas de ancho de banda y batería en dispositivo real

## Acceptance criteria

| Métrica | Éxito | Aborto |
|---------|-------|--------|
| Correlación | ≤10% | >50% |
| Ancho de banda/sync | ≤500 MB | >2 GB |
| Batería 24h pasivo | ≤5% | >15% |
| Batería 1h activo | ≤3% | >8% |

## Kill / downgrade trigger

- **Kill:** Cualquier diseño práctico revela >50% de actividad
- **Downgrade:** Lanzamiento restringido a full node; comunidad/infra como única opción light

## Dependencies

- MVP con notas y nullifiers (existe)
- Simulador `simulations/light-client-leakage/` (existe)

## Priority

P0 — Bloqueante constitucional. Sin esto, no hay adopción móvil masiva sin privacidad suicida.

## Harness ejecutable

```bash
python simulations/light-client-leakage/run_leakage_simulator.py
```

**Resultado actual:** Naive query ABORTA (100%). Full sync no revela. Batch intermedio depende del tamaño.
