# FORENSIC BASELINE — FASE 1

**Contrato:** Inspección del repo real. Sin parches. Sin inventar. Código manda.

---

## 1. ÁRBOL REAL RESUMIDO

### src/

| Archivo | Tipo | Descripción |
|---------|------|-------------|
| `src/coinlab/__init__.py` | Código | Exporta módulos |
| `src/coinlab/config.py` | Código | Config, chain_params_hash() |
| `src/coinlab/store.py` | Código | Persistencia JSON, config_for_chain, config_compatible_with_blocks |
| `src/coinlab/crypto_primitives.py` | Código | hash_hex, nullifier_for_note, owner_secret_hash |
| `src/coinlab/notes.py` | Código | Note, NoteCommitment, create_note |
| `src/coinlab/nullifiers.py` | Código | nullifier_set |
| `src/coinlab/types.py` | Código | CommitmentHash, TxId, BlockHash |
| `src/coinlab/transactions.py` | Código | PrivateTransaction, tx_id_from_payload, verify_tx_id |
| `src/coinlab/state.py` | Código | ChainState, can_apply_transaction, apply_transaction |
| `src/coinlab/blocks.py` | Código | Block, BlockHeader, block_hash(), compute_merkle_root |
| `src/coinlab/pow.py` | Código | mine_block, validate_block_pow, cumulative_work |
| `src/coinlab/chain.py` | Código | Blockchain, add_block, reorg_to, validate_block |
| `src/coinlab/mempool.py` | Código | Mempool, add_transaction_validated |
| `src/coinlab/miner.py` | Código | build_and_mine_block |
| `src/coinlab/cli.py` | Código | init-chain, create-wallet, mint-demo-notes, etc. |

**Total:** 15 archivos .py ejecutables (excl. __pycache__, egg-info).

---

### tests/

| Archivo | Tests | Descripción |
|---------|-------|-------------|
| test_conformance.py | 5 | Fixture válido, invalid input, reuse commitment, block difficulty, invalid-case JSON |
| test_config_constitutional.py | 5 | Manipulación config, legacy, config_for_chain |
| test_block_integrity.py | 8 | Alteración coinbase, chain_params, prev_hash |
| test_tx_payload_integrity.py | 7 | Alteración payload, tx_id derivado |
| test_authorization.py | 8 | Secret/owner_secret_hash, amount desde estado |
| test_commitment_uniqueness.py | 7 | Reuse commitment, coinbase, duplicados |
| test_critical_validation.py | 8 | Input inexistente, coinbase inflado, merkle |
| test_invariants.py | 8 | Forged amount/nullifier, difficulty |
| test_atomicity.py | 5 | add_block atómico, reorg atómico, mempool |
| test_supply_correctness.py | 1 | Conservación agregada |
| test_double_spend.py | 1 | Nullifier duplicado rechazado |
| test_short_reorg.py | 1 | Reorg por trabajo acumulado |
| test_chain_pow.py | 4 | meets_difficulty, validate |
| test_nullifiers.py | 2 | Estabilidad, set |
| test_transactions.py | 3 | Conservación, transfer |
| test_notes.py | 5 | create_note, commitment |
| test_fee_policy.py | 2 | Fee quemado |
| test_cli_smoke.py | 3 | run-demo, init-chain, validate |
| test_restart_reload.py | 2 | Persistencia, config incompatible |
| test_config_persistence.py | 4 | Save/load, compatible |
| test_config_compatibility_bug.py | 6 | Bug default_asset_id, fix |
| test_wallet_partial_state.py | 2 | Cache no reconciliado |

**Total:** 24 archivos, 108 tests.

---

### conformance/

| Ruta | Tipo | Contenido |
|------|------|-----------|
| fixtures/valid_chain/config.json | Fixture real | difficulty, block_reward, default_asset_id |
| fixtures/valid_chain/blocks.json | Fixture real | Genesis con chain_params_hash, coinbase |
| fixtures/.gitkeep | Scaffold | Vacío |
| invalid-cases/ | Fixture real | input_inexistente.json |
| vectors/ | Scaffold | Solo .gitkeep + README; sin supply-*.json, ordering-*.json |
| README.md | Documentación | Propósito, estructura |

---

### simulations/

| Directorio | Ejecutable | README | Estado |
|------------|------------|--------|--------|
| supply-correctness | run_supply_correctness.py | — | Ejecutable |
| mining-centralization | run_basic_mining_distribution.py | — | Ejecutable |
| double-spend | run_double_spend_test.py | — | Ejecutable |
| light-client-leakage | run_leakage_simulator.py | README.md | Ejecutable |
| provider-correlation | run_correlation_simulator.py | README.md | Ejecutable |
| dag-ordering | run_nullifier_conflict_simulator.py | README.md | Ejecutable |
| disclosure-composition | run_composition_simulator.py (stub) | README.md | Stub ejecutable; experimento completo no implementado |

---

### research/

| Directorio | Contenido | Tipo |
|------------|-----------|------|
| consensus-lab | README.md | Documentación |
| privacy-lab | README.md, SUPPLY_MVP_VS_SERIO.md | Documentación |
| light-client-lab | README.md | Documentación |
| network-lab | README.md | Documentación |
| disclosure-lab | README.md | Documentación |
| stable-unit-lab | README.md | Documentación |
| README.md | Índice labs | Documentación |

**No hay código ejecutable en research/.** Harnesses en simulations/.

---

### docs/

| Ruta | Tipo |
|------|------|
| 00_constitucion/*.md | Documentación conceptual |
| 01_arquitectura/*.md | Documentación conceptual |
| 02_investigacion/*.md | Documentación conceptual |
| 03_adrs/*.md | ADRs |
| 04_testplans/*.md | TP-001 a TP-006 |
| 99_auditoria_final/*.md | Veredicto, rebajas |

**Todo documentación.** No código.

---

### scripts/

| Archivo | Tipo | Descripción |
|---------|------|-------------|
| generate_conformance_fixture.py | Ejecutable | Genera fixtures/valid_chain |
| run_demo.sh | Ejecutable | python -m coinlab.cli run-demo |
| run_tests.sh | Ejecutable | pytest tests/ |
| run_research_simulations.sh | Ejecutable | 4 scripts (3 simuladores + 1 stub: light-client, provider, dag, disclosure-composition) |
| check-dependency-map/check.sh | Ejecutable | Check deps |
| generate-research-index/generate.sh | Ejecutable | Índice research |
| lint-docs/lint.sh | Ejecutable | Lint docs |

---

### README.md

Documentación raíz. Claims verificables en sección 3.

---

## 2. INVENTARIO DE CÓDIGO / TESTS / FIXTURES / SCAFFOLDING

| Categoría | Elementos |
|-----------|-----------|
| **Código ejecutable real** | 15 módulos src/coinlab/*.py |
| **Tests reales** | 108 tests en 24 archivos |
| **Fixtures reales** | conformance/fixtures/valid_chain/{config,blocks}.json |
| **Simuladores ejecutables** | 6 simuladores + 1 stub en simulations/ (supply, mining, double-spend, light-client, provider, dag, disclosure-composition) |
| **README/scaffolding** | research/* (RESEARCH_ITEM + READMEs), conformance/vectors/ |
| **Documentación conceptual** | docs/*, README.md |

---

## 3. MATRIZ DE ESTADO ACTUAL

| Fila | Estado | Evidencia exacta | Riesgo si queda así | Categoría |
|------|--------|------------------|---------------------|-----------|
| **block hashing / PoW integrity** | sí | blocks.py:block_hash() incluye prev_hash, merkle_root, timestamp, nonce, difficulty, coinbase_commitment, coinbase_amount, coinbase_owner_secret_hash, chain_params_hash. chain.py:validate_block llama validate_block_pow. test_block_integrity.py:test_alter_coinbase_* | Bajo | no-problema para MVP |
| **tx payload integrity** | sí | transactions.py:tx_id_from_payload, verify_tx_id. chain.py:validate_block llama verify_tx_id por tx. test_tx_payload_integrity.py | Bajo | no-problema para MVP |
| **coinbase integrity** | sí | block_hash incluye coinbase. validate_block verifica coinbase_amount vs policy. test_block_integrity, test_critical_validation | Bajo | no-problema para MVP |
| **chain params integrity** | sí | store.py:config_for_chain, config_compatible_with_blocks verifican chain_params_hash vs genesis. config.py:chain_params_hash. test_config_constitutional | Bajo | no-problema para MVP |
| **state transition integrity** | sí | state.py:can_apply_transaction, apply_transaction. Resolución amount/asset desde estado. test_authorization, test_invariants | Bajo | no-problema para MVP |
| **add_block atomicity** | sí | chain.py:add_block usa temp_state; solo promueve al final. test_atomicity:test_add_block_is_atomic_on_failure | Bajo | no-problema para MVP |
| **reorg atomicity** | sí | chain.py:reorg_to valida en temp_state; reemplaza solo si éxito. test_atomicity:test_reorg_*, test_short_reorg | Bajo | no-problema para MVP |
| **mempool safety** | sí | mempool.py:add_transaction_validated valida contra chain_state. Rechaza inputs inexistentes, nullifier conflict. test_conformance, test_critical_validation, test_atomicity | Bajo | no-problema para MVP |
| **restart/reload correctness** | sí | cli._load_chain usa config_for_chain. store.config_compatible_with_blocks. test_restart_reload, test_config_persistence | Bajo | no-problema para MVP |
| **wallet cache vs canonical state** | parcial | wallets.json es cache; no reconcile ni rescan. README lo declara. test_wallet_partial_state documenta que cache no se reconcilia | Desincronización silenciosa si edición manual | deuda técnica |
| **conformance fixtures** | parcial | Fixture 2 bloques; invalid-cases en tests + input_inexistente.json; vectors/ vacío | vectors bloqueados hasta ZK/DAG | inconsistencia documental menor |
| **research simulations** | sí | 6 simuladores ejecutables. Harnesses de hipótesis, no prototipos | Ninguno para MVP | no-problema para MVP |
| **docs vs code alignment** | sí | README claims verificados. docs/ no afirman implementación cerrada | Ninguno | no-problema para MVP |

---

## 4. CONTRADICCIONES ENTRE RELATO Y REPO

### Claims que SÍ están demostrados (no contradicción)

- README: "Config anclada en ledger" → config_for_chain, chain_params_hash
- README: "Block hash autentica coinbase" → block_hash incluye coinbase
- README: "tx_id = H(payload)" → tx_id_from_payload, verify_tx_id
- README: "108 tests" → pytest: 108 passed
- README: "Conformance: fixture válido + invalid-cases" → test_conformance (invalid-cases en tests + input_inexistente.json)

### Claims que están POR ENCIMA de lo demostrado

| Origen | Claim | Realidad |
|--------|-------|----------|
| README "Siguientes pasos": "Añadir más vectores a conformance/" | Implica vectores como siguiente paso natural | vectors/ vacío; supply-*.json, ordering-*.json bloqueados hasta ZK/DAG |
| docs/04_testplans/TP-001 | "conformance/vectors/ordering-*.json", "conformance/fixtures/dag-conflicts/" | No existen. DAG no implementado |
| docs/04_testplans/TP-002 | "conformance/vectors/supply-*.json", "conformance/invalid-cases/inflation-*.json" | No existen. ZK no implementado |
| simulations/README | "Los resultados deben alimentar conformance/vectors y conformance/invalid-cases" | Normativo futuro; vectors vacío; invalid-cases tiene input_inexistente.json |
| research/consensus-lab | "Harness ejecutable: run_nullifier_conflict_simulator" | Harness existe; DAG no. Lab no implementa DAG |

**Nota:** Los testplans y research declaran "artifacts esperados" o "cuando DAG exista". No afirman que existan hoy. La contradicción es leve: la documentación proyecta artefactos que el repo no produce aún.

### Claims que podrían malinterpretarse

- "Conformance: fixture válido + invalid-cases" — invalid-cases en tests + input_inexistente.json en conformance/invalid-cases/.

---

## 5. LISTA PRIORIZADA DE FALTANTES

### A. Debe corregirse ya en código

- **Ninguno.** No se identificaron bugs constitucionales abiertos. Las correcciones de AUDITORIA_CORRECTIVA están implementadas y testeadas.

### B. Debe endurecerse con tests/fixtures

1. **test_valid_fixture_loads_and_validates** no usa config_for_chain; usa load_config + config_compatible_with_blocks. Funcionalmente equivalente (ambos verifican chain_params_hash). Opcional: alinear con _load_chain usando config_for_chain para consistencia.
2. **conformance/invalid-cases/**: input_inexistente.json ya existe. Tests construyen casos programáticamente también.
3. **Fixture con múltiples bloques:** El fixture actual tiene 1 bloque (genesis). Un fixture con 2–3 bloques y txs ejercitaría mejor la cadena de prev_hash.

### C. No debe implementarse todavía; debe ser experimento/harness

- blockDAG
- ZK real (circuitos, proofs)
- conformance/vectors/supply-*.json (bloqueado hasta ZK)
- conformance/vectors/ordering-*.json (bloqueado hasta DAG)
- disclosure-composition (stub ejecutable; experimento completo no implementado)
- Privacidad de red
- Light client privado (simulador existe como harness)
- Stable unit

### D. Fuera de alcance actual

- Mainnet, producción
- Multi-implementación coordinada
- Gobernanza de upgrades
- Unidad estable sin recentralización

---

## 6. RECOMENDACIÓN DE ALCANCE PARA LA FASE 2

### Enfoque sugerido

1. **No tocar código de integridad.** block_hash, tx_id, chain_params están cerrados con evidencia.

2. **Opcional endurecimiento (B):**
   - Fixture con 2–3 bloques en conformance (si se quiere más cobertura de prev_hash).
   - Un invalid-case JSON en conformance/invalid-cases/ como golden (ej. input_inexistente.json) para documentar formato.

3. **Documentación:**
   - conformance/README ya documenta invalid-cases (tests + input_inexistente.json).
   - Revisar docs/04_testplans para que "artifacts esperados" lleve explícitamente "(pendiente ZK/DAG)".

4. **No abrir:**
   - DAG, ZK, disclosure-composition, stable unit.
   - Nuevos vectores conformance hasta tener construcción criptográfica.

5. **Validación de metadata:**
   - config.json y blocks.json se cargan desde disco. La autenticación es vía chain_params_hash en genesis y verify_tx_id en cada tx. No hay identificadores arbitrarios no autenticados en el flujo de validación.
   - wallets.json: no autenticado; es cache. README lo declara. No es fuente de verdad.

---

*Baseline anclado al árbol real. Sin parches propuestos. Fase 2 puede usar este documento como referencia.*
