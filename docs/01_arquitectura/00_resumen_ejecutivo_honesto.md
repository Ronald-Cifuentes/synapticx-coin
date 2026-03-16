# Resumen ejecutivo honesto

## Advertencia inicial

Este documento **no** describe una arquitectura implementable cerrada. Describe un **marco conceptual** con partes sólidas, hipótesis de diseño y bloqueantes de investigación. La capa mínima viable es mucho más austera que la visión máxima.

---

## Los tres bloqueantes más severos

Antes de cualquier detalle, estos tres problemas pueden invalidar o recortar drásticamente el proyecto:

1. **Cliente ligero privado usable.** Si no existe una ruta para que un usuario móvil descubra sus notas y verifique estado sin filtrar su vida financiera al proveedor, la adopción masiva exige privacidad suicida o queda restringida a usuarios con full node.

2. **Supply correctness bajo privacidad fuerte.** Si no se puede auditar la emisión y conservación de valor sin exponer montos ni grafos, el sistema no puede distinguir dinero sano de inflación oculta. No es "elegir familia ZK"; es diseñar una construcción criptográfica específica.

3. **PoW + blockDAG + transacciones privadas.** La combinación de ledger paralelo, ordering determinístico, nullifiers y verificación ZK no está demostrada viable. Nadie la ha implementado de forma satisfactoria. Puede ser computacionalmente prohibitiva o lógicamente ambigua.

---

## Qué es este corpus

- **Convicciones estructurales:** Reglas duras que no dependen de investigación futura (privacidad por defecto, no PoS en base, separación base/estable, supply auditable, privacidad de red obligatoria, disclosure acotado, no custodios).

- **Hipótesis de diseño:** Direcciones razonables pero no demostradas (PoW como base, capa de pagos rápidos separada, disclosure selectivo para comercio, wallet honesta).

- **Bloqueantes de investigación:** Problemas abiertos cuyo fracaso invalida o recorta la arquitectura (cliente ligero, supply correctness, blockDAG privado, unidad estable no custodial, gobernanza multiimplementación).

---

## Visión mínima vs. visión máxima

| Aspecto | Mínima viable | Ambiciosa |
|---------|---------------|-----------|
| Ledger | Cadena lineal PoW | blockDAG PoW |
| Cliente | Full node o light client solo si no suicida | Light client móvil masivo |
| Unidad estable | No incluida | Overcollateralizada privada |
| Disclosure | Pago, recibo, factura | Nómina, auditoría, reservas |
| Gobernanza | Principios, una implementación | Multi-implementación, mecanismos formales |

---

## Prioridad

La versión mínima (Monero endurecido) es más visible y defendible que la versión máxima. La máxima es aspiracional; la mínima es el techo si los bloqueantes no se cierran.

---

## Referencia

- Taxonomía: `docs/00_constitucion/00_taxonomia_epistemologica.md`
- Invariantes: `docs/00_constitucion/01_invariantes_no_negociables.md`
- Versión mínima: `docs/00_constitucion/06_arquitectura_minima_honesta.md`
