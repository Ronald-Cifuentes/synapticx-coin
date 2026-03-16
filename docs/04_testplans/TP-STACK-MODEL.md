# Stack-level product model (L0–L4)

## Marco

| Layer | Nombre | Función |
|-------|--------|---------|
| L0 | Privacy transport | Relay, anti-correlación, supervivencia en red hostil |
| L1 | Sovereign monetary base | Emisión, validez, consenso, settlement privado, supply correctness |
| L2 | Fast payments | Pagos retail casi instantáneos, exposición acotada |
| L3 | Stable unit | Unidad de gasto estable, mecanismos de mercado |
| L4 | Selective disclosure | Pruebas estrechas: pago, recibo, factura, nómina, auditoría |

---

## Estado por capa

| Layer | Implementado | Simulado | Conceptual | Bloqueante |
|-------|--------------|----------|------------|------------|
| **L0** | — | `simulations/provider-correlation/` (relay vs gossip) | Relay staging, mixnet | Privacidad usable en móvil; latencia/batería |
| **L1** | Cadena lineal PoW, notas, nullifiers, conservación, config constitucional, block/tx integridad | `run_supply_correctness`, `run_double_spend`, `run_basic_mining` | blockDAG, supply con ZK | Supply correctness serio; blockDAG |
| **L2** | — | — | Pagos rápidos con exposición acotada | No demostrado; puede contaminar base |
| **L3** | — | — | Overcollateralizado privado | Mecanismo vacío; recentralización |
| **L4** | — | — | Pago, recibo, factura; nómina/auditoría | Composición leaky; `simulations/disclosure-composition` vacío |

---

## Evidencia exacta

| Componente | Existe | Ubicación |
|------------|--------|-----------|
| L1 base | Sí | `src/coinlab/`, 97 tests |
| L0 simulador | Sí | `simulations/provider-correlation/run_correlation_simulator.py` |
| Light-client simulador | Sí | `simulations/light-client-leakage/run_leakage_simulator.py` |
| DAG harness | Sí | `simulations/dag-ordering/run_nullifier_conflict_simulator.py` |
| Supply simulador | Sí | `simulations/supply-correctness/run_supply_correctness.py` |
| L2/L3/L4 | No | Solo conceptual en docs |
| Disclosure simulador | No | `simulations/disclosure-composition/` solo README |

---

## Kill criteria por capa

| Layer | Si falla | Downgrade |
|-------|----------|-----------|
| L0 | Inferencia >60%, latencia >2 min, batería >8%/h | Modos degradados explícitos |
| L1 supply | No existe construcción auditable sin revelar | No hay downgrade; mata programa |
| L1 DAG | Ordering ambiguo, verificación >200 ms/bloque | Cadena lineal |
| L2 | Captura o indispensable | Eliminar/simplificar capa |
| L3 | Custodio único, oráculo central | Posponer capa estable |
| L4 | Composición >60% grafo reconstruible | Reducir a pago, recibo, factura |
