# Conformance

## Propósito

Fixtures válidos y invalid-cases para verificar invariantes del MVP. Los tests viven en `tests/test_conformance.py`.

## Estructura actual

```
conformance/
  fixtures/
    valid_chain/   — Genesis válido (config.json, blocks.json)
  README.md
```

## Cómo generar el fixture

```bash
python scripts/generate_conformance_fixture.py
```

## Cómo ejecutar conformance

```bash
pytest tests/test_conformance.py -v
```

## Invalid-cases (en tests)

Los invalid-cases se ejecutan como tests:

- **input inexistente:** tx con commitment que no está en estado → rechazado
- **reuse commitment:** output que reutiliza commitment existente → rechazado
- **block header inválido:** difficulty distinto a policy → rechazado

## Qué NO contiene aún

- vectors/ (ordering, supply proofs)
- invalid-cases/ como archivos JSON independientes
