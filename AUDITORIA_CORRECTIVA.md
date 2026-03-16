# Auditoría correctiva — cierre de rigor

## Corrección 3: tx_id = H(payload) (autenticación del payload de tx)

### Problema estructural resuelto

El merkle root se calculaba sobre tx_ids arbitrarios (aleatorios). Alterar payload de tx en blocks.json (owner_secret_hash, amount, fee, etc.) manteniendo tx_id dejaba merkle_root y block_hash intactos; validate_chain pasaba con estado corrupto.

### Solución implementada

**tx_id = H(serialización canónica del payload):**
- inputs: commitment, nullifier, amount, asset_id, secret
- outputs: commitment, amount, asset_id, owner_secret_hash
- fee

Alterar cualquiera cambia tx_id; merkle_root cambia; validación falla.

---

## Corrección 2: Block hash autentica coinbase (integridad del bloque)

### Problema estructural resuelto

Campos state-relevant (coinbase_commitment, coinbase_amount, coinbase_owner_secret_hash, chain_params_hash) no estaban en block_hash(). Alterar blocks.json permitía corrupción sin cambiar block_hash() ni invalidar PoW.

### Solución implementada

**block_hash() incluye todo lo que afecta validez y estado:**
- prev_hash, merkle_root, timestamp, nonce, difficulty
- coinbase_commitment, coinbase_amount, coinbase_owner_secret_hash, (chain_params_hash o "")

Alterar cualquiera en blocks.json cambia block_hash(); prev_hash del siguiente bloque no coincide → fallo explícito.

---

## Corrección 1: chain_params_hash (config constitucional)

### Problema estructural resuelto

El ledger dependía de config.json (archivo externo editable) para reconstruir semántica constitucional. Alterar config.json permitía reconstrucción canónica distinta o corrupta sin que la cadena lo impidiera.

### Solución implementada

**chain_params_hash anclado en genesis.** La fuente de verdad constitucional está en el ledger:
- `genesis.chain_params_hash = H(difficulty|block_reward|default_asset_id)`
- Al cargar: config desde config.json debe producir hash == genesis.chain_params_hash
- Si config.json fue alterada: RuntimeError explícito
- Formato legado (genesis sin chain_params_hash): rechazo explícito

### Parámetros constitucionales

- difficulty
- block_reward
- default_asset_id

---

## 1. BUGS REALES CONFIRMADOS

### A. Config / estado reconstruido (resuelto)

| Bug | Descripción | Evidencia |
|-----|-------------|-----------|
| `config_compatible_with_blocks()` solo validaba difficulty | block_reward y default_asset_id distintos permitían recarga | `test_config_compatibility_bug.py` |
| Reconstrucción con default_asset_id distinto | coinbase se reconstruía con asset incorrecto; validate_chain pasaba | `test_bug_default_asset_id_mismatch_corrupts_state_BEFORE_FIX` |
| **Alterar config.json manualmente** | Permitía corrupción silenciosa | **Resuelto:** `test_manipulation_config_json_fails_explicitly` |

### B. Block / coinbase no autenticados (resuelto)

| Bug | Descripción | Evidencia |
|-----|-------------|----------|
| Alterar coinbase_commitment | block_hash no cambiaba; estado corrupto | **Resuelto:** `test_alter_coinbase_commitment_breaks_prev_hash` |
| Alterar coinbase_amount | idem | **Resuelto:** `test_alter_coinbase_amount_breaks_prev_hash` |
| Alterar coinbase_owner_secret_hash | idem | **Resuelto:** `test_alter_coinbase_owner_secret_hash_breaks_prev_hash` |
| Alterar chain_params_hash | bypass config + estado corrupto | **Resuelto:** `test_alter_chain_params_hash_breaks_prev_hash_chain` |

### C. Payload de tx no autenticado (resuelto)

| Bug | Descripción | Evidencia |
|-----|-------------|----------|
| Alterar output.owner_secret_hash | tx_id aleatorio; merkle no cambia; estado corrupto | **Resuelto:** `test_alter_output_owner_secret_hash_breaks_validation` |
| Alterar output.amount | idem | **Resuelto:** `test_alter_output_amount_breaks_validation` |
| Alterar fee | idem | **Resuelto:** `test_alter_fee_breaks_validation` |
| Alterar input.nullifier | idem | **Resuelto:** `test_alter_input_nullifier_breaks_validation` |

---

## 2. DECISIÓN DE DISEÑO

**Config:** chain_params_hash en genesis. Verificación contra hash antes de usar config.

**Block hash:** Incluir coinbase + chain_params en block_hash(). Mining recibe coinbase_owner_secret_hash y chain_params_hash; no mutar después.

**tx_id:** tx_id = H(payload canónico). verify_tx_id en validate_block. tx_id aleatorio (legacy) → rechazo.

**Legado:** Genesis sin chain_params_hash → rechazo. Bloques con block_hash viejo → prev_hash rota. Bloques con tx_id aleatorio → verify_tx_id falla. Regenerar fixture: `python scripts/generate_conformance_fixture.py`.

---

## 3. ARCHIVOS MODIFICADOS

| Archivo | Cambio |
|---------|--------|
| `src/coinlab/config.py` | `chain_params_hash(config)` |
| `src/coinlab/blocks.py` | Block.chain_params_hash opcional |
| `src/coinlab/store.py` | `config_for_chain()`, serializar chain_params_hash |
| `src/coinlab/chain.py` | create_genesis asigna chain_params_hash |
| `src/coinlab/cli.py` | _load_chain usa config_for_chain |
| `src/coinlab/blocks.py` | block_hash() incluye coinbase + chain_params |
| `src/coinlab/pow.py` | mine_block recibe coinbase_owner_secret_hash, chain_params_hash |
| `src/coinlab/miner.py` | pasa coinbase_owner_secret_hash a mine_block |
| `tests/test_config_constitutional.py` | **Nuevo.** Manipulación config |
| `src/coinlab/transactions.py` | tx_id_from_payload, verify_tx_id; create_* usa tx_id derivado |
| `src/coinlab/chain.py` | validate_block: verify_tx_id para cada tx |
| `tests/test_block_integrity.py` | **Nuevo.** Alteración blocks.json, legacy |
| `tests/test_tx_payload_integrity.py` | **Nuevo.** Alteración payload tx |
| `conformance/fixtures/valid_chain/` | Regenerado |

---

## 4. TESTS NUEVOS

| Test | Propósito |
|------|-----------|
| `test_manipulation_config_json_fails_explicitly` | Alterar config.json → fallo explícito |
| `test_legacy_format_rejected_explicitly` | Genesis sin hash → rechazo |
| `test_same_dataset_altered_config_fails_no_silent_corruption` | Mismo blocks, config alterada → fallo |
| `test_load_correct_with_unchanged_config` | Carga correcta |
| `test_config_for_chain_verifies_hash` | config_for_chain rechaza config alterada |
| `test_alter_coinbase_commitment_breaks_prev_hash` | Alterar coinbase_commitment → fallo |
| `test_alter_coinbase_amount_breaks_prev_hash` | Alterar coinbase_amount → fallo |
| `test_alter_coinbase_owner_secret_hash_breaks_prev_hash` | Alterar owner_secret_hash → fallo |
| `test_alter_chain_params_hash_breaks_prev_hash_chain` | Alterar chain_params_hash → fallo |
| `test_legacy_block_format_fails_prev_hash` | Formato legacy → rechazo |

---

## 5. DEMOSTRACIÓN ANTES DEL FIX

```bash
# Alterar config.json default_asset_id -> FAKE
# _load_chain() → estado con asset_id=FAKE, validate_chain pasa
# Corrupción silenciosa
python -c "
import json
from pathlib import Path
from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.store import Store
from coinlab.cli import _load_chain
tmp = Path('/tmp/bug'); tmp.mkdir(exist_ok=True)
store = Store(tmp)
config = Config(difficulty=2, default_asset_id='BASE')
chain = Blockchain(config)
chain.create_genesis('faucet')
store.save_config(config)
store.save_blocks(chain.blocks)
data = json.loads(store.config_file.read_text())
data['default_asset_id'] = 'FAKE'
store.config_file.write_text(json.dumps(data, indent=2))
chain2 = _load_chain(store)
print('asset:', chain2.state.notes[str(chain2.blocks[0].coinbase_commitment)].asset_id)
# Antes: FAKE (corrupto)"
```

---

## 6. DEMOSTRACIÓN DESPUÉS DEL FIX

```bash
pytest tests/test_config_constitutional.py::test_manipulation_config_json_fails_explicitly -v
# RuntimeError: Config alterada: hash no coincide con genesis
```

---

## 7. COMPATIBILIDAD / MIGRACIÓN / FAIL-FAST

| Caso | Comportamiento |
|------|----------------|
| Genesis con chain_params_hash | Verificación normal |
| Genesis sin chain_params_hash (legado) | Rechazo: "Formato legacy. Ejecute init-chain --force." |
| config.json alterada | Rechazo: "Config alterada: hash no coincide con genesis." |
| Fixture conformance | Regenerar con `python scripts/generate_conformance_fixture.py` |

---

## 8. TABLA FINAL

| Área | Antes | Después | Evidencia exacta |
|------|-------|---------|------------------|
| fuente de verdad constitucional | config.json | genesis.chain_params_hash, config.json verificada | config.py:chain_params_hash, store.py:config_for_chain |
| dependencia de config externa | Reconstrucción usaba config sin verificar | config debe producir hash == genesis | cli._load_chain, store.config_for_chain |
| reconstrucción de estado | Corrupción silenciosa posible | Fallo explícito si config alterada | test_manipulation_config_json_fails_explicitly |
| manejo de legado | N/A | Rechazo explícito | test_legacy_format_rejected_explicitly |
| restart/reload | Funcionaba con config corrupta | Fallo explícito | test_same_dataset_altered_config_fails_no_silent_corruption |
| autenticación de chain params | Metadata JSON mutable | En block_hash(), alterar invalida | blocks.block_hash, test_alter_chain_params_hash |
| autenticación de coinbase | Fuera de block_hash | En block_hash(), alterar rompe prev_hash | test_alter_coinbase_* |
| integridad del bloque | Solo header en hash | Coinbase + chain_params en hash | blocks.block_hash |
| autenticación de payload tx | tx_id aleatorio | tx_id = H(payload) | transactions.tx_id_from_payload, verify_tx_id |
| merkle root | Sobre tx_ids arbitrarios | Sobre tx_ids derivados de payload | blocks.compute_merkle_root |

---

## Comandos reproducibles

```bash
cd /path/to/coin
pip install -e ".[dev]"
python scripts/generate_conformance_fixture.py  # si fixture legado
pytest tests/ -v
python -m coinlab.cli run-demo
```
