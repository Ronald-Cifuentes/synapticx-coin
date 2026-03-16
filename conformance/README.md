# Conformance

## Propósito

Fixtures válidos y invalid-cases para verificar invariantes del MVP. Los tests viven en `tests/test_conformance.py`.

## Estructura actual

```
conformance/
  fixtures/
    valid_chain/   — 2+ bloques (genesis + tx), config.json, blocks.json
  invalid-cases/
    input_inexistente.json — tx con commitment inexistente (golden)
  vectors/        — vacío (bloqueado hasta ZK/DAG)
```

## Cómo generar fixtures

```bash
python scripts/generate_conformance_fixture.py
python scripts/generate_invalid_cases.py
```

## Cómo ejecutar conformance

```bash
pytest tests/test_conformance.py -v
```

## Invalid-cases

- **En tests:** input inexistente, reuse commitment, block header inválido (construidos programáticamente)
- **En JSON:** input_inexistente.json — golden para formato; test_invalid_case_input_inexistente_from_json lo carga

## Qué NO contiene aún

- vectors/ (ordering, supply proofs) — bloqueado hasta ZK y DAG
