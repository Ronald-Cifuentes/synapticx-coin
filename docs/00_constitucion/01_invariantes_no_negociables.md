# Invariantes no negociables

## Propósito

Este documento lista las reglas duras del sistema. Cada punto justifica por qué sigue siendo válido aunque cambie el resto del diseño. Ningún invariante depende de que una investigación futura tenga éxito.

---

## 1. Privacidad por defecto

**Regla:** La capa base debe ser privada por defecto. No existe modo transparente coexistente.

**Justificación:** Si la privacidad es opcional, el conjunto de anonimato se fragmenta y la fungibilidad se degrada. Los usuarios en modo transparente se convierten en outliers identificables. La decisión no depende de tecnología futura; es una restricción de diseño que se mantiene aunque cambie el mecanismo de privacidad (ZK, ring signatures, etc.).

---

## 2. No soberanía PoS / dPoS / BFT visible en la capa base

**Regla:** El consenso de la capa base no puede derivar su autoridad de stake, validadores visibles o comités BFT.

**Justificación:** PoS, dPoS y BFT con validadores visibles convierten capital previo y visibilidad institucional en poder de consenso. Son más fáciles de capturar regulatoria y políticamente. Esta decisión es estructural, no técnica: el objetivo es resistencia a captura, y el mecanismo de stake es incompatible con ese objetivo en la capa base. Se mantiene aunque mejore la eficiencia de PoS.

---

## 3. Separación base / unidad estable

**Regla:** La estabilidad diaria no puede exigir contaminar la base con custodios, oráculos centrales o transparencia universal.

**Regla complementaria:** La base no será forzada a ser unidad estable final.

**Justificación:** Mezclar soberanía y estabilidad en una sola capa crea un punto único de fallo y captura. La separación preserva que el activo base pueda sobrevivir aunque la capa estable falle. Esta decisión es conceptual; no depende de que la unidad estable esté resuelta.

---

## 4. Supply correctness auditable en agregado

**Regla:** El suministro total debe poder auditarse con garantías suficientes para descartar inflación accidental o maliciosa, sin exponer la vida financiera de los usuarios.

**Justificación:** Sin auditabilidad agregada, el sistema no puede distinguir dinero sano de inflación oculta. La regla es invariante aunque el mecanismo de prueba (ZK, rangeproofs, etc.) siga abierto. Si no se puede auditar, el diseño falla constitucionalmente.

---

## 5. Privacidad de red no opcional

**Regla:** La capa base debe asumir mixnet, relay privacy o un sistema equivalente. No se acepta "usa Tor por tu cuenta" como diseño suficiente.

**Justificación:** La privacidad del ledger es insuficiente si el transporte filtra IP, timing y patrones. La privacidad de red es parte del modelo de amenazas, no una práctica opcional del usuario. Se mantiene aunque el mecanismo concreto (mixnet, Dandelion, etc.) varíe.

---

## 6. Disclosure acotado en vez de transparencia total

**Regla:** La interoperabilidad legal debe lograrse mediante divulgación selectiva y acotada, no mediante transparencia universal.

**Justificación:** Si la única forma de usar el sistema en contextos legales es abrir toda la historia financiera, el objetivo de privacidad civil se invalida. La regla es que el diseño debe soportar pruebas estrechas (pago, recepción, solvencia parcial) sin exigir panóptico.

---

## 7. Rechazo de custodios en la base

**Regla:** El sistema no puede exigir confiar en custodios para la validez del settlement en la capa base.

**Justificación:** La custodia reintroduce el punto único de fallo y captura que el diseño intenta evitar. La validez del gasto no puede depender de un tercero. Se mantiene aunque existan capas superiores con modelos custodiales acotados (ej. eCash con exposición limitada).

---

## 8. Clientes ligeros no suicidas

**Regla:** No se acepta un modelo donde la wallet móvil promedio filtre media vida financiera al nodo remoto.

**Justificación:** Si el camino de adopción masiva requiere que el usuario entregue su grafo de actividad a un proveedor, el sistema ha fallado su propósito. La regla es invariante; el mecanismo para cumplirla puede ser bloqueante de investigación.

---

## 9. Divulgación selectiva como capacidad, no como defecto

**Regla:** El sistema debe permitir demostrar lo necesario y nada más: pago, recepción, solvencia parcial, prueba contable puntual, cumplimiento acotado.

**Justificación:** La economía legal mínima requiere pruebas. La alternativa a disclosure acotado es transparencia total. La regla exige que exista un camino intermedio; no que esté ya implementado.

---

## 10. Supervivencia bajo hostilidad regulatoria

**Regla:** La arquitectura debe seguir siendo utilizable aunque haya delistings, presión AML, bloqueos bancarios o censura de infraestructura.

**Justificación:** El diseño asume adversarios con capacidad regulatoria. No promete inmunidad, pero la arquitectura no debe depender existencialmente de CEX, bancos cooperativos o infraestructura no censurable. Es una restricción de diseño, no una garantía de resultado.
