# Hipótesis de diseño a validar

## Propósito

Este documento lista hipótesis fuertes, no invariantes. Son direcciones de diseño que deben demostrarse viables antes de tratarlas como cerradas.

---

## H1. PoW como base provisional

**Hipótesis:** PoW es la piedra angular menos mala para un sistema que prioriza resistencia a captura sobre eficiencia. El descarte de PoS deja PoW como opción que ancla el coste de ataque a recurso externo.

**Qué validar:** Que el coste de captura de consenso bajo PoW (memory-hard, commodity-accessible) permanezca alto suficiente durante ventana de participación abierta. Que la concentración de minería no sea inevitablemente oligárquica en horizonte relevante.

**No es invariante porque:** Podría existir un mecanismo alternativo no considerado. La hipótesis es fuerte por descarte, no por demostración positiva.

---

## H2. blockDAG como mejora de geometría

**Hipótesis:** Un blockDAG con ordering determinístico permitiría mayor throughput que una cadena lineal, sin sacrificar seguridad ni privacidad. La complejidad es por validar; no está demostrada manejable.

**Qué validar:** Que el ordering sea determinístico, que los conflictos de nullifiers se resuelvan sin ambigüedad, que el coste de verificación sea manejable. Ver bloqueante B3.

**No es invariante porque:** Tiene downgrade path (cadena lineal). La geometría DAG es mejora, no requisito constitucional.

---

## H3. Disclosure acotado como puente con comercio

**Hipótesis:** Las pruebas estrechas (pago, recibo, factura) pueden servir para operación empresarial y legal sin requerir transparencia total.

**Bloqueante asociado:** La composición de múltiples pruebas puede reconstruir el grafo completo. Eso es [BLOQUEANTE DE INVESTIGACIÓN]; si la composición es leaky, el disclosure selectivo colapsa.

**Qué validar:** Análisis formal de composición. Que N pruebas de tipo X no permitan inferir más de M% del grafo. Que contrapartes (bancos, auditores) acepten pruebas en contextos reales.

**No es invariante porque:** La composición puede ser leaky. Si lo es, se reduce el conjunto de pruebas (downgrade).

---

## H4. Capa de pagos rápidos separada

**Hipótesis:** Una capa superior con exposición acotada (inspiración eCash) puede mejorar UX de pagos diarios sin contaminar la base soberana. El usuario puede distinguir settlement de pago rápido.

**Qué validar:** Que la capa tenga límites de exposición y confianza definidos. Que su fallo no comprometa la base. Que la UX no confunda capas.

**No es invariante porque:** La capa podría ser capturable o indispensable de forma que contamine el diseño. Si ocurre, la capa se recorta o se elimina.

---

## H5. Wallet honesta reduce traición por producto

**Hipótesis:** Una interfaz que hace visibles capas, privacy mode y finality puede evitar que la conveniencia silencie la custodia o la filtración de metadatos.

**Qué validar:** Tests de usabilidad donde usuarios distinguen correctamente en qué capa operan, cuándo están en modo degradado, y qué confían. Que la ruta más fácil no sea la custodial.

**No es invariante porque:** Es problema de producto. La presión de conveniencia puede erosionar el diseño a pesar de la UI.

---

## H6. Memory-hard PoW retrasa oligopolio

**Hipótesis:** Un PoW memory-hard, accesible a hardware commodity, retrasa y diluye la concentración en ASICs y pools respecto a un PoW compute-dominant.

**Qué validar:** Modelado de ventana de participación abierta. Comparación con ASIC-first. Que la ventana sea suficiente para legitimidad del lanzamiento.

**No es invariante porque:** La especialización puede llegar igual; la hipótesis es que llega más tarde y más diluida.
