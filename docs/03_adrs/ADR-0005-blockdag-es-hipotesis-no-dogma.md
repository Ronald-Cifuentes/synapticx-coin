# ADR-0005: blockDAG es hipótesis, no dogma

## Contexto

Un blockDAG con ordering determinístico permitiría mayor throughput que una cadena lineal. Pero PoW + blockDAG + transacciones privadas no está demostrado viable. Nadie lo ha implementado de forma satisfactoria. La interacción entre ordering paralelo, nullifiers, reorgs y verificación ZK puede ser computacionalmente prohibitiva o lógicamente ambigua.

## Decisión

blockDAG es [HIPÓTESIS DE DISEÑO] con [DOWNGRADE PATH] explícito. Se investiga en research/consensus-lab y simulations/dag-ordering. Si no sobrevive validación adversarial, se degrada a cadena lineal PoW. No se trata como decisión cerrada.

## Estado epistemológico

[HIPÓTESIS DE DISEÑO] + [BLOQUEANTE DE INVESTIGACIÓN]. Abierto. Tiene downgrade path.

## Consecuencias

- No se escribe código de "blockDAG final" hasta que el prototipo pase criterios
- simulations/dag-ordering valida ordering y conflictos antes de cualquier implementación
- La cadena lineal es el fallback documentado

## Qué lo invalidaría

Ordering no determinístico, conflictos de nullifiers ambiguos, o coste de verificación >200 ms/bloque. Eso activa el downgrade a lineal. No mata el programa; simplifica la geometría del ledger.
