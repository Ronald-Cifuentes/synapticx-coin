# Versión mínima defendible

## Advertencia

Este documento describe la versión más austera del proyecto si se recorta ambición. **No es un diseño listo para construir.** La versión mínima se parece más a Monero endurecido (mejor transporte, mejor wallet, capas superiores limitadas) que a una moneda total ya resuelta.

---

## Tesis central

Si se recorta ambición al mínimo que los invariantes permiten, el sistema resultante es:

- **Base:** PoW + notas privadas + nullifiers + conservación de valor auditable en agregado.
- **Ledger:** Cadena lineal (no blockDAG), salvo que el blockDAG sobreviva validación adversarial.
- **Red:** Capa de relay/mixnet obligatoria, con modos degradados explícitos.
- **Cliente:** Ruta de full node fuerte; ruta de light client solo si existe diseño no suicida (si no, lanzamiento inicial restringido a usuarios con infraestructura propia o comunitaria).
- **Pagos rápidos:** Capa superior limitada, inspiración eCash, exposición acotada.
- **Disclosure:** Solo pruebas esenciales: pago, recibo, liquidación de factura.
- **Unidad estable:** No incluida en lanzamiento mínimo. Se pospone hasta que exista diseño creíble.
- **Gobernanza:** Bounded, con kill criteria y downgrade paths; multi-implementación como objetivo, no como requisito de día uno.

---

## Qué queda dentro de la versión mínima

| Componente | Estado en mínima |
|------------|------------------|
| PoW como base de consenso | Dentro |
| Modelo de notas privadas con nullifiers | Dentro |
| Supply correctness auditable en agregado | Dentro |
| Privacidad de red obligatoria (relay/mixnet) | Dentro, con degraded modes explícitos |
| Cadena lineal como fallback si blockDAG falla | Dentro |
| Full node como anchor de verdad | Dentro |
| Wallet honesta (capas visibles, privacy mode visible) | Dentro |
| Pagos rápidos con exposición acotada | Dentro, si el diseño sobrevive |
| Disclosure: pago, recibo, factura | Dentro |
| Kill criteria y downgrade paths | Dentro |

---

## Qué queda fuera de la versión mínima

| Componente | Razón de exclusión |
|------------|-------------------|
| blockDAG | Solo si sobrevive validación; si no, lineal |
| Unidad estable | Mecanismo vacío; posponer hasta diseño creíble |
| Disclosure amplio (nómina, auditoría, reservas) | Reducir a esenciales primero; composición no validada |
| Cliente ligero móvil masivo | Bloqueante constitucional; si no hay ruta viable, lanzamiento restringido |
| Múltiples implementaciones desde día uno | Objetivo, no requisito mínimo; puede iniciarse con una |
| Gobernanza formal completa | Principios fijados; mecanismos pueden iterarse |

---

## Comparación con Monero

La arquitectura mínima honesta es estructuralmente cercana a una evolución de Monero:

| Aspecto | Monero actual | Mínima honesta |
|---------|---------------|----------------|
| Consenso | PoW lineal | PoW lineal (o blockDAG si viable) |
| Privacidad ledger | Ring signatures, etc. | Notas privadas + nullifiers (familia ZK) |
| Privacidad red | Opcional (Tor) | Obligatoria en diseño |
| Cliente ligero | Debilidades documentadas | Bloqueante; no lanzar si es suicida |
| UX wallet | Variable | Honestidad explícita (capas, privacy mode) |
| Pagos rápidos | No nativo | Capa superior limitada |
| Disclosure | Limitado | Selectivo, pruebas esenciales |
| Unidad estable | No | No en mínima |

**Conclusión:** El núcleo sólido se parece más a "Monero con mejor transporte, mejor wallet, disclosure acotado y capa de pagos rápidos" que a una teoría monetaria nueva y cerrada. Todo lo que está encima (blockDAG, stable unit, disclosure amplio, gobernanza multiimplementación) es ambición legítima pero no confirmada.

---

## Condiciones de lanzamiento mínimo

La versión mínima no debe lanzarse a menos que:

1. **Consenso:** Ordering determinístico, reorgs manejables, finality policy comprensible.
2. **Estado privado:** Conservación de valor verificable, nullifiers correctos, supply auditable.
3. **Cliente:** O bien existe ruta light client no suicida, o el lanzamiento se restringe explícitamente a usuarios con full node o infraestructura comunitaria.
4. **Red:** Relay/mixnet reduce inferencia de origen de forma material, o degraded mode se comunica con honestidad.
5. **Producto:** Usuario distingue capas, privacy mode y finality; no hay custodia oculta.

Si alguno falla, se aplica kill criterion o downgrade antes de lanzar.

---

## Lo que no es la versión mínima

La versión mínima **no** es:

- Una moneda total ya resuelta.
- Un sistema que promete todas las propiedades objetivo desde día uno.
- Una arquitectura que ignora los bloqueantes; los nombra y los respeta.
- Un whitepaper que vende ambición como realidad.

La versión mínima **es**:

- El menor sistema coherente con los invariantes que se intentaría construir si los bloqueantes se resuelven o se recorta alcance.
- Estructuralmente cercana a Monero endurecido: mejor transporte, mejor wallet, disclosure acotado.
- Un punto de partida desde el que crecer o desde el que reconocer límites.
