# Auditoría correctiva — Fase cleanup (inventario y decisiones)

## ANTES DE EDITAR

### 1. INTENCIÓN EN UNA FRASE

Reducir deuda real: eliminar código/documentos muertos demostrados, corregir contradicciones documentales residuales, sin romper flujo MVP.

### 2. BASELINE DEL REPO

- **Tests:** 108 passed (pytest tests/ -v)
- **Flujo MVP:** init-chain, create-wallet, mint-demo-notes, create-transfer, mine-block, run-demo OK
- **Conformance:** fixture 2 bloques, input_inexistente.json, 5 tests
- **Scripts:** generate_conformance_fixture.py, generate_invalid_cases.py, run_tests.sh, run_demo.sh, run_research_simulations.sh; placeholders: generate-research-index, check-dependency-map, lint-docs

### 3. MAPA DE USO REAL

| Componente | Usado por | Evidencia |
|------------|-----------|-----------|
| add_transaction_validated | CLI, tests, scripts, simulaciones | rg add_transaction_validated |
| add_transaction | NINGUNO | rg "add_transaction\(" → solo definición en mempool.py |
| create_transfer_with_output_notes | CLI, tests, scripts, simulaciones | rg create_transfer_with_output_notes |
| create_transfer_transaction | test_transactions.py | rg create_transfer_transaction |
| commitment_for_output | chain, blocks, transactions, notes, scripts | rg commitment_for_output |
| commitment_for_note | NINGUNO (solo definición + docs) | rg "commitment_for_note\(" → crypto_primitives.py, DESIGN doc |
| nullifier_set, is_nullifier_used, add_nullifier | test_nullifiers.py | rg nullifier_set |
| deserialize_tx | test_conformance, store interno | rg deserialize_tx |

### 4. CONTRADICCIONES CONFIRMADAS

| Contradicción | Ubicación | Estado |
|---------------|-----------|--------|
| "97 passed" vs 108 actual | FASE2_IMPLEMENTACION.md §6 | Histórico; no marcado |
| AUDITORIA_LIMPIEZA_FINAL | Ya marcado "Documento histórico" | OK |

### 5. CANDIDATOS

| Candidato | Tipo | Evidencia | Decisión |
|-----------|------|----------|----------|
| add_transaction (mempool) | Código muerto | rg: 0 callers | ELIMINAR |
| create_transfer_transaction import en cli | Import muerto | cli importa pero nunca llama | ELIMINAR import |
| commitment_for_note | Código deprecado | 0 callers; DESIGN doc "mantener compatibilidad" | DEJAR INTACTO |
| test_commitment_uniqueness.py.bak | Backup | Duplicado de test | ELIMINAR |
| FASE2 "97 passed" | Doc residual | No marca histórico | Marcar explícitamente |
| nullifiers.py | API usada solo por tests | test_nullifiers.py | DEJAR INTACTO — tests son uso válido |

### 6. DECISIONES DE LIMPIEZA

| Elemento | Categoría | Justificación |
|----------|-----------|---------------|
| add_transaction | A. ELIMINAR | 0 callers; ruta débil; add_transaction_validated es la ruta segura |
| cli create_transfer_transaction import | A. ELIMINAR | Import no usado |
| test_commitment_uniqueness.py.bak | A. ELIMINAR | Backup redundante |
| FASE2 §6 resultado | B. CONSERVAR COMO HISTÓRICO | Añadir nota "Valores históricos; estado actual: 108 tests" |
| commitment_for_note | E. DEJAR INTACTO | DESIGN doc pide mantener; DEPRECADO ya documentado |
| nullifiers.py | E. DEJAR INTACTO | Usado por test_nullifiers.py |

### 7. PLAN DE CAMBIO POR ARCHIVO

| Archivo | Cambio |
|---------|--------|
| src/coinlab/mempool.py | Eliminar add_transaction (mantener _add_transaction_internal) |
| src/coinlab/cli.py | Eliminar import create_transfer_transaction |
| tests/test_commitment_uniqueness.py.bak | Eliminar archivo |
| FASE2_IMPLEMENTACION.md | Añadir nota histórica en §6 |
| scripts/generate_conformance_fixture.py | Añadir `if __name__ == "__main__": main()` — script no ejecutaba main() |

---

## DESPUÉS DE IMPLEMENTAR

### 1. ARCHIVOS MODIFICADOS

| Archivo | Cambio |
|---------|--------|
| src/coinlab/mempool.py | Eliminado add_transaction |
| src/coinlab/cli.py | Eliminado import create_transfer_transaction |
| FASE2_IMPLEMENTACION.md | Nota histórica en §6 |
| scripts/generate_conformance_fixture.py | Añadido if __name__ == "__main__": main() |

### 2. ARCHIVOS ELIMINADOS

| Archivo | Razón |
|---------|-------|
| tests/test_commitment_uniqueness.py.bak | Backup redundante |

### 3. ARCHIVOS REGENERADOS

Ninguno. Fixtures se regeneran con scripts; validados con pytest.

### 4. CÓDIGO ENDURECIDO

N/A. add_transaction eliminado (ruta débil); add_transaction_validated ya era la ruta segura.

### 5. TESTS / COMANDOS EJECUTADOS

```bash
pytest tests/ -v --tb=no -q
python -m coinlab.cli run-demo
pytest tests/test_conformance.py -v
python scripts/generate_conformance_fixture.py
python scripts/generate_invalid_cases.py
```

### 6. RESULTADO DE TESTS

```
108 passed in ~2s
```

### 7. CONTRADICCIONES RESUELTAS

| Contradicción | Resolución |
|---------------|------------|
| FASE2 "97 passed" sin contexto | Nota histórica añadida; estado actual: 108 tests |

### 8. CÓDIGO MUERTO ELIMINADO

| Elemento | Evidencia |
|---------|-----------|
| add_transaction (mempool) | 0 callers; rg confirmado |
| create_transfer_transaction import (cli) | Import no usado |
| test_commitment_uniqueness.py.bak | Backup duplicado |

### 9. DOCUMENTOS HISTÓRICOS REETIQUETADOS

FASE2_IMPLEMENTACION.md §6: "Valores siguientes reflejan el estado en el momento de la implementación. Estado actual: 108 tests."

### 10. LIMITACIONES HONESTAS RESTANTES

- commitment_for_note: definido, DEPRECADO, 0 callers; DESIGN doc pide mantener
- nullifiers.py: API usada solo por test_nullifiers.py; chain/state usan sets internos; mantener por tests
- resourses/contexto.txt: referencias a add_transaction; archivo de contexto histórico; no modificado
- scripts generate-research-index, check-dependency-map, lint-docs: placeholders; no eliminados

### 11. TABLA FINAL

| Área | Antes | Después | Evidencia exacta |
|------|-------|---------|-------------------|
| flujo normal MVP | OK | OK | run-demo, 108 tests |
| rutas débiles | add_transaction disponible | Eliminada | mempool.py |
| código muerto | add_transaction, import cli, .bak | Eliminados | rg, eliminación |
| docs residuales | FASE2 "97 passed" sin contexto | Nota histórica | FASE2_IMPLEMENTACION.md |
| metadata generada | N/A | N/A | — |
| consistencia global | 108 tests en README/AUDITORIA | 108 tests; FASE2 marcado histórico | pytest, docs |
