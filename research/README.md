# Research labs

## Propósito

Cada lab investiga un bloqueante o hipótesis. **No** contiene implementación de protocolo final. Contiene experimentos y harnesses para validar viabilidad.

**Rebaja epistemológica:** Simulador ≠ solución. Harness ≠ prototipo. Target metric ≠ métrica medida. Hipótesis ≠ evidencia.

## Labs y RESEARCH_ITEM

| Lab | Bloqueante/Hipótesis | Harness | RESEARCH_ITEM |
|-----|----------------------|---------|---------------|
| [light-client-lab](light-client-lab/) | Cliente ligero privado viable | `simulations/light-client-leakage/` | [RESEARCH_ITEM.md](light-client-lab/RESEARCH_ITEM.md) |
| [network-lab](network-lab/) | Privacidad de red usable | `simulations/provider-correlation/` | [RESEARCH_ITEM.md](network-lab/RESEARCH_ITEM.md) |
| [privacy-lab](privacy-lab/) | Supply correctness, ZK | `simulations/supply-correctness/` | [RESEARCH_ITEM.md](privacy-lab/RESEARCH_ITEM.md) |
| [consensus-lab](consensus-lab/) | blockDAG + ordering | `simulations/dag-ordering/` | [RESEARCH_ITEM.md](consensus-lab/RESEARCH_ITEM.md) |
| [disclosure-lab](disclosure-lab/) | Composición de pruebas | `simulations/disclosure-composition/` (stub) | [RESEARCH_ITEM.md](disclosure-lab/RESEARCH_ITEM.md) |
| [stable-unit-lab](stable-unit-lab/) | Unidad estable sin recentralización | — (no hay harness) | [RESEARCH_ITEM.md](stable-unit-lab/RESEARCH_ITEM.md) |

## Formato RESEARCH_ITEM

Cada lab tiene RESEARCH_ITEM.md con:
- Question, Why it matters
- Tasks, Deliverables
- Acceptance, Kill/downgrade trigger
- Dependencies, Priority
- Harness ejecutable (o declaración explícita de ausencia)

## Simuladores ejecutables

| Simulador | Comando | Estado |
|-----------|---------|--------|
| light-client-leakage | `python simulations/light-client-leakage/run_leakage_simulator.py` | Ejecutable |
| provider-correlation | `python simulations/provider-correlation/run_correlation_simulator.py` | Ejecutable |
| dag-ordering | `python simulations/dag-ordering/run_nullifier_conflict_simulator.py` | Ejecutable |
| supply-correctness | `python simulations/supply-correctness/run_supply_correctness.py` | Ejecutable |
| disclosure-composition | `python simulations/disclosure-composition/run_composition_simulator.py` | Stub |
