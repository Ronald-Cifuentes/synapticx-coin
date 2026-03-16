# Pagos rápidos y capa de uso diario

## Estado epistemológico del capítulo

- **Cerrado:** La capa de pagos rápidos es separada del settlement soberano. No puede confundirse con la base. Inspiración eCash/Cashu/Fedimint, pero con límites de exposición y confianza.
- **Abierto:** Mecanismo concreto (federado, note-locked, bounded-trust). Límites numéricos de exposición. Integración con wallet y merchant.
- **Qué lo mataría:** Que los pagos rápidos se conviertan en dependencia oculta del settlement; que la capa sea capturable y termine contaminando el diseño entero.

---

## 1. Separación de la base soberana

[CONVICCIÓN ESTRUCTURAL] Los pagos rápidos viven en una capa superior. El settlement soberano es la base. La capa de pagos rápidos no es, ni puede presentarse como, el núcleo de validez.

[DESCARTADO] eCash tipo Cashu/Fedimint como núcleo soberano. Cashu admite que el mint custodia el bitcoin subyacente y puede ver la IP. Fedimint admite riesgo custodial, de debasement y regulatorio. Sirven como inspiración para UX; no como base.

---

## 2. Propiedades deseadas

[HIPÓTESIS DE DISEÑO] Una capa de pagos rápidos separada puede mejorar UX sin romper soberanía, si cumple:

- Pagos casi instantáneos para montos pequeños y medianos.
- UX simple, nombres legibles, soporte móvil.
- Top-up y cash-out desde la base.
- Límites de exposición y duración.

---

## 3. Límites de exposición y confianza

[CONVICCIÓN ESTRUCTURAL] La capa de pagos rápidos debe tener:

- **Límite de exposición:** Cuánto valor puede estar en riesgo si la capa falla o es capturada.
- **Límite temporal:** Ventanas de uso; no exposición indefinida.
- **Bounded trust:** La confianza no puede ser ilimitada. Si la capa es federada, el número y la naturaleza de los federadores deben ser acotados.

[KILL CRITERION] Si esta capa termina siendo indispensable para usar el sistema y además es capturable, entonces contaminó el diseño entero.

---

## 4. Prohibido confundir con settlement

[CONVICCIÓN ESTRUCTURAL] El usuario no debe poder confundir:

- Un pago en la capa rápida (reversible, con confianza acotada).
- Un settlement en la base (irreversible, sin custodia).

La wallet debe distinguir claramente entre capas. El producto no puede ocultar esta diferencia por conveniencia.

---

## 5. Resumen de etiquetas

| Componente | Etiqueta |
|------------|----------|
| Separación base / pagos rápidos | [CONVICCIÓN ESTRUCTURAL] |
| eCash como base | [DESCARTADO] |
| Capa rápida mejora UX | [HIPÓTESIS DE DISEÑO] |
| Límites de exposición y confianza | [CONVICCIÓN ESTRUCTURAL] |
| Captura de capa rápida | [KILL CRITERION] |
