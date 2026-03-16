# Supply Correctness: MVP vs Modelo Serio

## Lo que el MVP SÍ prueba

| Aspecto | Evidencia |
|---------|-----------|
| Conservación en agregado | `sum(inputs desde estado) == sum(outputs) + fee` |
| Emisión controlada | Coinbase = `block_reward` por bloque; validado en `validate_block` |
| No doble gasto | Nullifiers únicos; rechazo en `can_apply_transaction` |
| Supply auditable | Simulación `run_supply_correctness.py`; test `test_supply_aggregate_conserved` |

## Lo que el MVP NO prueba

| Aspecto | Por qué no |
|---------|------------|
| Montos ocultos | Amount está en `NoteRecord`; no hay range proof ni ZK |
| Grafos ocultos | Inputs/outputs visibles en estructura de tx |
| Auditoría sin revelar | Un auditor que verifica ve commitments y nullifiers; puede correlacionar |
| Inflación maliciosa rechazada criptográficamente | Rechazo es por validación de estado, no por prueba ZK |

## Gap para modelo serio

1. **Circuito ZK** (o equivalente): prueba que `sum(in) = sum(out) + fee` sin revelar montos.
2. **Range proofs**: cada amount en rango válido sin revelar valor.
3. **Auditoría agregada**: derivar emisión total desde estado público sin exponer grafos.

## Kill criterion TP-002

Si no existe construcción que cumpla sin revelar más de lo permitido → **no hay downgrade**. Supply correctness es constitucional.

## Fixtures preparatorios

- `conformance/fixtures/valid_chain/` — cadena válida (ya existe)
- `conformance/invalid-cases/` — inflación, conflictos (tests en `test_conformance.py`)

Vectores JSON para inflación maliciosa: pendiente hasta tener formato de tx con proofs.
