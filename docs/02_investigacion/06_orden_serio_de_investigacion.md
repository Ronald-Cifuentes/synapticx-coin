# Orden serio de investigación

## Propósito

Orden duro, no paralelo por entusiasmo. Cada fase depende de que la anterior haya producido evidencia favorable. No se investiga la fase N+1 hasta que la fase N no haya matado el programa.

---

## Orden

### Fase 1. Soundness monetaria privada

**Objetivo:** Demostrar que existe construcción criptográfica para conservación de valor oculta + nullifiers + issuance + supply auditable.

**Bloqueante:** B2 (Supply correctness).

**Salida:** Especificación verificada o evidencia de que no existe. Si no existe, el programa muere.

**No continuar a Fase 2 si:** Supply correctness no es auditable.

---

### Fase 2. Cliente ligero viable

**Objetivo:** Demostrar que existe diseño de light client que no filtra grafo de actividad de forma catastrófica.

**Bloqueante:** B1 (Cliente ligero privado).

**Salida:** Prototipo que pasa criterios de éxito o evidencia de fracaso. Si fracasa, downgrade: lanzamiento restringido.

**No continuar a Fase 3 con ambición masiva si:** Light client es suicida. Se puede continuar con ambición restringida.

---

### Fase 3. Privacidad de red usable

**Objetivo:** Demostrar que relay/mixnet reduce inferencia de origen de forma material sin destruir usabilidad móvil.

**Bloqueante:** B4 (Privacidad de red).

**Salida:** Prototipo con métricas. Si fracasa, downgrade: modos degradados explícitos.

**No continuar a Fase 4 con protección fuerte si:** Privacidad de red es inusable. Se puede continuar con modos degradados honestos.

---

### Fase 4. Geometría del ledger

**Objetivo:** Validar si blockDAG + privado es viable. Si no, cadena lineal.

**Bloqueante:** B3 (blockDAG + estado privado).

**Salida:** blockDAG validado o downgrade a lineal. No es kill; es simplificación.

**No paralelizar con Fases 1–3:** La geometría depende de que el estado privado (Fase 1) y el light client (Fase 2) no contradigan el ordering.

---

### Fase 5. Producto mínimo

**Objetivo:** Wallet honesta que distingue capas, privacy mode, finality. Que la ruta más fácil no sea custodial.

**Hipótesis:** H4 (pagos rápidos), H5 (wallet honesta).

**Salida:** Prototipo de producto que pasa tests de usabilidad.

**No antes de Fases 1–4:** El producto depende de que exista algo que construir (base, cliente, red).

---

### Fase 6. Disclosure

**Objetivo:** Validar que pruebas estrechas sirven para comercio sin composición leaky.

**Hipótesis:** H3 (disclosure acotado).

**Salida:** Análisis de composición. Si leaky, downgrade a proofs mínimos.

**No antes de Fase 5:** El disclosure se integra en producto.

---

### Fase 7. Stable unit

**Objetivo:** Diseño de unidad estable privada sin recentralización. Solo si la visión la exige.

**Bloqueante:** B5.

**Salida:** Diseño validado o pospuesto.

**No antes de Fases 1–6:** La stable unit depende de base sólida. Si la base no existe, la stable no tiene sentido.

---

### Fase 8. Gobernanza final

**Objetivo:** Mecanismos formales de gobernanza, multi-implementación, emergencia acotada.

**Problema:** Político/social. No solo tecnología.

**Salida:** Mecanismos que no contradigan principios. Puede iterarse después del lanzamiento.

**Última:** La gobernanza depende de saber qué capas sobreviven. No tiene sentido fijarla antes.

---

## Diagrama de dependencias

```
Fase 1 (Supply) ──► Fase 2 (Light client) ──► Fase 3 (Network) ──► Fase 4 (Geometry)
       │                    │                        │                     │
       └────────────────────┴────────────────────────┴─────────────────────┘
                                              │
                                              ▼
                                    Fase 5 (Producto)
                                              │
                                    ┌─────────┴─────────┐
                                    ▼                   ▼
                            Fase 6 (Disclosure)   Fase 7 (Stable)
                                    │                   │
                                    └─────────┬─────────┘
                                              ▼
                                    Fase 8 (Gobernanza)
```

---

## Regla de no paralelización prematura

No iniciar Fase N+1 hasta que Fase N haya producido evidencia que no mate el programa. Paralelizar solo dentro de una fase (ej. distintos experimentos del mismo bloqueante), no entre fases con dependencias.
