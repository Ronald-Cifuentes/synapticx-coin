# Taxonomía epistemológica obligatoria

## Propósito

Este documento define las etiquetas con las que debe clasificarse toda afirmación relevante del corpus. La taxonomía existe para evitar que hipótesis se presenten como soluciones cerradas, que problemas abiertos se disfracen de backlog de ingeniería, o que contradicciones se oculten bajo redacción ambigua.

## Definición de cada etiqueta

### [CONVICCIÓN ESTRUCTURAL]

**Definición:** Regla dura del sistema. No depende de que una investigación futura "salga bien". Es una decisión de diseño que se mantiene aunque cambie el resto de la arquitectura.

**Uso:** Aplicar cuando la afirmación es consecuencia directa de los objetivos no negociables y no requiere resolver ningún problema abierto para ser válida.

**Ejemplos:**
- "La base no usará PoS ni validadores visibles como soberanía."
- "La privacidad de red es obligatoria, no opcional."

---

### [HIPÓTESIS DE DISEÑO]

**Definición:** Dirección razonable, pero todavía no demostrada. Es una apuesta de diseño que puede fallar sin invalidar los invariantes, pero cuya falla obliga a recortar ambición o cambiar ruta.

**Uso:** Aplicar cuando la afirmación es plausible y coherente con el resto, pero depende de trabajo técnico o de investigación que aún no está cerrado.

**Ejemplos:**
- "PoW es la piedra angular menos mala para este objetivo."
- "Una capa de pagos rápidos separada puede mejorar UX sin romper soberanía."

---

### [BLOQUEANTE DE INVESTIGACIÓN]

**Definición:** Problema abierto cuyo fracaso invalida o recorta la arquitectura. No es un ítem de backlog; es una pregunta de investigación de alta gravedad sin solución conocida.

**Uso:** Aplicar cuando el fracaso del problema obliga a matar el proyecto, posponer capas enteras o simplificar drásticamente.

**Ejemplos:**
- "Cliente ligero privado usable sin filtración catastrófica."
- "Supply correctness auditable bajo privacidad fuerte."

---

### [DESCARTADO]

**Definición:** Enfoque rechazado por razones estructurales. No es una preferencia; es una exclusión justificada.

**Uso:** Aplicar cuando el corpus rechaza explícitamente un camino de diseño y explica por qué.

**Ejemplos:**
- "PoS, dPoS y BFT visible para la capa base."
- "Privacidad opcional."
- "Custodios en la capa base."

---

### [DOWNGRADE PATH]

**Definición:** Ruta de simplificación si la hipótesis falla. Es el plan B explícito cuando una pieza ambiciosa no sobrevive validación.

**Uso:** Aplicar cuando existe una ruta de recorte documentada que preserva invariantes aunque reduzca alcance.

**Ejemplos:**
- "Si blockDAG falla: downgrade a cadena lineal PoW."
- "Si la unidad estable centraliza: posponer capa estable."

---

### [KILL CRITERION]

**Definición:** Condición que obliga a detener o reiniciar una parte del proyecto. No es una recomendación; es un gatillo de aborto.

**Uso:** Aplicar cuando la arquitectura declara explícitamente que bajo cierta condición el diseño debe considerarse inválido.

**Ejemplos:**
- "Si el cliente ligero requiere filtración catastrófica: fallo constitucional."
- "Si supply correctness no es auditable: fallo constitucional."

---

## Prohibiciones de redacción

1. **No vender hipótesis como soluciones cerradas.** Una hipótesis de diseño debe etiquetarse como tal, no como "diseño elegido" sin matiz.

2. **No llamar "pendiente de ingeniería" a investigación abierta.** Si no existe solución conocida, es bloqueante de investigación.

3. **No ocultar contradicciones.** Las tensiones deben enumerarse explícitamente en documentos dedicados.

4. **No presentar como implementable lo que depende de un problema abierto no resuelto.** La implementabilidad requiere que los bloqueantes estén cerrados o tengan downgrade path aceptado.

5. **No usar lenguaje promocional o grandilocuente.** El corpus debe redactarse en español técnico sobrio.

6. **No borrar ideas útiles; reclasificarlas con dureza.** Una idea descartada para un propósito puede ser útil como referencia o como límite; no se elimina, se etiqueta.

---

## Flujo de aplicación

1. Para cada afirmación relevante del corpus: identificar a qué categoría pertenece.
2. Si hay duda entre CONVICCIÓN e HIPÓTESIS: inclinar hacia HIPÓTESIS.
3. Si hay duda entre HIPÓTESIS y BLOQUEANTE: inclinar hacia BLOQUEANTE.
4. Verificar que cada BLOQUEANTE tenga asociado un KILL CRITERION o DOWNGRADE PATH explícito.
