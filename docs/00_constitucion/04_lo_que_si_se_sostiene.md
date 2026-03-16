# Lo que sí se sostiene

## Propósito

Este documento enumera las partes del corpus que siguen siendo defendibles tras la auditoría epistemológica. Incluye las secciones obligatorias sobre PoS y separación base/estable.

---

## 1. Estructura de invariantes

La estructura de invariantes no negociables es sólida y honesta. Las reglas duras (privacidad por defecto, no PoS en base, separación base/estable, supply correctness auditable, privacidad de red obligatoria, disclosure acotado, rechazo de custodios) son coherentes entre sí y con el objetivo declarado. No dependen de investigación futura para ser válidas como restricciones de diseño.

---

## 2. Por qué PoS sigue descartado para la capa base de este objetivo

**Afirmación defendible:** Para un sistema cuyo objetivo prioritario es resistencia a captura política y oligárquica, PoS, dPoS y BFT con validadores visibles son estructuralmente malos como núcleo de soberanía.

**Razones:**

1. **Conversión de capital en poder:** El stake convierte la tenencia previa del activo en autoridad de consenso. Quien tiene más, decide más. Eso es lo opuesto a "resistencia a captura por riqueza".

2. **Visibilidad institucional:** Los validadores en PoS/dPoS son identificables. Pueden ser regulados, demandados, presionados. Un estado o cartel puede concentrar presión sobre un conjunto pequeño de actores visibles.

3. **Custodios como amplificadores:** El staking delegado concentra poder en custodios y exchanges. La captura se traslada a quien custodia el stake, no desaparece.

4. **No es preferencia estética:** La decisión no se basa en que PoS sea "menos puro". Se basa en que para el objetivo concreto (dinero privado resistente a captura), PoS alinea incentivos en la dirección equivocada.

**Lo que no se afirma:** Que PoS sea inútil en otros contextos. IOTA Rebased, Penumbra y otros pueden ser válidos para otros objetivos. Para esta arquitectura, el descarte es correcto.

---

## 3. Por qué la separación base / estable sigue siendo correcta aunque la unidad estable siga abierta

**Afirmación defendible:** La estabilidad diaria no puede contaminar la base con custodios, oráculos centrales o transparencia universal. La base no será forzada a ser unidad estable final.

**Razones:**

1. **Punto único de fallo:** Si la base y la estabilidad están fusionadas, un fallo de la lógica estable (depeg, colapso de colateral, captura de oráculo) compromete la validez del settlement. La separación aísla el blast radius.

2. **Contradicción de requisitos:** La base prioriza privacidad, soberanía y resistencia a captura. La estabilidad prioriza anclaje de precio, lo que suele requerir colateral valorado, oráculos, liquidaciones. Mezclar ambos en una capa crea tensiones irresolubles.

3. **Independencia de mecanismo:** La corrección de la separación no depende de que exista un diseño concreto de unidad estable. Es una decisión arquitectónica: la base es settlement y soberanía; la estabilidad es capa superior con fronteras duras.

4. **Fallback explícito:** Si la unidad estable no puede construirse sin recentralización, se pospone. La base sobrevive. Eso confirma que la separación es correcta: permite fallar la capa superior sin matar la base.

**Lo que no se afirma:** Que la unidad estable esté resuelta. El mecanismo (overcollateralización privada, oráculos, liquidaciones) sigue abierto. La separación es correcta; la implementación de la capa estable no.

---

## 4. Modelo de amenazas

El modelo de amenazas identifica adversarios (estado, exchange, ISP, analista de cadena, cartel de pools, proveedor móvil, atacante físico), amenazas técnicas (double spend, eclipse, spy nodes, timing correlation, mempool leakage, inflation bug) y amenazas políticas (Travel Rule, criminalización, presión sobre custodios). No promete inmunidad; define contra qué se defiende el diseño.

---

## 5. Kill criteria y downgrade paths

Los kill criteria y downgrade paths obligan a definir condiciones de aborto antes de invertir en implementación. Pocos proyectos similares los incluyen. Ejemplos: si el cliente ligero requiere filtración catastrófica, fallo constitucional; si blockDAG es inmanejable, downgrade a lineal. Esta disciplina reduce el autoengaño.

---

## 6. Privacidad de red como capa arquitectónica

El reconocimiento de que la privacidad de red no es opcional sino arquitectónica está bien posicionado. El ledger privado sin transporte privado deja al usuario operativamente transparente. La decisión de que mixnet/relay sea obligatorio, no "usa Tor por tu cuenta", es correcta.

---

## 7. Descarte de eCash como núcleo soberano

Cashu y Fedimint sirven como inspiración para UX de pagos, pero sus propios documentos admiten que el mint custodia fondos y puede observar metadatos. Usarlos como núcleo soberano reintroduciría custodia y visibilidad. El descarte es correcto; la inspiración para capa de pagos rápidos separada también.

---

## 8. Disclosure selectivo como dirección

La dirección de disclosure selectivo (pruebas estrechas, acotadas en tiempo, audiencia y propósito) es coherente con el objetivo. No está resuelta la composición ni la aceptación regulatoria, pero la dirección conceptual es correcta: no transparencia total para legalidad, sino pruebas mínimas necesarias.

---

## 9. Rechazo de narrativas falsas

El corpus rechaza correctamente: "el base coin se estabilizará solo", "algoritmo reflexivo solo resuelve estabilidad", "reserva centralizada es suficiente", "estabilidad mágica y trustless a la vez". Esas narrativas son indefendibles y el corpus no las adopta.

---

## 10. Orden de prioridades

El orden de investigación (private settlement soundness → light client viability → network privacy → consensus geometry → product honesty → disclosure → stable unit → governance) es razonable. La base debe existir antes de que las capas superiores tengan sentido. No paralelizar todo es correcto.
