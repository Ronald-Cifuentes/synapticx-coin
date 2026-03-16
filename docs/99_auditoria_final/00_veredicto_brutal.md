# Veredicto brutal

## Qué sí quedó firme

- **Invariantes:** Privacidad por defecto, no PoS en base, separación base/estable, supply auditable (como requisito), privacidad de red obligatoria, disclosure acotado, no custodios. Son restricciones de diseño coherentes.
- **Descarte de PoS:** Justificado para el objetivo de resistencia a captura. No es preferencia estética.
- **Separación base/estable:** Correcta como decisión arquitectónica. No depende de que la unidad estable esté resuelta.
- **Kill criteria y downgrade paths:** Documentados. Obligan a condiciones de aborto explícitas.
- **Modelo de amenazas:** Identifica adversarios y amenazas sin prometer inmunidad.
- **Taxonomía epistemológica:** Aplicada. Distingue convicciones, hipótesis y bloqueantes.

---

## Qué sigue siendo investigación abierta

- **Cliente ligero privado usable.** Sin solución conocida. Monero documenta debilidades. Ningún sistema privado masivo lo ha resuelto.
- **Supply correctness bajo privacidad fuerte.** Requiere construcción criptográfica específica. No es "elegir familia ZK".
- **PoW + blockDAG + transacciones privadas.** Nadie lo ha implementado de forma satisfactoria. Puede ser prohibitivo o ambiguo.
- **Privacidad de red usable en móvil.** Trade-off no resuelto.
- **Unidad estable privada sin recentralización.** Mecanismo vacío.
- **Composición de disclosure.** Puede ser leaky; no modelada completamente.
- **Gobernanza multiimplementación.** Principios claros; mecanismos (financiación, coordinación) abiertos.

---

## Qué se parece más a Monero endurecido

La versión mínima defendible es estructuralmente cercana a una evolución de Monero:

- PoW lineal (o blockDAG solo si validado)
- Privacidad en ledger (notas + nullifiers en lugar de ring signatures)
- Privacidad de red obligatoria (vs. Tor opcional)
- Mejor wallet (capas visibles, privacy mode visible)
- Disclosure acotado (pago, recibo, factura)
- Capa de pagos rápidos separada

No es una teoría monetaria nueva. Es Monero endurecido con mejor transporte, mejor wallet y capas superiores limitadas.

---

## Qué ambiciones siguen sin demostrar

- **blockDAG** como mejora de throughput. Hipótesis; no validada.
- **Light client móvil masivo** sin filtración catastrófica. Bloqueante constitucional.
- **Unidad estable overcollateralizada privada.** Mecanismo vacío.
- **Disclosure amplio** (nómina, auditoría, reservas) sin composición leaky. No validado.
- **Multi-implementación** con financiación y coordinación no capturada. Problema político abierto.
- **Pagos rápidos** que mejoren UX sin contaminar la base. Hipótesis; no demostrada.

---

## Conclusión

El repo es un marco serio con invariantes válidos, hipótesis útiles y bloqueantes que pueden recortar o matar la ambición. No es una arquitectura implementable cerrada. La versión mínima (Monero endurecido) es el techo razonable hoy; la versión máxima es especulativa.
