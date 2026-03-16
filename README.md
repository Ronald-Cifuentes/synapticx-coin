# CoinLab MVP — Laboratorio de base monetaria privada

**Advertencia:** Esto es un MVP de laboratorio ejecutable. NO es criptografía de producción ni privacidad real.

## Qué SÍ implementa

- Cadena lineal PoW simple (no blockDAG)
- Modelo de notas privadas con commitments
- Nullifiers públicos para evitar doble gasto
- Conservación de valor en agregado
- Estado canónico reproducible
- **Config persistida**: difficulty y block_reward se guardan con la cadena; recarga coherente al reiniciar
- **Validación fuerte**: autorización real (hash(secret)==owner_secret_hash); amount y asset relevantes se resuelven contra el estado (input no es fuente de verdad); commitment único no reutilizable; coinbase según política; difficulty fijada contra policy; merkle root recomputado
- **Reorg por trabajo acumulado** (no solo longitud)
- Mempool rechaza tx con inputs inexistentes y conflictos por nullifier
- CLI: init-chain, create-wallet, mint-demo-notes, create-transfer, show-chain, show-state, show-utxo-equivalent, mine-block, run-demo, validate-chain
- Tests automatizados (68 tests)
- Simulaciones: supply correctness, mining distribution, double spend
- Conformance: fixture válido + invalid-cases (input inexistente, reuse commitment, block header inválido)

## Qué NO implementa

- blockDAG
- ZK real (commitments son hashes, no pruebas criptográficas)
- Privacidad de red
- Stable unit
- Disclosure complejo
- Criptografía de producción

## Política de fees

**Fees quemadas.** El fee de una tx se consume en la ecuación de conservación (in = out + fee). El minero recibe solo `block_reward`; las fees no van al coinbase. Esto es deliberado en el MVP.

## Wallet local

**wallets.json es cache de demo, NO fuente canónica.** La fuente de verdad es la cadena (blocks.json) y el estado derivado. El archivo wallets.json es un helper para el flujo CLI que mantiene notas por owner; puede desincronizarse si se edita manualmente. No hay reconcile/rescan automático.

## Limitaciones honestas

- Sigue siendo laboratorio, no seguridad de producción
- Los primitivos (hash, commitment, nullifier) son simplificaciones para modelar semántica
- No hay privacidad criptográfica real (el secret se revela en la tx)
- No hay privacidad de red; la ambición grande (blockDAG, light client, etc.) sigue abierta
- El laboratorio exige autorización verificable contra estado (owner_secret_hash); en validación contextual, amount y asset se resuelven contra el estado, no contra el input
- Los inputs ya no se validan por autoconsistencia del atacante; hash(secret) debe coincidir con el almacenado
- El commitment es identificador único no reutilizable; no puede reaparecer como output ni coinbase
- El índice owner->balance es auxiliar solo para demos
- PoW con dificultad baja (2 ceros hex) para demos rápidos

## Cómo ejecutar

```bash
# Instalar
pip install -e ".[dev]"

# Tests
pytest tests/ -v
# o
./scripts/run_tests.sh

# Demo completa
python -m coinlab.cli run-demo
# o
./scripts/run_demo.sh

# Flujo CLI interactivo
# (Para comenzar desde cero: init-chain --force)
python -m coinlab.cli init-chain
python -m coinlab.cli create-wallet alice
python -m coinlab.cli mint-demo-notes alice 50
python -m coinlab.cli mine-block
python -m coinlab.cli show-chain
python -m coinlab.cli show-state
python -m coinlab.cli show-utxo-equivalent
python -m coinlab.cli validate-chain
```

## Simulaciones

```bash
python simulations/supply-correctness/run_supply_correctness.py
python simulations/mining-centralization/run_basic_mining_distribution.py
python simulations/double-spend/run_double_spend_test.py
```

## Estructura

```
src/coinlab/
  config.py             # Config (persistida en config.json)
  store.py              # Persistencia: blocks, wallets, mempool, config
  crypto_primitives.py  # hash, commitment, nullifier (MVP)
  notes.py              # Note, NoteCommitment
  transactions.py       # PrivateTransaction
  state.py              # ChainState
  blocks.py             # Block, BlockHeader
  pow.py                # mine_block, meets_difficulty
  chain.py              # Blockchain
  mempool.py            # Mempool
  miner.py              # build_and_mine_block
  cli.py                # Comandos CLI
tests/                  # Suite de tests (68)
conformance/            # fixtures, invalid-cases
simulations/            # supply, mining, double spend
```

## Conformance

```bash
python scripts/generate_conformance_fixture.py
pytest tests/test_conformance.py -v
```

## Siguientes pasos inmediatos

1. Aumentar dificultad PoW para tests de estrés
2. Añadir más vectores a conformance/
