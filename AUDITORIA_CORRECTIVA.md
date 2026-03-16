# Auditoría correctiva — cierre de rigor

## 1. BUGS REALES CONFIRMADOS

### A. Config / estado reconstruido

| Bug | Descripción | Evidencia |
|-----|-------------|-----------|
| `config_compatible_with_blocks()` solo validaba difficulty | block_reward y default_asset_id distintos permitían recarga con config incorrecta | `test_config_compatibility_bug.py`: tests de mismatch |
| Reconstrucción con default_asset_id distinto | Al reconstruir chain con `default_asset_id` distinto, el coinbase se reconstruía con asset incorrecto; `validate_chain()` pasaba | `test_bug_default_asset_id_mismatch_corrupts_state_BEFORE_FIX` |
| Corrupción silenciosa | Sin verificación de block_reward ni default_asset_id contra config persistida, el estado podía corruptirse sin fallo explícito | Tests de mismatch |

**Nota:** Sobrescribir `config.json` manualmente sigue permitiendo corrupción. La corrección cubre: override desde CLI, verificación de config contra persistida, y rechazo explícito cuando no hay config. Para proteger contra edición directa del archivo sería necesario `config_fingerprint` / `chain_params_hash` persistido en bloque (no implementado).

---

## 2. DECISIÓN DE DISEÑO TOMADA

**Compatibilidad config:**  
- **Opción elegida:** Compatibilidad estricta sobre parámetros constitucionales (difficulty, block_reward, default_asset_id) contra config persistida.  
- **No elegido:** Persistir `coinbase_asset_id` en bloque o `config_fingerprint` / `chain_params_hash` (requeriría migración de formato).  
- **Regla:** Con bloques existentes, `_load_chain()` usa SOLO config persistida; no se permite override desde CLI con config distinta. Si no hay config persistida: fallo explícito.

**Wallet:**  
- **Opción elegida:** Rebajar formalmente a "parcial".  
- **No elegido:** Implementar `reconcile-wallet-cache` / `rescan-wallet-cache`.  
- **Estado:** wallets.json es cache de demo, NO fuente canónica. No hay reconcile ni rescan. Documentado en README y tests.

---

## 3. ARCHIVOS MODIFICADOS

| Archivo | Cambio |
|---------|--------|
| `src/coinlab/store.py` | `config_compatible_with_blocks()` exige config persistida; valida difficulty, block_reward, default_asset_id contra config guardada; valida `block.coinbase_amount == config.block_reward` |
| `src/coinlab/cli.py` | `_load_chain()` usa solo config persistida cuando hay bloques; rechaza override con config distinta |
| `tests/test_config_persistence.py` | `test_config_incompatible_with_blocks_fails`: guarda config y bloques antes de llamar a `config_compatible_with_blocks` |
| `tests/test_config_compatibility_bug.py` | **Nuevo.** Tests que demuestran bug y verifican corrección |
| `tests/test_wallet_partial_state.py` | **Nuevo.** Tests que documentan estado parcial del wallet |
| `README.md` | Wallet: "ESTADO PARCIAL"; comandos reproducibles; requisitos |
| `research/README.md` | Rebaja epistemológica; harnesses ≠ prototipos |
| `research/light-client-lab/README.md` | "Resultado del simulador (no evidencia de protocolo)"; target metric ≠ métrica medida |

---

## 4. TESTS NUEVOS

| Test | Propósito |
|------|-----------|
| `test_bug_default_asset_id_mismatch_corrupts_state_BEFORE_FIX` | Demuestra que reconstruir con default_asset_id distinto corrompe |
| `test_FIX_reject_config_override_with_different_default_asset_id` | Verifica que _load_chain rechaza override |
| `test_FIX_config_compatible_rejects_block_reward_mismatch` | Verifica rechazo de block_reward distinto |
| `test_FIX_config_compatible_rejects_default_asset_id_mismatch` | Verifica rechazo de default_asset_id distinto |
| `test_FIX_reload_with_identical_config_succeeds` | Recarga correcta con config idéntica |
| `test_FIX_blocks_without_config_fails` | Fallo explícito si no hay config persistida |
| `test_wallet_cache_not_reconciled_on_load` | Documenta que no hay reconcile |
| `test_wallet_cache_is_demo_helper_not_canonical` | Documenta que wallets.json no es fuente canónica |

---

## 5. DEMOSTRACIÓN DEL BUG ANTES

```bash
# Escenario: config con default_asset_id="BASE", crear genesis, guardar
# Luego: config con default_asset_id="FAKE", load_blocks, add_block
# Resultado: chain.state.notes[genesis_comm].asset_id == "FAKE" (incorrecto)
# validate_chain() pasa. Estado corrupto.
pytest tests/test_config_compatibility_bug.py::test_bug_default_asset_id_mismatch_corrupts_state_BEFORE_FIX -v
```

---

## 6. DEMOSTRACIÓN DE LA CORRECCIÓN DESPUÉS

```bash
# Override rechazado
pytest tests/test_config_compatibility_bug.py::test_FIX_reject_config_override_with_different_default_asset_id -v

# Mismatches rechazados
pytest tests/test_config_compatibility_bug.py::test_FIX_config_compatible_rejects_block_reward_mismatch -v
pytest tests/test_config_compatibility_bug.py::test_FIX_config_compatible_rejects_default_asset_id_mismatch -v

# Recarga correcta
pytest tests/test_config_compatibility_bug.py::test_FIX_reload_with_identical_config_succeeds -v

# Sin config: fallo explícito
pytest tests/test_config_compatibility_bug.py::test_FIX_blocks_without_config_fails -v
```

---

## 7. CLAIMS REBAJADOS

| Documento | Antes | Después |
|-----------|-------|---------|
| README wallet | "wallets.json es cache de demo, NO fuente canónica. No hay reconcile/rescan automático" | "Wallet local — ESTADO PARCIAL. ... No hay reconcile ni rescan. Si wallets.json se desincroniza, no se corrige automáticamente." |
| research/README | "Simuladores/harnesses para validar viabilidad" | + "Simulador ≠ solución. Harness ≠ prototipo de protocolo. Target metric ≠ métrica medida. Hipótesis ≠ evidencia." |
| light-client-lab | "Resultado del simulador" | "Resultado del simulador (no evidencia de protocolo)"; "Target metric ≠ métrica medida en entorno real" |

---

## 8. TABLA FINAL

| Área | Antes | Después | Evidencia |
|------|-------|---------|-----------|
| compatibilidad config | Solo difficulty validada; config distinta podía reconstruir | difficulty, block_reward, default_asset_id verificados contra persistida; override rechazado | `test_config_compatibility_bug.py`, `test_config_persistence.py` |
| reconstrucción de estado | default_asset_id distinto reconstruía coinbase incorrecto sin fallo | _load_chain usa solo config persistida; no override; fallo explícito si no hay config | `test_FIX_*`, `test_FIX_blocks_without_config_fails` |
| wallet local | "cache de demo" (implícito parcial) | "ESTADO PARCIAL" explícito; no reconcile; tests documentan | `test_wallet_partial_state.py`, README |
| docs/research claims | Simulador podía leerse como evidencia | Rebaja epistemológica explícita | `research/README.md`, `light-client-lab/README.md` |
| comandos reproducibles | Sin requisitos explícitos | "Requisitos: Python ≥3.10, raíz del repo, instalación previa obligatoria" | README |

---

## Comandos reproducibles (entorno limpio)

```bash
cd /path/to/coin
pip install -e ".[dev]"
pytest tests/ -v
python -m coinlab.cli run-demo
```
