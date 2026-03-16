#!/usr/bin/env python3
"""
Simulador de inferencia de origen (network metadata privacy).

HIPÓTESIS: En gossip plano, el primer nodo que recibe un mensaje es probablemente el origen.
Un relay staging (Dandelion-like) diluye esa señal.

THREAT MODEL: Adversario con N spy nodes. Cada spy registra cuándo recibe cada tx.
Inferencia: dado orden de recepción, ¿puede el adversario identificar el origen?

MÉTRICAS:
- origin_inference_rate: probabilidad de que adversario acierte el origen
- gossip_plano: ~90% (quien recibe primero suele ser vecino del origen)
- relay_staging: menor si hay fase de stem antes de difusión

CRITERIO ABORTO TP-004: >60% inferencia
CRITERIO ÉXITO: ≤30% inferencia
"""

import random
from collections import defaultdict


def build_ring_network(n_nodes: int) -> dict[int, list[int]]:
    """Grafo en anillo: cada nodo conectado a 2 vecinos."""
    return {i: [(i - 1) % n_nodes, (i + 1) % n_nodes] for i in range(n_nodes)}


def simulate_gossip_plain(
    n_nodes: int,
    origin: int,
    spy_nodes: set[int],
    n_runs: int = 100,
) -> float:
    """
    Gossip plano: origen broadcast a vecinos; cada uno reenvía a sus vecinos.
    Spy registra orden de llegada. Inferencia: el primero en recibir es vecino del origen.
    Con un spy vecino del origen: recibe en ronda 1 → inferencia alta.
    """
    hits = 0
    for _ in range(n_runs):
        graph = build_ring_network(n_nodes)
        received: dict[int, int] = {}
        wave = {origin}
        round_num = 0
        while wave and round_num < n_nodes:
            round_num += 1
            next_wave = set()
            for node in wave:
                if node not in received:
                    received[node] = round_num
                    if node in spy_nodes:
                        pass
                for neighbor in graph[node]:
                    if neighbor not in received:
                        next_wave.add(neighbor)
            wave = next_wave
        first_spy_receiver = min(
            (n for n in spy_nodes if n in received),
            key=lambda n: received[n],
            default=None,
        )
        if first_spy_receiver is not None:
            neighbors_of_origin = set(graph[origin])
            if first_spy_receiver in neighbors_of_origin:
                hits += 1
    return hits / n_runs if n_runs else 0.0


def simulate_relay_staging(
    n_nodes: int,
    origin: int,
    spy_nodes: set[int],
    stem_length: int = 2,
    n_runs: int = 100,
) -> float:
    """
    Relay staging: origen envía por stem (cadena de 1 nodo); luego broadcast desde último.
    Spy que recibe en fase stem no sabe si es origen o relay. Inferencia reducida.
    """
    hits = 0
    for _ in range(n_runs):
        graph = build_ring_network(n_nodes)
        current = origin
        stem = [origin]
        for _ in range(stem_length - 1):
            neighbors = [n for n in graph[current] if n not in stem]
            if not neighbors:
                break
            current = random.choice(neighbors)
            stem.append(current)
        broadcast_origin = current
        received = {n: i for i, n in enumerate(stem)}
        wave = {broadcast_origin}
        r = len(stem)
        while wave and r < n_nodes:
            r += 1
            next_wave = set()
            for node in wave:
                for neighbor in graph[node]:
                    if neighbor not in received:
                        received[neighbor] = r
                        next_wave.add(neighbor)
            wave = next_wave
        first_spy = min(
            (n for n in spy_nodes if n in received),
            key=lambda n: received[n],
            default=None,
        )
        if first_spy is None:
            continue
        round_when = received[first_spy]
        if round_when < len(stem):
            hits += 0.0
        else:
            neighbors_of_broadcast = set(graph[broadcast_origin])
            if first_spy in neighbors_of_broadcast:
                hits += 1.0 / max(1, len(neighbors_of_broadcast))
    return hits / n_runs if n_runs else 0.0


def main():
    print("=== Provider Correlation / Origin Inference Simulator ===\n")
    print("Hipótesis: gossip plano revela origen; relay staging diluye.")
    print("Métricas: origin_inference_rate\n")

    n_nodes = 20
    origin = 0
    spy_as_neighbor = {1}
    spy_distant = {n_nodes // 2}

    inf_gossip_n = simulate_gossip_plain(n_nodes, origin, spy_as_neighbor)
    inf_gossip_d = simulate_gossip_plain(n_nodes, origin, spy_distant)
    inf_relay = simulate_relay_staging(n_nodes, origin, spy_as_neighbor, stem_length=2)

    print(f"Setup: {n_nodes} nodos, origen=0")
    print(f"  Gossip (spy=vecino):  inferencia ≈ {inf_gossip_n:.0%}")
    print(f"  Gossip (spy=lejano):  inferencia ≈ {inf_gossip_d:.0%}")
    print(f"  Relay stem=2 (spy=vecino): inferencia ≈ {inf_relay:.0%}")

    print("\nCriterios TP-004:")
    print("  Éxito: ≤30%  |  Aborto: >60%")
    if inf_gossip_n > 0.6:
        print("  → Gossip plano típicamente ABORTA sin mitigación")
    print("\nConclusión: modelo simplificado. Relay staging reduce inferencia.")
    print("Para métricas reales: integrar con wallet y medir en dispositivo.")


if __name__ == "__main__":
    main()
