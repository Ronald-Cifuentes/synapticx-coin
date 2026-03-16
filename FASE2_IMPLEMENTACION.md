# FASE 2: IMPLEMENTACIÓN CODE-FIRST — MVP ENDURECIDO

---

## ANTES DE EDITAR

### 1. BUGS REPRODUCIDOS

| Bug | Reproducción | Resultado |
|-----|--------------|-----------|
| Config alterada | Alterar config.json default_asset_id → FAKE, _load_chain | OK: Rechazó "Config alterada: hash no coincide con genesis" |
| Coinbase alterado | Alterar blocks.json coinbase_amount → 999 | OK: Rechazó "Config incoherente con bloques" |
| Legacy format | Genesis sin chain_params_hash | OK: Rechazó "Formato legacy" |
| Tx payload alterado | Alterar output amount en blocks.json | OK: Rechazó "Tx payload alterado o formato legacy" |

**Conclusión:** No hay bugs constitucionales abiertos. Las protecciones de AUDITORIA_CORRECTIVA están activas.

### 2. CAUSAS RAÍZ

N/A — no se corrigieron bugs, se endureció conformance.

### 3. OPCIONES DE DISEÑO

| Opción | Descripción | Decisión |
|--------|-------------|----------|
| Fixture 1 bloque | Mantener genesis solo | Descartada: no ejercita prev_hash chain |
| Fixture 2+ bloques | Genesis + block con tx | Elegida |
| Invalid-cases solo en tests | Sin JSON | Descartada: golden documenta formato |
| Invalid-case JSON | input_inexistente.json | Elegida |
| test_valid_fixture con load_config | Actual | Descartada: config_for_chain alinea con _load_chain |
| test_valid_fixture con config_for_chain | Como _load_chain | Elegida |

### 4. DECISIÓN PROPUESTA

Endurecer conformance sin tocar código de integridad:
- Fixture con 2 bloques (genesis + tx)
- Invalid-case JSON input_inexistente.json
- test_valid_fixture usa config_for_chain
- store.deserialize_tx para cargar invalid-cases

### 5. PLAN DE CAMBIO POR ARCHIVO

| Archivo | Cambio |
|---------|--------|
| scripts/generate_conformance_fixture.py | Añadir mint + mine block 2 |
| scripts/generate_invalid_cases.py | Nuevo: genera input_inexistente.json |
| src/coinlab/store.py | deserialize_tx() público |
| tests/test_conformance.py | config_for_chain; test_invalid_case_input_inexistente_from_json |
| conformance/README.md | Estructura actualizada |
| README.md | Comandos conformance |
| AUDITORIA_CORRECTIVA.md | Sección 9 endurecimiento |

---

## DESPUÉS DE IMPLEMENTAR

### 1. ARCHIVOS MODIFICADOS

| Archivo | Cambio |
|---------|--------|
| scripts/generate_conformance_fixture.py | Fixture 2 bloques con tx |
| scripts/generate_invalid_cases.py | Nuevo |
| src/coinlab/store.py | deserialize_tx() |
| tests/test_conformance.py | config_for_chain, test_invalid_case_input_inexistente_from_json |
| conformance/fixtures/valid_chain/blocks.json | Regenerado (2 bloques) |
| conformance/invalid-cases/input_inexistente.json | Nuevo |
| conformance/README.md | Estructura, comandos |
| README.md | Conformance |
| AUDITORIA_CORRECTIVA.md | Sección 9 |

### 2. DECISIONES DE DISEÑO CERRADAS

- Fixture: 2 bloques. Genesis + block con mint tx.
- Invalid-case: JSON golden con tx_id derivado de payload (verify_tx_id pasa; falla por input inexistente).
- test_valid_fixture: config_for_chain para consistencia con _load_chain.

### 3. DIFF STAT

```
scripts/generate_conformance_fixture.py  | +15 -8
scripts/generate_invalid_cases.py       | +68 (nuevo)
src/coinlab/store.py                    | +5
tests/test_conformance.py               | +29 -6
conformance/README.md                   | +21 -15
conformance/fixtures/valid_chain/blocks.json | +42
conformance/invalid-cases/input_inexistente.json | +27 (nuevo)
README.md                               | +4 -4
AUDITORIA_CORRECTIVA.md                 | +11
```

### 4. TESTS NUEVOS

| Test | Propósito |
|------|-----------|
| test_invalid_case_input_inexistente_from_json | Carga input_inexistente.json, mempool rechaza |

Tests modificados:
- test_valid_fixture_loads_and_validates: usa config_for_chain

### 5. COMANDOS EJECUTADOS

```bash
python scripts/generate_conformance_fixture.py
python scripts/generate_invalid_cases.py
pytest tests/test_conformance.py -v
pytest tests/ -v --tb=no -q
python -m coinlab.cli run-demo
```

### 6. RESULTADO DE TESTS

```
97 passed in 0.77s
```

### 7. RESULTADO DE DEMO / CLI

```
=== Demo OK ===
Cadena válida: True
```

### 8. DEMOSTRACIÓN ANTES DEL FIX

N/A — no se corrigieron bugs. Reproducciones confirmaron que las protecciones ya funcionan.

### 9. DEMOSTRACIÓN DESPUÉS DEL FIX

- Fixture 2 bloques: test_valid_fixture_loads_and_validates PASSED
- Invalid-case JSON: test_invalid_case_input_inexistente_from_json PASSED

### 10. COMPATIBILIDAD / MIGRACIÓN / FAIL-FAST

- Fixture regenerado: ejecutar `python scripts/generate_conformance_fixture.py`
- Invalid-cases: ejecutar `python scripts/generate_invalid_cases.py`
- Sin cambios de formato persistido en producción (solo conformance)

### 11. LIMITACIONES HONESTAS RESTANTES

- wallets.json sigue siendo cache; no reconcile
- vectors/ vacío; supply/ordering bloqueados hasta ZK/DAG
- blockDAG, ZK, disclosure no implementados

### 12. TABLA FINAL

| Área | Antes | Después | Evidencia exacta |
|------|-------|---------|------------------|
| integridad del bloque | block_hash incluye coinbase+chain_params | Igual | blocks.block_hash, test_block_integrity |
| integridad del payload tx | tx_id = H(payload) | Igual | transactions.verify_tx_id, test_tx_payload_integrity |
| atomicidad | add_block, reorg atómicos | Igual | test_atomicity |
| restart/reload | config_for_chain, fail-fast | Igual | test_restart_reload, test_config_constitutional |
| legacy | Rechazo explícito | Igual | test_legacy_format_rejected_explicitly |
| conformance fixture | 1 bloque | 2 bloques con tx | generate_conformance_fixture, test_valid_fixture |
| conformance invalid-cases | Solo en tests | JSON golden + test | input_inexistente.json, test_invalid_case_input_inexistente_from_json |
| test_valid_fixture | load_config + config_compatible | config_for_chain | test_conformance.test_valid_fixture_loads_and_validates |
