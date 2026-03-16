# Auditoría epistemológica — Estado real del MVP

**Intención:** Separar con brutal honestidad qué está implementado, parcial, scaffold o investigación abierta. Sin inventar evidencia. Código manda sobre documentación.

---

## 1. RESUMEN EJECUTIVO

| Categoría | Contenido |
|-----------|-----------|
| **Implementado** | Cadena lineal PoW, notas/commitments/nullifiers, conservación, config constitucional, block/tx integridad, mempool, CLI, 96 tests, 4 conformance, 6 simulaciones ejecutables |
| **Parcial** | Conformance: fixture válido + invalid-cases en tests; vectors/ e invalid-cases/ como JSON no existen |
| **Scaffold** | research/* (solo READMEs); conformance/vectors/, conformance/invalid-cases/ (carpetas con .gitkeep) |
| **Investigación abierta** | blockDAG, ZK real, privacidad de red, light client privado, disclosure composición, stable unit |

---

## 2. EVIDENCIA VERIFICADA

### 2.1 Tests

```
pytest tests/ -v --tb=no -q
# 96 passed in 0.82s
```

| Archivo | Tests | Estado |
|---------|-------|--------|
| test_conformance.py | 4 | PASS |
| test_config_constitutional.py | 5 | PASS |
| test_block_integrity.py | 8 | PASS |
| test_tx_payload_integrity.py | 7 | PASS |
| test_authorization.py | 8 | PASS |
| test_commitment_uniqueness.py | 7 | PASS |
| test_critical_validation.py | 8 | PASS |
| test_invariants.py | 8 | PASS |
| test_supply_correctness.py | 1 | PASS |
| test_double_spend.py | 1 | PASS |
| test_short_reorg.py | 1 | PASS |
| test_chain_pow.py | 4 | PASS |
| test_nullifiers.py | 2 | PASS |
| test_transactions.py | 3 | PASS |
| test_notes.py | 5 | PASS |
| test_atomicity.py | 5 | PASS |
| test_fee_policy.py | 2 | PASS |
| test_cli_smoke.py | 3 | PASS |
| test_restart_reload.py | 2 | PASS |
| test_config_persistence.py | 4 | PASS |
| test_config_compatibility_bug.py | 6 | PASS |
| test_wallet_partial_state.py | 2 | PASS |

**Evidencia:** `pytest tests/ -v` → 96 passed.

---

### 2.2 Simulaciones ejecutables

| Simulación | Comando | Salida verificada |
|------------|---------|--------------------|
| supply-correctness | `python simulations/supply-correctness/run_supply_correctness.py` | "Supply conservado: OK" |
| mining-centralization | `python simulations/mining-centralization/run_basic_mining_distribution.py` | Distribución miner_a/b/c |
| double-spend | `python simulations/double-spend/run_double_spend_test.py` | "Doble gasto rechazado correctamente" |
| light-client-leakage | `python simulations/light-client-leakage/run_leakage_simulator.py` | Full sync 0%, naive query 100% |
| provider-correlation | `python simulations/provider-correlation/run_correlation_simulator.py` | Gossip vs relay, inferencia |
| dag-ordering | `python simulations/dag-ordering/run_nullifier_conflict_simulator.py` | "MVP es lineal. DAG no implementado" |

**Evidencia:** Todas ejecutan sin error. Son harnesses de hipótesis, no prototipos de protocolo.

---

### 2.3 Conformance

| Elemento | Estado | Evidencia |
|----------|--------|-----------|
| fixtures/valid_chain/ | Existe | config.json, blocks.json |
| invalid-cases | En tests, no en JSON | test_invalid_input_inexistente_rejected, test_invalid_reuse_commitment_rejected, test_invalid_block_header_difficulty_rejected |
| vectors/ | Vacío (solo README) | supply-*.json, ordering-*.json bloqueados hasta ZK y DAG |
| invalid-cases/ (carpeta) | Vacía (.gitkeep) | No hay archivos JSON de casos inválidos |

**Evidencia:** `pytest tests/test_conformance.py -v` → 4 passed.

---

### 2.4 Research labs

| Lab | Contenido | Estado |
|-----|-----------|--------|
| consensus-lab | README.md | Solo documentación |
| privacy-lab | README.md, SUPPLY_MVP_VS_SERIO.md | Solo documentación |
| light-client-lab | README.md | Solo documentación |
| network-lab | README.md | Solo documentación |
| disclosure-lab | README.md | Solo documentación |
| stable-unit-lab | README.md | Solo documentación |

**Evidencia:** `find research -type f` → solo READMEs. No hay código ejecutable en research/*.

---

### 2.5 disclosure-composition

```
simulations/disclosure-composition/README.md:
"Reconstrucción de grafo con N pruebas de disclosure no está implementada."
```

**Evidencia:** No hay run_*.py. Solo README que declara no implementado.

---

## 3. VERIFICACIÓN DE CLAIMS DEL README

| Claim README | Verificado | Nota |
|--------------|------------|------|
| Cadena lineal PoW simple (no blockDAG) | SÍ | chain.py, blocks.py |
| Modelo de notas privadas con commitments | SÍ | notes.py, transactions.py |
| Nullifiers públicos para evitar doble gasto | SÍ | test_double_spend, mempool |
| Conservación de valor en agregado | SÍ | test_supply_correctness, run_supply_correctness |
| Config anclada en ledger (chain_params_hash) | SÍ | test_config_constitutional, AUDITORIA_CORRECTIVA |
| Block hash autentica coinbase | SÍ | test_block_integrity |
| tx_id = H(payload) | SÍ | test_tx_payload_integrity |
| Reorg por trabajo acumulado | SÍ | test_short_reorg |
| Mempool rechaza inputs inexistentes y nullifier conflict | SÍ | test_conformance, test_double_spend |
| CLI: init-chain, create-wallet, mint-demo-notes, etc. | SÍ | `python -m coinlab.cli --help` |
| 96 tests | SÍ | pytest tests/ → 96 passed |
| Simulaciones: supply, mining, double spend | SÍ | Ejecutadas |
| Conformance: fixture válido + invalid-cases | SÍ | Fixture existe; invalid-cases en tests (no JSON) |

**Ningún claim del README contradice el código.** La documentación es correcta respecto al estado actual.

---

## 4. LO QUE NO EXISTE (NO DEMOSTRADO POR EL REPO ACTUAL)

| Área | Estado |
|------|--------|
| blockDAG | NO implementado. DAG no existe. |
| ZK real | Commitments son hashes. No proof/verify. |
| Privacidad de red | No hay capa de red. |
| Light client privado | Solo simulador de leakage (harness). |
| Conformance vectors JSON | vectors/ vacío; supply-*.json, ordering-*.json bloqueados. |
| invalid-cases como JSON | invalid-cases/ vacío; casos en tests. |
| disclosure-composition | No implementado (README explícito). |
| Stable unit | Solo research lab (README). |

---

## 5. DECISIÓN DE DISEÑO (NO CAMBIOS)

| Área | Decisión |
|------|----------|
| invalid-cases | Los tests construyen casos programáticamente. No es obligatorio tener JSON; los tests son evidencia suficiente. |
| vectors | Bloqueados hasta ZK y DAG. Documentación correcta. |
| research | Labs son documentación + plan de investigación. Simuladores en simulations/ son los harnesses. |

---

## 6. COMANDOS REPRODUCIBLES

```bash
cd /path/to/coin
pip install -e ".[dev]"

# Tests
pytest tests/ -v
# 96 passed

# Conformance
pytest tests/test_conformance.py -v
# 4 passed

# Simulaciones
python simulations/supply-correctness/run_supply_correctness.py
python simulations/mining-centralization/run_basic_mining_distribution.py
python simulations/double-spend/run_double_spend_test.py
./scripts/run_research_simulations.sh

# Demo
python -m coinlab.cli run-demo
```

---

## 7. LIMITACIONES HONESTAS

1. **MVP de laboratorio.** No es criptografía de producción.
2. **Commitments = hashes.** No ZK. No proof/verify.
3. **Secret en tx.** No privacidad criptográfica real.
4. **wallets.json es cache de demo.** No reconcile ni rescan.
5. **PoW difficulty 2.** Para demos rápidos.
6. **Simuladores ≠ solución.** Informan diseño, no cierran bloqueantes.
7. **Research labs = solo READMEs.** No ejecutables en research/*.

---

## 8. CRITERIO DE ÉXITO (CUMPLIDO)

- **MVP de laboratorio duro y coherente:** SÍ. 96 tests, 6 simulaciones, conformance, auditoría correctiva aplicada.
- **Separación implementación vs ambición:** SÍ. Este documento.
- **Programa de investigación explícito:** SÍ. research/*, simulations/*, kill criteria en simuladores.
- **Auditoría que diga qué existe y qué no:** SÍ. Este documento.

---

## 9. QUÉ PODRÍA MATAR EL PROGRAMA

| Riesgo | Estado |
|--------|--------|
| Supply correctness con ZK | Bloqueante: requiere circuitos/proofs. No implementado. |
| blockDAG + ordering + nullifier conflict | Bloqueante: DAG no implementado. Harness existe. |
| Light client sin leakage | Bloqueante: naive query 100% correlación. Aborto TP-003. |
| Privacidad de red | Bloqueante: gossip plano revela origen. Relay staging en simulador. |
| Disclosure composición | No implementado. |
| Stable unit | Sin recentralización. Solo research. |

---

*Documento generado por auditoría epistemológica. Verificado contra repositorio real. Sin inventar archivos ni resultados.*
