#!/usr/bin/env python3
"""
Simulador de leakage por patrón de consulta (light client).

HIPÓTESIS: Una consulta directa "¿tienes commitment C?" revela ownership.
Full sync bruto revela menos por-commitment; query ingenua revela todo.

THREAT MODEL: Proveedor adversario registra qué commitments solicita el cliente.
Si el cliente pide C, el proveedor infiere que el cliente posee C.

MÉTRICAS:
- correlation_rate: fracción de commitments del usuario que el proveedor puede inferir
- full_sync: 0% (descarga todo, no pide nada específico)
- naive_query: 100% (cada consulta revela ownership)
- batch_query: depende del tamaño del batch

CRITERIO ABORTO TP-003: >50% correlacionables → diseño inviable
CRITERIO ÉXITO: ≤10% correlacionables
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block
from coinlab.transactions import create_transfer_with_output_notes


def build_chain_and_user_commitments(num_blocks: int = 12) -> tuple:
    """Construye cadena simple; retorna (chain, alice_commitments)."""
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet = chain.create_genesis("faucet")
    mempool = Mempool()
    alice_commits = set()
    spendable = faucet
    for i in range(num_blocks - 1):
        amt = spendable.amount
        if amt < 2:
            build_and_mine_block(chain, mempool, "miner")
            continue
        half = amt // 2
        tx, out_notes = create_transfer_with_output_notes(
            [spendable], [half, amt - half], ["alice", "faucet"], fee=0
        )
        mempool.add_transaction_validated(tx, chain.state)
        build_and_mine_block(chain, mempool, "miner")
        alice_commits.add(str(out_notes[0].commitment()))
        spendable = out_notes[1]
    return chain, alice_commits


def simulate_naive_query(user_commitments: set[str], all_commitments: set[str]) -> float:
    """
    Usuario hace query "¿está C en el estado?" por cada C que posee.
    Proveedor ve exactamente qué preguntó → correlation = 100%.
    """
    return 1.0 if user_commitments else 0.0


def simulate_full_sync(user_commitments: set[str], all_commitments: set[str]) -> float:
    """
    Usuario descarga todo. No hace queries específicas.
    Proveedor solo ve "descargó N bloques" → no correlación por commitment.
    """
    return 0.0


def simulate_batch_query(
    user_commitments: set[str],
    all_commitments: set[str],
    batch_size: int,
) -> float:
    """
    Usuario pide batches de commitments (ej. por rango de block).
    Si batch_size = 1: cada query revela 1 commitment → alta correlación.
    Si batch_size = len(all): equivale a full sync → 0%.
    """
    if not user_commitments:
        return 0.0
    n_total = len(all_commitments)
    if batch_size >= n_total:
        return 0.0
    revealed_per_batch = min(batch_size, len(user_commitments))
    return revealed_per_batch / len(user_commitments) if user_commitments else 0.0


def main():
    print("=== Light Client Leakage Simulator ===\n")
    print("Hipótesis: query directa revela ownership; full sync no.")
    print("Métricas: correlation_rate (fracción inferible por proveedor)\n")

    chain, alice_comm = build_chain_and_user_commitments(12)
    all_comm = chain.state.commitments

    print(f"Chain: {len(chain.blocks)} bloques, {len(all_comm)} commitments")
    print(f"Alice tiene {len(alice_comm)} commitments\n")

    full = simulate_full_sync(alice_comm, all_comm)
    naive = simulate_naive_query(alice_comm, all_comm)
    batch_small = simulate_batch_query(alice_comm, all_comm, 5)
    batch_large = simulate_batch_query(alice_comm, all_comm, len(all_comm))

    print("Resultados:")
    print(f"  Full sync:        correlation = {full:.0%}")
    print(f"  Naive query:      correlation = {naive:.0%}")
    print(f"  Batch (size=5):   correlation = {batch_small:.0%}")
    print(f"  Batch (size=all): correlation = {batch_large:.0%}")

    print("\nCriterios TP-003:")
    print("  Éxito: ≤10%  |  Aborto: >50%")
    if naive > 0.5:
        print("  → Naive query ABORTA (revela >50%)")
    else:
        print("  → Naive query no alcanza aborto en este modelo simplificado")
    print("\nConclusión: full sync no revela; query por commitment revela todo.")
    print("Cualquier diseño que use query directa debe mitigar (batching, padding).")


if __name__ == "__main__":
    main()
