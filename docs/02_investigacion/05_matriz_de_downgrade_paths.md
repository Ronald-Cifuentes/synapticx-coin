# Matriz de downgrade paths

## Propósito

Rutas de simplificación concretas cuando una hipótesis o bloqueante falla. Cada una preserva invariantes aunque reduzca alcance.

---

| Si falla | Downgrade path | Qué se preserva | Qué se pierde |
|----------|----------------|------------------|---------------|
| **blockDAG** | Cadena lineal PoW | Consenso, privacidad, supply correctness | Throughput paralelo |
| **blockDAG** | Mismo modelo de notas y nullifiers. Misma PoW. Solo cambia geometría del ledger. | | |
| **Stable unit** | Posponer capa estable | Base, pagos rápidos, disclosure esencial | Estabilidad para comercio diario |
| **Stable unit** | Lanzar con base + fast payments únicamente. | | |
| **Disclosure amplio** | Proofs mínimos: pago, recibo, liquidación de factura | Interoperabilidad legal básica | Nómina, auditoría, reservas, proof complejos |
| **Disclosure amplio** | Eliminar tipos de prueba que no pasan composición. | | |
| **Recovery complejo** | Threshold recovery simple; seed + multisig | Recuperación sin custodia | Social recovery, recovery institucional |
| **Recovery complejo** | No ofrecer recovery que derive en custodia oculta. | | |
| **Privacidad de red fuerte** | Modos degradados explícitos | Funcionalidad básica | Protección de metadatos en condiciones débiles |
| **Privacidad de red fuerte** | Comunicar con honestidad cuándo la privacidad está debilitada. No fingir. | | |
| **Cliente ligero privado** | Lanzamiento restringido a full node o infra comunitaria | Base soberana, privacidad | Adopción móvil masiva |
| **Cliente ligero privado** | No lanzar light client hasta que exista diseño no suicida. | | |
| **Pagos rápidos** | Eliminar o simplificar capa | Base pura | UX de pagos instantáneos |
| **Pagos rápidos** | Si la capa es capturable o indispensable, recortarla. | | |
| **Multi-implementación** | Una implementación al inicio | Protocolo funcional | Pluralidad de clientes |
| **Multi-implementación** | Objetivo a largo plazo; no requisito de día uno. | | |

---

## Regla de aplicación

Aplicar el downgrade path cuando la evidencia de fracaso supere el criterio definido en `03_experimentos_y_prototipos_minimos.md`. No posponer la decisión. No racionalizar que "con más tiempo saldrá".
