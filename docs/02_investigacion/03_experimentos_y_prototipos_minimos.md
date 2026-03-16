# Experimentos y prototipos mínimos

## Propósito

Para cada hipótesis o bloqueante: prototipo mínimo, métrica, criterio de éxito, criterio de fracaso. Nada genérico.

---

## B1. Cliente ligero privado

| Campo | Contenido |
|-------|-----------|
| **Prototipo mínimo** | Light client que pide lotes de note commitments a 1–3 proveedores; descifra localmente. Simulador de proveedor adversario que registra patrones de solicitud. |
| **Métrica** | % de transacciones del usuario que el adversario puede correlacionar con confianza >80%. Ancho de banda por sync completo. % batería consumida en 24h de uso típico. |
| **Criterio de éxito** | Correlación ≤10%. BW ≤500 MB/sync. Batería ≤5%/día en uso pasivo. |
| **Criterio de fracaso** | Correlación >50%. O BW >2 GB/sync. O batería >15%/día. |

---

## B2. Supply correctness

| Campo | Contenido |
|-------|-----------|
| **Prototipo mínimo** | Circuito ZK que prueba conservación + range + nullifiers + issuance. Test vectors con inflación maliciosa que debe ser rechazada. Implementación de auditoría agregada. |
| **Métrica** | Auditor independiente puede derivar emisión total en <1h. Coste de verificación por tx en ms. |
| **Criterio de éxito** | Auditoría reproducible. Verificación <100 ms/tx en hardware commodity. |
| **Criterio de fracaso** | No existe construcción que cumpla sin revelar grafos. O verificación >500 ms/tx. |

---

## B3. blockDAG + estado privado

| Campo | Contenido |
|-------|-----------|
| **Prototipo mínimo** | Consenso blockDAG con 4+ mineros paralelos. Transacciones con nullifiers. 10k bloques con conflictos simulados. Dos implementaciones independientes. |
| **Métrica** | ¿Ambas implementaciones producen el mismo ordering canónico? Tiempo de ordenación por bloque. Ambiguidad en conflictos (debe ser 0). |
| **Criterio de éxito** | Ordering idéntico. Sin ambigüedad. <50 ms ordenación/bloque. |
| **Criterio de fracaso** | Divergencia en ordering. Conflictos no resolubles. >200 ms/bloque. |

---

## B4. Privacidad de red usable

| Campo | Contenido |
|-------|-----------|
| **Prototipo mínimo** | Relay staging (Dandelion-like o mixnet simplificado) integrado con wallet. 100 nodos, 10% adversarios. Medición de inferencia de origen. |
| **Métrica** | Probabilidad de que adversario identifique origen correcto. Latencia p50 y p99. Batería móvil en 1h de uso. |
| **Criterio de éxito** | Inferencia ≤30% (vs. ~90% en gossip plano). Latencia p99 <30 s. Batería <3%/h. |
| **Criterio de fracaso** | Inferencia >60%. Latencia p99 >2 min. Batería >8%/h. |

---

## B5. Stable unit privada

| Campo | Contenido |
|-------|-----------|
| **Prototipo mínimo** | Diseño formal + simulador. Colapso de colateral 50% en 24h. Corrida de redención 80% del supply. |
| **Métrica** | ¿Sobrevive sin custodio único? ¿Solvencia auditable en agregado? |
| **Criterio de éxito** | Diseño que sobrevive estrés sin recentralización. Auditoría agregada posible. |
| **Criterio de fracaso** | Todo diseño creíble requiere custodio único u oráculo central. |

---

## H3. Disclosure composition

| Campo | Contenido |
|-------|-----------|
| **Prototipo mínimo** | Modelo formal de 5 tipos de prueba. Simulación: usuario genera 20 pruebas en 1 año. ¿Cuánto del grafo puede inferir un adversario? |
| **Métrica** | % del grafo reconstruible con N pruebas de tipos X, Y, Z. |
| **Criterio de éxito** | ≤20% del grafo con combinaciones típicas. |
| **Criterio de fracaso** | >60% del grafo con 10+ pruebas comunes. |

---

## H4. Capa de pagos rápidos

| Campo | Contenido |
|-------|-----------|
| **Prototipo mínimo** | Prototipo de capa con límite de exposición (ej. 1000 unidades máx). Fallo simulado: ¿la base sigue intacta? |
| **Métrica** | ¿El usuario distingue settlement de pago rápido en test de usabilidad? Blast radius si la capa falla. |
| **Criterio de éxito** | 80% de usuarios distinguen correctamente. Base no afectada por fallo de capa. |
| **Criterio de fracaso** | <50% distinguen. Base depende de capa para operación normal. |
