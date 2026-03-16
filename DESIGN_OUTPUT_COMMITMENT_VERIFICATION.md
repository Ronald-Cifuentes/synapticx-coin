# Diseño: Verificación de Semántica de Output Commitment

## 1. BUG REPRODUCIDO

Test: `tests/test_output_commitment_semantics.py::test_arbitrary_output_commitment_rejected`

**Flujo del bug (antes del fix):**
1. Tx con input válido (faucet), output con `commitment = H("arbitrary")` (no derivado de metadata)
2. `output.amount`, `output.asset_id`, `output.owner_secret_hash` coherentes
3. `tx_id = H(payload)` → `verify_tx_id` pasa
4. `mempool.add_transaction_validated(tx, chain.state)` → **aceptaba**
5. `build_and_mine_block` → bloque se minaba
6. Output entraba al estado
7. Atacante gastaba el output con su secret → **pasaba**

**Estado actual:** Fix implementado. Output sin nonce o con commitment no derivado es rechazado por `validate_transaction_basic`.

---

## 2. CAUSA RAÍZ

| Componente | Qué verifica | Qué NO verifica |
|------------|--------------|-----------------|
| `verify_tx_id` | tx_id == H(payload canónico) | Semántica del commitment |
| `validate_transaction_basic` | Estructura, duplicados, conservación con amounts declarados | Vínculo commitment↔metadata |
| `can_apply_transaction` | Inputs existen, autorización, nullifier, conservación desde estado, reuse de commitment | Que output.commitment derive de output metadata |
| `apply_transaction` | — | Persiste NoteRecord sin comprobar vínculo |

**Fórmula actual:** `commitment_for_note(owner_key, amount, nonce, asset_id)` = H(owner_key|amount|nonce|asset_id)

**Problema:** `TransactionOutput` tiene `commitment`, `amount`, `asset_id`, `owner_secret_hash` pero **no tiene `nonce` ni `owner_key`**. No hay forma de verificar que commitment derive de los campos.

---

## 3. OPCIONES DE DISEÑO

### A. commitment = H(owner_secret_hash | amount | asset_id | nonce)

- **Pros:** Output ya tiene owner_secret_hash, amount, asset_id. Solo falta añadir nonce. Verificación pura: no depende de estado.
- **Contras:** Requiere cambiar fórmula de commitment (hoy usa owner_key). Note usa owner_key; output usa owner_secret_hash. Hay que alinear.

### B. commitment = H(owner_key | amount | asset_id | nonce) con owner_key en output

- **Pros:** Mantiene owner_key en fórmula.
- **Contras:** Output tendría que exponer owner_key. Hoy output solo tiene owner_secret_hash (para autorización). Añadir owner_key + nonce duplica información y puede afectar privacidad.

### C. commitment = H(amount | asset_id | nonce) sin binding a owner

- **Pros:** Más simple.
- **Contras:** No vincula commitment al dueño. Cualquiera podría reclamar si adivina. Inaceptable.

### D. Otra fórmula verificable

- Pedersen/Poseidon: fuera de alcance MVP.
- HMAC(owner_secret_hash, amount|asset_id|nonce): equivalente a A en semántica.

**Decisión:** Opción A. `commitment = H(owner_secret_hash | amount | asset_id | nonce)`. El output ya tiene owner_secret_hash; añadimos nonce. La fórmula vincula criptográficamente el commitment a los campos semánticos.

---

## 4. DECISIÓN PROPUESTA

- **Fórmula:** `commitment = H(owner_secret_hash | amount | asset_id | nonce)`
- **Cambios de modelo:**
  - `TransactionOutput`: añadir campo `nonce: str`
  - `Note.commitment()`: usar `owner_secret_hash(secret)` en lugar de `owner_key` en la fórmula
  - `commitment_for_note` → `commitment_for_output(owner_secret_hash, amount, asset_id, nonce)` (o extender la firma)
- **Validación:** Nueva función `validate_output_commitments(tx)` que para cada output verifica `commitment == commitment_for_output(o.owner_secret_hash, o.amount, o.asset_id, o.nonce)`. Llamada desde `validate_transaction_basic` o desde `validate_block` antes de validate_transaction_basic.
- **Coinbase:** Añadir `coinbase_nonce` al Block. Verificar `coinbase_commitment == commitment_for_output(coinbase_owner_secret_hash, coinbase_amount, asset_id, coinbase_nonce)` en validate_block o add_block.

---

## 5. PLAN DE CAMBIO POR ARCHIVO

| Archivo | Cambio |
|---------|--------|
| `crypto_primitives.py` | Añadir `commitment_for_output(owner_secret_hash, amount, asset_id, nonce)`; mantener `commitment_for_note` para compatibilidad o unificar |
| `notes.py` | `Note.commitment()` usa `owner_secret_hash(secret)` en lugar de owner_key |
| `transactions.py` | TransactionOutput: añadir `nonce`; `validate_transaction_basic` o nueva función llama verificación de output commitments; create_transfer* incluye nonce |
| `blocks.py` | Block: añadir `coinbase_nonce`; block_hash incluye coinbase_nonce |
| `pow.py` | mine_block: aceptar coinbase_nonce |
| `chain.py` | create_genesis: pasar coinbase_nonce; add_block/validate_chain: verificar coinbase commitment |
| `miner.py` | Pasar coinbase_nonce al minar |
| `store.py` | Serializar/deserializar nonce en outputs; coinbase_nonce en blocks |
| `scripts/generate_conformance_fixture.py` | Regenerar fixture con nonce |
| `scripts/generate_invalid_cases.py` | Ajustar si usa outputs |
| Tests | test_output_commitment_semantics: invertir para que rechace; añadir tests de mismatch, legítimo, restart, legacy |

---

## 6. RESIDUAL OPERATIVO: MEMPOOL Y tx_id (corregido después)

**Problema:** `add_transaction_validated` no llamaba `verify_tx_id(tx)`. Tx con payload válido pero tx_id falso entraba al mempool; fallo al minar.

**Fix:** `mempool.add_transaction_validated` ahora llama `verify_tx_id(tx)` primero. Mismo contrato que `validate_block`. Tests: `tests/test_mempool_tx_id_integrity.py`.
