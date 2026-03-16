# privacy-lab

**Bloqueante:** B2 — Supply correctness bajo privacidad fuerte.

**Test plan:** TP-002.

## Hipótesis

Existe construcción que prueba conservación oculta + range + nullifiers + issuance sin exponer montos ni grafos.

## Lo que el MVP prueba vs no prueba

Ver `research/privacy-lab/SUPPLY_MVP_VS_SERIO.md`.

## Gap

- Circuito ZK para conservación
- Range proofs
- Auditoría agregada sin revelar grafos

## Kill criterion

No hay downgrade. Si supply correctness no es auditable sin revelar más de lo permitido → proyecto falla en su base.
