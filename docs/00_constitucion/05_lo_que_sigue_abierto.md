# Lo que sigue abierto

## Propósito

Este documento lista los bloqueantes reales. No como backlog bonito, sino como preguntas abiertas de alta gravedad sin solución conocida. Cada ítem puede invalidar o recortar drásticamente la arquitectura.

---

## 1. Cliente ligero privado usable

**Pregunta:** ¿Existe una ruta para que un usuario móvil descubra sus notas y verifique estado sin filtrar su vida financiera al proveedor remoto?

**Gravedad:** Constitucional. Si no existe, la adopción masiva requiere privacidad suicida o exclusión de usuarios móviles.

**Estado:** Problema abierto. Monero documenta debilidades. Ningún sistema privado ha resuelto esto de forma satisfactoria. Los esquemas de consulta privada (PIR, etc.) son costosos o no escalan en este contexto.

**No es:** Un ítem de backlog de ingeniería. Es investigación de primer orden.

---

## 2. Supply correctness bajo privacidad fuerte

**Pregunta:** ¿Cómo se audita la emisión y la conservación de valor sin exponer montos ni grafos, con garantías suficientes para detectar inflación?

**Gravedad:** Constitucional. Sin auditabilidad agregada, el sistema no puede distinguir dinero sano de inflación oculta.

**Estado:** Requiere un sistema de pruebas ZK específico: conservación oculta + range validity + nullifiers + issuance compliance. No es "elegir familia ZK"; es diseñar y demostrar una construcción adaptada a esta arquitectura. Investigación de criptografía aplicada de primera línea.

**No es:** Una caja a marcar en un backlog. Es bloqueante criptográfico.

---

## 3. Viabilidad real de blockDAG privado

**Pregunta:** ¿Un PoW blockDAG con transacciones privadas, ordering determinístico, nullifiers y reorgs puede implementarse con complejidad manejable y coste de verificación razonable?

**Gravedad:** Estructural. Si falla, se degrada a cadena lineal (downgrade path existe, pero se pierde throughput paralelo).

**Estado:** Nadie ha implementado esta combinación de forma satisfactoria. La interacción entre ordering paralelo, nullifiers, reorgs y verificación ZK no está modelada completamente. Puede ser computacionalmente prohibitiva.

**No es:** "Decisión abierta de ingeniería". Es frontera de investigación.

---

## 4. Red de transporte privada usable en móvil

**Pregunta:** ¿Qué relay/mixnet reduce suficientemente la inferencia de origen sin destruir latencia, batería y experiencia móvil?

**Gravedad:** Operacional. Si la privacidad de red es inusable en móvil, los usuarios normalizarán modos degradados o la abandonarán.

**Estado:** Trade-off no resuelto. Los mixnets añaden latencia. El móvil tiene restricciones de batería y conectividad intermitente. Existe degraded mode como fallback, pero no hay diseño que equilibre bien ambos.

**No es:** Solo configuración. Es diseño de protocolo bajo restricciones duras.

---

## 5. Stable unit privada no custodial creíble

**Pregunta:** ¿Existe un diseño de unidad estable overcollateralizada que preserve privacidad, evite custodio único, minimice oráculos y siga siendo auditable en agregado?

**Gravedad:** Económica. Sin esto, la arquitectura puede lanzar con base + fast payments, pero no con estabilidad para comercio diario.

**Estado:** Mecanismo vacío. La filosofía (overcollateralización, separación, liquidaciones explícitas) es correcta. La implementación concreta no existe. MakerDAO/DAI funciona con transparencia total y es frágil bajo estrés. Hacerlo privado multiplica la dificultad.

**No es:** "Elegir modelo de colateral". Es investigación de diseño económico y criptográfico.

---

## 6. Gobernanza multiimplementación no capturada

**Pregunta:** ¿Cómo se financia y coordina el desarrollo de múltiples implementaciones independientes sin crear una fundación que se convierta en centro de poder?

**Gravedad:** Política. La gobernanza descentralizada de protocolo es uno de los problemas más difíciles. El corpus fija principios pero no mecanismos.

**Estado:** Sin respuesta. Cómo se paga la segunda implementación, cómo se coordina un fork de emergencia sin centralizar temporalmente, cómo se distingue pluralidad real de cosmética (mismo equipo, distintos nombres) no está definido.

**No es:** "Definir proceso de propuestas". Es problema de coordinación y financiación descentralizada.

---

## 7. Disclosure composition safety

**Pregunta:** ¿Las pruebas estrechas pueden usarse en flujos comerciales y legales sin que la composición de varias pruebas reconstruya el grafo financiero completo del usuario?

**Gravedad:** Legal/interoperabilidad. Si cada prueba es estrecha pero su combinación es amplia, el disclosure selectivo colapsa.

**Estado:** No modelado completamente. Existe dirección (time-scope, audience-scope, granularidad mínima) pero no análisis formal de composición.

**Downgrade path:** Reducir tipos de prueba a los esenciales (pago, recibo, liquidación de factura).

---

## 8. Orden de resolución y dependencias

**Pregunta crítica no formulada explícitamente en el corpus:** ¿Existe algún equipo, financiamiento y horizonte temporal que pueda resolver los bloqueantes 1–7 sin que la solución de uno invalide las decisiones ya tomadas en otros?

**Estado:** No respondida. Las dependencias son complejas: blockDAG puede romper light clients; light clients pueden debilitar privacidad de red; privacidad de red puede degradar UX móvil; disclosure usable puede abrir compositional leakage; stable unit operable puede recentralizar.

**Implicación:** El orden de investigación (settlement soundness → light client → network privacy → consensus geometry → product → disclosure → stable → governance) es una hipótesis de secuencia, no una garantía de cruzabilidad.
