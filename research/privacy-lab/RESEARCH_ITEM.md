# Supply correctness bajo privacidad fuerte — Research item

## Question

¿Existe construcción criptográfica que pruebe conservación de valor oculta + range validity + nullifiers + issuance sin exponer montos ni grafos, permitiendo auditoría agregada?

## Why it matters

Sin supply correctness auditable, no se puede distinguir dinero sano de inflación oculta. Es constitucional. **No hay downgrade.** Si falla, el proyecto falla en su base.

## Lo que el MVP SÍ prueba hoy

| Aspecto | Evidencia |
|---------|-----------|
| Conservación en agregado | `sum(inputs desde estado) == sum(outputs) + fee` |
| Emisión controlada | Coinbase = `block_reward` por bloque; `validate_block` |
| No doble gasto | Nullifiers únicos; `can_apply_transaction` |
| Supply auditable (modelo simplificado) | `run_supply_correctness.py`, `test_supply_aggregate_conserved` |

## Lo que el MVP NO prueba

| Aspecto | Por qué no |
|---------|------------|
| Montos ocultos | Amount en `NoteRecord`; no range proof ni ZK |
| Grafos ocultos | Inputs/outputs visibles en estructura de tx |
| Auditoría sin revelar | Auditor ve commitments y nullifiers; puede correlacionar |
| Inflación maliciosa rechazada criptográficamente | Rechazo por validación de estado, no por prueba ZK |

## Qué requeriría construcción seria

1. **Circuito ZK** (o equivalente): prueba `sum(in) = sum(out) + fee` sin revelar montos
2. **Range proofs**: cada amount en rango válido sin revelar valor
3. **Auditoría agregada**: derivar emisión total desde estado público sin exponer grafos

## Kill criterion constitucional

Si no existe construcción que cumpla sin revelar más de lo permitido → **no hay downgrade**. Supply correctness es no negociable.

## Tasks

1. [ ] Especificar circuito/proof candidato
2. [ ] Test vectors con inflación maliciosa (formato pendiente hasta ZK)
3. [ ] Auditoría independiente (cuando exista construcción)
4. [ ] Benchmark: verificación <100 ms/tx en commodity

## Deliverables

- `conformance/vectors/supply-*.json` — bloqueado hasta ZK
- `conformance/invalid-cases/inflation-*.json` — bloqueado hasta ZK
- Especificación del circuito
- Informe de auditoría independiente

## Acceptance criteria

| Métrica | Éxito | Aborto |
|---------|-------|--------|
| Auditoría reproducible | Sí, <1h | No reproducible |
| Verificación/tx | <100 ms | >500 ms |
| Inflación maliciosa | Rechazada en todos los vectores | Cualquier vector pasa |
| Revelación grafos | Ninguna | Cualquier filtración |

## Dependencies

- MVP con conservación (existe)
- Construcción criptográfica (no existe)

## Priority

P0 — Constitucional. Sin esto, no hay dinero privado auditable.

## Harness ejecutable

```bash
python simulations/supply-correctness/run_supply_correctness.py
```

**Resultado actual:** Conservación en modelo simplificado (amounts visibles). No es evidencia de supply correctness serio.
