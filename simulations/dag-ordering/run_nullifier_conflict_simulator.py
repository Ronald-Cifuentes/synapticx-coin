#!/usr/bin/env python3
"""
Simulador de conflictos de nullifier en escenario DAG.

HIPÓTESIS: En blockDAG, dos bloques pueden contener la misma tx (mismo nullifier).
El ordering determinístico debe resolver: solo uno sobrevive. El otro se descarta.

ESTE MVP NO IMPLEMENTA DAG. Este script es un harness para:
- definir los casos de conflicto que una implementación DAG debe resolver
- verificar que la cadena LINEAL actual rechaza correctamente (segundo bloque con mismo nullifier falla)

MÉTRICAS:
- conflictos_resolubles: en DAG, ¿todos los conflictos tienen resolución determinística?
- tiempo_ordenacion: ms por bloque (placeholder; no hay DAG real)

DECISIÓN:
- Si DAG no sobrevive: downgrade a lineal (ya implementado)
- Si DAG sobrevive: documentar en consensus-lab
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from coinlab.blocks import compute_merkle_root
from coinlab.chain import Blockchain, validate_block
from coinlab.config import Config
from coinlab.crypto_primitives import hash_hex, owner_secret_hash
from coinlab.pow import mine_block
from coinlab.transactions import (
    PrivateTransaction,
    TransactionInput,
    TransactionOutput,
    create_transfer_with_output_notes,
)
from coinlab.types import CommitmentHash, TxId


def test_linear_rejects_duplicate_nullifier_in_second_block():
    """
    Caso: dos bloques, ambos intentan gastar el mismo nullifier.
    En cadena LINEAL: el segundo bloque no puede aplicarse (nullifier ya usado).
    En DAG hipotético: ordering debe elegir uno; el otro se descarta.
    """
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet = chain.create_genesis("faucet")
    tx, out_notes = create_transfer_with_output_notes(
        [faucet], [50, 50], ["alice", "bob"], fee=0
    )
    from coinlab.mempool import Mempool
    from coinlab.miner import build_and_mine_block
    build_and_mine_block(chain, Mempool(), "miner")
    mempool = Mempool()
    mempool.add_transaction_validated(tx, chain.state)
    build_and_mine_block(chain, mempool, "miner")
    alice_note = out_notes[0]
    tx1, _ = create_transfer_with_output_notes([alice_note], [50], ["bob"], fee=0)
    tx2, _ = create_transfer_with_output_notes([alice_note], [50], ["carol"], fee=0)
    assert tx1.nullifiers() == tx2.nullifiers()
    block1 = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([tx1]),
        timestamp=1,
        difficulty=config.difficulty,
        transactions=[tx1],
        coinbase_commitment=hash_hex("cb1"),
        coinbase_amount=config.block_reward,
    )
    block1.coinbase_owner_secret_hash = owner_secret_hash("miner")
    ok1, _ = chain.add_block(block1, coinbase_owner="miner")
    assert ok1
    block2 = mine_block(
        prev_hash=chain.tip_hash(),
        merkle_root=compute_merkle_root([tx2]),
        timestamp=2,
        difficulty=config.difficulty,
        transactions=[tx2],
        coinbase_commitment=hash_hex("cb2"),
        coinbase_amount=config.block_reward,
    )
    block2.coinbase_owner_secret_hash = owner_secret_hash("miner")
    ok2, err2 = chain.add_block(block2, coinbase_owner="miner")
    assert not ok2
    assert "Nullifier" in err2 or "nullifier" in err2.lower()
    return True


def main():
    print("=== DAG Ordering / Nullifier Conflict Simulator ===\n")
    print("Hipótesis: DAG requiere ordering determinístico para nullifiers.")
    print("MVP actual: cadena LINEAL; conflicto = segundo bloque rechazado.\n")

    test_linear_rejects_duplicate_nullifier_in_second_block()
    print("Caso: dos bloques con mismo nullifier (doble gasto)")
    print("  Lineal: segundo bloque RECHAZADO (nullifier ya usado)")
    print("  DAG: ordering debe elegir uno; el otro descartado")

    print("\nEstado: MVP es lineal. DAG no implementado.")
    print("Si se implementa DAG: este harness define el caso de conflicto a resolver.")
    print("Kill criterion: conflictos no resolubles de forma determinística.")


if __name__ == "__main__":
    main()
