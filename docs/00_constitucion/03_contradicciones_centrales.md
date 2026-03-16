# Contradicciones centrales

## Propósito

Este documento expone sin suavizar las tensiones principales del corpus. Para cada contradicción se indica: qué se quiere, por qué choca, si hoy hay solución conocida, y qué parte es ingeniería vs. investigación abierta.

---

## 1. Anonimato fuerte vs. interoperabilidad legal

**Qué se quiere:** Privacidad por defecto y capacidad de operar en economía legal (nómina, facturación, auditoría, impuestos).

**Por qué choca:** La interoperabilidad legal históricamente se ha logrado mediante transparencia o identificación. Los reguladores y bancos esperan trazabilidad. El Travel Rule y FATF presionan hacia más visibilidad, no menos.

**Solución conocida hoy:** No. Lo que existe es disclosure selectivo como dirección (Penumbra), pero la composición de pruebas y la aceptación regulatoria real están abiertas.

**Ingeniería vs. investigación:** Parcialmente ingeniería (gramática de pruebas, UI de disclosure). Mayormente investigación (qué pruebas aceptan jurisdicciones, cómo evitar linkability acumulativa).

---

## 2. Privacidad fuerte vs. cliente ligero usable

**Qué se quiere:** Usuario móvil que no filtre su vida financiera al proveedor remoto, con experiencia usable (sincronización, batería, latencia).

**Por qué choca:** El descubrimiento de notas en un sistema privado requiere que el cliente obtenga datos. Si pide datos de forma identificable, filtra. Si pide todo y filtra localmente, el ancho de banda y la batería explotan. Los esquemas de consulta privada (PIR, etc.) son costosos o no escalan.

**Solución conocida hoy:** No. Monero documenta debilidades de wallets ligeras. Ningún sistema privado masivo ha resuelto esto de forma satisfactoria.

**Ingeniería vs. investigación:** Investigación abierta de primer orden. No es backlog de ingeniería; es problema sin solución demostrada.

---

## 3. PoW + blockDAG + transacciones privadas

**Qué se quiere:** Throughput paralelo (blockDAG), coste externo de ataque (PoW), y privacidad de montos y grafos (transacciones privadas).

**Por qué choca:** El blockDAG requiere ordering determinístico. Las transacciones privadas usan nullifiers como marcadores de conflicto. La interacción entre ordering paralelo, nullifiers, reorgs y verificación de pruebas ZK puede ser computacionalmente prohibitiva o lógicamente ambigua. Nadie ha implementado esta combinación de forma satisfactoria.

**Solución conocida hoy:** No. Es frontera de investigación. El documento lo trata como "decisión abierta" cuando en realidad es "problema abierto".

**Ingeniería vs. investigación:** Investigación. La verificación de pruebas sobre un DAG con ordering complejo no está modelada. El downgrade path (cadena lineal) es ingeniería conocida.

---

## 4. Unidad estable privada sin recentralización

**Qué se quiere:** Denominación estable para precios, nómina y comercio diario, sin custodio único, sin oráculo único, con privacidad.

**Por qué choca:** La estabilidad requiere mecanismo de anclaje (colateral, oráculo, gobernanza). El colateral debe valorarse. La valoración requiere datos. Los datos contradicen la privacidad. Las liquidaciones requieren ejecución visible. La auditoría de solvencia requiere visibilidad agregada que puede filtrar. MakerDAO/DAI funciona con transparencia total y aún así es frágil bajo estrés.

**Solución conocida hoy:** No. La experiencia con estables privados es limitada. Overcollateralización privada con oráculos mínimos no tiene diseño creíble publicado.

**Ingeniería vs. investigación:** Mayormente investigación. La filosofía de separación es correcta; el mecanismo está vacío.

---

## 5. Gobernanza sin élite operativa

**Qué se quiere:** Protocolo que evolucione (bugs, upgrades, emergencias) sin que una fundación, un equipo core o un comité de emergencia se convierta en soberano permanente.

**Por qué choca:** La coordinación requiere alguien que coordine. Las emergencias requieren respuesta rápida. El desarrollo de múltiples implementaciones requiere financiación. La financiación tiende a centralizarse. No existe mecanismo ampliamente probado de gobernanza descentralizada que no derive en oligarquía informal o parálisis.

**Solución conocida hoy:** No. El corpus fija principios (no monopolio, no poder permanente, no captura) pero no mecanismos. Cómo se financia la segunda implementación sin fundación no está respondido.

**Ingeniería vs. investigación:** Filosofía correcta; mecanismo abierto. Parcialmente ingeniería (conformance, test vectors), mayormente problema de coordinación social.

---

## 6. Resistencia a coerción estatal física

**Qué se quiere:** Sistema utilizable bajo presión regulatoria, delistings, bloqueos bancarios, censura de infraestructura.

**Por qué choca:** Un estado que tiene control físico sobre el usuario (dispositivo, ubicación, identidad) puede coercer independientemente del protocolo. La tecnología no derrota la coerción física. Solo puede elevar el costo de vigilancia masiva y censura económica.

**Solución conocida hoy:** Parcial. Se puede diseñar para supervivencia sin CEX, con mixnets, con resistencia a delisting. No se puede diseñar para inmunidad ante coerción física directa.

**Ingeniería vs. investigación:** Límite estructural. El corpus debería decirlo explícitamente: esta arquitectura no protege contra un estado que te tiene físicamente.

---

## Resumen de contradicciones

| Contradicción | Solución conocida | Parte ingeniería | Parte investigación |
|---------------|-------------------|------------------|---------------------|
| Anonimato vs. legalidad | No | Gramática de pruebas | Aceptación regulatoria, composición |
| Privacidad vs. light client | No | — | Problema abierto |
| PoW + DAG + privado | No | Fallback lineal | Ordering + ZK en DAG |
| Stable privado no centralizado | No | — | Mecanismo vacío |
| Gobernanza sin élite | No | Conformance | Financiación, coordinación |
| Resistencia a coerción física | Parcial | Supervivencia infra | Límite estructural |
