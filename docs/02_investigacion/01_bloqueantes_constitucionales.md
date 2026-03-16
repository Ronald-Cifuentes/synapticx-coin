# Bloqueantes constitucionales

## Propósito

Este documento lista solo los puntos que, si fallan, tumban la ambición fuerte del programa. Cada uno tiene asociado: pregunta, por qué importa, experimento, evidencia que cierra, evidencia que mata, simplificación si falla.

---

## B1. Cliente ligero privado viable

**Pregunta:** ¿Existe una ruta para que un usuario móvil descubra sus notas y verifique estado sin filtrar su vida financiera al proveedor remoto?

**Por qué importa:** Si no existe, la adopción masiva exige privacidad suicida o queda restringida a usuarios con full node. El objetivo de dinero privado civilmente útil se invalida.

**Experimento/prototipo:** Prototipo de light client que solicita datos a uno o más proveedores y mide qué puede inferir un proveedor malicioso sobre el grafo de actividad del usuario. Comparar con umbral aceptable (ej. no más de N% de transacciones correlacionables).

**Evidencia que cierra:** Un diseño donde, bajo modelo de adversario definido, el proveedor no puede reconstruir el grafo de actividad con confianza superior a X%. Métricas de ancho de banda y batería dentro de umbrales móviles aceptables.

**Evidencia que mata:** Demostración de que cualquier diseño práctico requiere que el cliente revele información que permite correlacionar >Y% de su actividad. O que el coste de ancho de banda/batería hace el cliente inusable en móvil.

**Simplificación si falla:** Restringir lanzamiento a usuarios con full node o infraestructura comunitaria. Abandonar ambición de adopción móvil masiva.

---

## B2. Supply correctness bajo privacidad fuerte

**Pregunta:** ¿Cómo se audita la emisión y conservación de valor sin exponer montos ni grafos, con garantías suficientes para detectar inflación?

**Por qué importa:** Sin auditabilidad agregada, el sistema no puede distinguir dinero sano de inflación oculta. Es requisito de integridad monetaria.

**Experimento/prototipo:** Construcción criptográfica que demuestre conservación de valor oculta + range validity + nullifiers + issuance compliance. Verificación por equipos independientes. Benchmarks de coste de verificación en full node.

**Evidencia que cierra:** Especificación formal verificada; implementación que pasa test vectors de conservación; auditoría independiente que confirma que la emisión agregada es derivable públicamente.

**Evidencia que mata:** Demostración de que no existe construcción que cumpla los requisitos sin revelar más de lo permitido. O que el coste de verificación es prohibitivo para full nodes ordinarios.

**Simplificación si falla:** No existe. Es kill criterion. Si supply correctness no es auditable, el programa de visión máxima se invalida.

---

## B3. Viabilidad del ordering / estado privado (blockDAG + privado)

**Pregunta:** ¿Un PoW blockDAG con transacciones privadas, ordering determinístico, nullifiers y reorgs puede implementarse con complejidad manejable y coste de verificación razonable?

**Por qué importa:** La combinación blockDAG + privado no está demostrada. Si es inviable, se pierde throughput paralelo; la base sigue con cadena lineal.

**Experimento/prototipo:** Prototipo de consenso blockDAG con transacciones privadas (nullifiers, commitments). Medir: tiempo de ordenación canónica, coste de verificación por bloque, ambigüedad en resolución de conflictos bajo minería paralela honesta.

**Evidencia que cierra:** Ordering determinístico reproducible por implementaciones independientes. Sin ambigüedad en conflictos de nullifiers. Coste de verificación dentro de umbral (ej. <Z ms por bloque en hardware commodity).

**Evidencia que mata:** Ordering no determinístico bajo condiciones normales. Conflictos de nullifiers ambiguos. Coste de verificación que centraliza la validación en pocos actores.

**Simplificación si falla:** Downgrade a cadena lineal PoW. Se preserva consenso y privacidad; se pierde paralelismo.

---

## B4. Privacidad de red usable

**Pregunta:** ¿Qué relay/mixnet reduce suficientemente la inferencia de origen sin destruir latencia, batería y experiencia móvil?

**Por qué importa:** Si la privacidad de red es inusable en móvil, los usuarios normalizarán modos degradados o abandonarán. El ledger privado sin transporte privado es incompleto.

**Experimento/prototipo:** Prototipo de relay/mixnet integrado con wallet móvil. Medir: reducción de inferencia de origen (vs. gossip plano), latencia percibida, consumo de batería, comportamiento bajo conectividad intermitente.

**Evidencia que cierra:** Reducción material de inferencia (ej. adversario con visibilidad parcial no puede identificar origen con confianza >X%). Latencia y batería dentro de umbrales aceptables para uso diario.

**Evidencia que mata:** La única forma de lograr privacidad material requiere latencia o batería que hace el sistema inusable en móvil para usuarios ordinarios.

**Simplificación si falla:** Modos degradados explícitos. Comunicar con honestidad cuándo la privacidad de red está debilitada. No fingir protección fuerte cuando no la hay.

---

## B5. Stable unit privada sin recentralización (si la visión la exige)

**Pregunta:** ¿Existe un diseño de unidad estable overcollateralizada que preserve privacidad, evite custodio único, minimice oráculos y siga siendo auditable en agregado?

**Por qué importa:** Si la visión máxima incluye estabilidad para comercio diario, este bloqueante la habilita. Si no se resuelve, la estabilidad se pospone.

**Experimento/prototipo:** Diseño formal de stable unit con: colateral privado, liquidaciones, redención, oráculos mínimos. Simulación de estrés (colapso de colateral, corrida de redención).

**Evidencia que cierra:** Diseño que sobrevive simulaciones de estrés sin recentralización. Auditoría de solvencia agregada sin exponer grafos. Sin custodio único como trust anchor.

**Evidencia que mata:** Cualquier diseño creíble requiere custodio único, oráculo central, o transparencia que contradice la privacidad.

**Simplificación si falla:** Posponer capa estable. Lanzar con base + pagos rápidos únicamente.
