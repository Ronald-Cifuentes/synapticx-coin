# FASE 3: Investigación ejecutable — Lo no resuelto

---

## 1. FRENTE POR FRENTE

### 1.1 Light-client privacy and note discovery

| Elemento | Contenido |
|----------|-----------|
| Threat model | Proveedor registra qué commitments solicita cliente; si pide C → infiere ownership |
| Leakage model | Full sync 0%; naive query 100%; batch depende tamaño |
| Provider assumptions | Ve solicitudes; no ve contenido; correlaciona con sesión |
| Local verification target | Merkle proofs, headers, supply; sync ≤500 MB, batería ≤5%/día |
| Acceptance | Correlación ≤10%; ancho de banda ≤500 MB |
| Kill | >50% correlacionable |
| Downgrade | Full node / infra comunitaria only |

**Archivo:** `research/light-client-lab/RESEARCH_ITEM.md`  
**Harness:** `simulations/light-client-leakage/run_leakage_simulator.py`

---

### 1.2 Network metadata privacy

| Elemento | Contenido |
|----------|-----------|
| Adversary model | Spy nodes registran orden de recepción |
| Spy-node model | Vecino del origen: ~100% inferencia; relay stem diluye |
| Timing correlation | Primer receptor = vecino origen (gossip) |
| Mobile constraints | Latencia p99 <30 s; batería <3%/h |
| Degraded mode | No fingir protección; comunicar cuándo debilitada |
| Acceptance | Inferencia ≤30% |
| Kill | >60% inferencia |
| Downgrade | Modos degradados explícitos |

**Archivo:** `research/network-lab/RESEARCH_ITEM.md`  
**Harness:** `simulations/provider-correlation/run_correlation_simulator.py`

---

### 1.3 Supply correctness bajo privacidad fuerte

| Elemento | Contenido |
|----------|-----------|
| MVP prueba hoy | Conservación agregada, emisión controlada, no doble gasto |
| MVP NO prueba | Montos ocultos, grafos ocultos, auditoría sin revelar |
| Requiere construcción seria | Circuito ZK, range proofs, auditoría agregada |
| Kill criterion | No existe construcción → no hay downgrade; mata programa |

**Archivo:** `research/privacy-lab/RESEARCH_ITEM.md`, `SUPPLY_MVP_VS_SERIO.md`  
**Harness:** `simulations/supply-correctness/run_supply_correctness.py` (modelo simplificado)

---

### 1.4 Consensus geometry

| Elemento | Contenido |
|----------|-----------|
| Lineal implementada | PoW, bloques orden, reorg por trabajo, nullifier único |
| blockDAG hipótesis | No implementada; harness define conflicto |
| Criterios degradar | Divergencia ordering; conflictos no resolubles; >200 ms/bloque |
| Downgrade | Cadena lineal (ya existe) |

**Archivo:** `research/consensus-lab/RESEARCH_ITEM.md`  
**Harness:** `simulations/dag-ordering/run_nullifier_conflict_simulator.py`

---

### 1.5 Stack-level product model (L0–L4)

| Layer | Implementado | Simulado | Conceptual | Bloqueante |
|-------|--------------|----------|------------|------------|
| L0 Privacy transport | — | provider-correlation | Relay, mixnet | Usable en móvil |
| L1 Sovereign base | Cadena, notas, nullifiers | supply, double-spend, mining | blockDAG, supply ZK | Supply serio, DAG |
| L2 Fast payments | — | — | Pagos rápidos | No demostrado |
| L3 Stable unit | — | — | Overcollateralizado | Mecanismo vacío |
| L4 Disclosure | — | disclosure-composition (stub) | Pago, recibo, factura | Composición leaky |

**Archivo:** `docs/04_testplans/TP-STACK-MODEL.md`

---

### 1.6 Disclosure composition

| Elemento | Contenido |
|----------|-----------|
| Hipótesis | 20 pruebas típicas → adversario reconstruye ≤20% grafo |
| Harness | Stub; modelo formal no implementado |
| Kill | >60% reconstruible |
| Downgrade | Reducir a pago, recibo, factura |

**Archivo:** `research/disclosure-lab/RESEARCH_ITEM.md`  
**Harness:** `simulations/disclosure-composition/run_composition_simulator.py` (stub)

---

### 1.7 Stable unit

| Elemento | Contenido |
|----------|-----------|
| Hipótesis | Overcollateralizado sobrevive estrés sin recentralización |
| Harness | No existe |
| Kill | Custodio único, oráculo central |
| Downgrade | Posponer capa estable |

**Archivo:** `research/stable-unit-lab/RESEARCH_ITEM.md`

---

## 2. ARCHIVOS CREADOS / MODIFICADOS

| Archivo | Acción |
|---------|--------|
| docs/04_testplans/TP-STACK-MODEL.md | Creado |
| research/light-client-lab/RESEARCH_ITEM.md | Creado |
| research/network-lab/RESEARCH_ITEM.md | Creado |
| research/privacy-lab/RESEARCH_ITEM.md | Creado |
| research/consensus-lab/RESEARCH_ITEM.md | Creado |
| research/disclosure-lab/RESEARCH_ITEM.md | Creado |
| research/stable-unit-lab/RESEARCH_ITEM.md | Creado |
| research/README.md | Modificado |
| simulations/disclosure-composition/run_composition_simulator.py | Creado |
| simulations/disclosure-composition/README.md | Modificado |
| scripts/run_research_simulations.sh | Modificado |

---

## 3. EXPERIMENTOS / HARNESSES / TESTPLANS

| Frente | Harness | Estado |
|--------|---------|--------|
| Light-client | run_leakage_simulator.py | Ejecutable |
| Network | run_correlation_simulator.py | Ejecutable |
| Supply | run_supply_correctness.py | Ejecutable (modelo simplificado) |
| Consensus/DAG | run_nullifier_conflict_simulator.py | Ejecutable |
| Disclosure | run_composition_simulator.py | Stub |
| Stable unit | — | No existe |

---

## 4. MÉTRICAS Y UMBRALES

| Frente | Éxito | Aborto |
|--------|-------|--------|
| Light-client correlación | ≤10% | >50% |
| Light-client ancho de banda | ≤500 MB | >2 GB |
| Light-client batería 24h | ≤5% | >15% |
| Network inferencia | ≤30% | >60% |
| Network latencia p99 | <30 s | >2 min |
| Network batería 1h | <3% | >8% |
| Supply verificación/tx | <100 ms | >500 ms |
| DAG ordenación/bloque | <50 ms | >200 ms |
| Disclosure grafo (20 pruebas) | ≤20% | >60% |

---

## 5. KILL CRITERIA

| Frente | Kill | Severidad |
|--------|------|-----------|
| Supply correctness | No existe construcción auditable | Mata programa |
| Light-client | >50% correlacionable | Mata ambición móvil |
| Network | >60% inferencia | Obliga modos degradados |
| DAG | Ordering ambiguo, >200 ms/bloque | Downgrade a lineal |
| Disclosure | >60% grafo reconstruible | Reducir tipos prueba |
| Stable unit | Custodio único requerido | Posponer capa |

---

## 6. DOWNGRADE PATHS

| Si falla | Downgrade | Qué preserva |
|----------|-----------|--------------|
| Light-client | Full node / infra comunitaria only | Base, privacidad |
| Network | Modos degradados explícitos | Funcionalidad básica |
| DAG | Cadena lineal | Consenso, notas, nullifiers |
| Disclosure | Pago, recibo, factura únicamente | Interoperabilidad legal básica |
| Stable unit | Posponer capa estable | Base, pagos rápidos |
| Supply | — | No hay downgrade |

---

## 7. TABLA FINAL

| Frente | Estado | Qué sí existe | Qué no existe | Qué lo mata | Qué lo simplifica |
|--------|--------|---------------|---------------|-------------|-------------------|
| **Light-client** | Investigación | Simulador leakage, threat model, RESEARCH_ITEM | Diseño viable, métricas dispositivo real | >50% correlacionable | Full node only |
| **Network** | Investigación | Simulador inferencia, relay vs gossip | Integración wallet, métricas móvil | >60% inferencia | Modos degradados |
| **Supply correctness** | Bloqueante | MVP conservación, simulador supply | ZK, range proofs, auditoría agregada | No existe construcción | No hay downgrade |
| **Consensus DAG** | Hipótesis | Cadena lineal, harness conflicto | DAG, ordering, 10k bloques | Ordering ambiguo, >200 ms | Cadena lineal |
| **L0–L4 stack** | Parcial | L1 base, simuladores L0 | L2, L3, L4, supply ZK | Por capa | Por capa |
| **Disclosure** | Investigación | RESEARCH_ITEM, stub | Modelo formal, adversario | >60% grafo | 3 tipos prueba |
| **Stable unit** | Conceptual | RESEARCH_ITEM | Diseño, simulador estrés | Custodio único | Posponer |
