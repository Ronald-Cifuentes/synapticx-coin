# FASE 4: AUDITORÍA FINAL BRUTAL

---

## 1. RESUMEN EJECUTIVO BRUTAL

El MVP es un **laboratorio de cadena lineal PoW con notas privadas** que demuestra conservación, integridad constitucional y rechazo de mutaciones silenciosas. No es criptomoneda de producción. No hay ZK real, no hay privacidad de red, no hay light client viable, no hay blockDAG, no hay unidad estable. La ambición de "verdadera criptomoneda" depende de resolver bloqueantes que nadie ha cerrado. El techo honesto hoy es Monero endurecido con mejor transporte; el resto es investigación abierta o especulación.

---

## 2. QUÉ SÍ QUEDÓ FIRME

| Área | Evidencia |
|------|-----------|
| Integridad del bloque | `blocks.block_hash()` incluye coinbase + chain_params; `test_block_integrity` |
| Integridad del payload tx | `tx_id = H(payload)`; `verify_tx_id`; `test_tx_payload_integrity` |
| Atomicidad add_block/reorg | `chain.add_block` temp_state; `test_add_block_is_atomic_on_failure` |
| Restart/reload | `config_for_chain` verifica genesis; `test_restart_reload` |
| Chain params constitucional | `chain_params_hash` en genesis; alterar config.json falla |
| Conservación agregada | `test_supply_aggregate_conserved`; `run_supply_correctness` |
| Doble gasto rechazado | `test_double_spend`; mempool rechaza nullifier conflict |
| Conformance | Fixture 2 bloques; invalid-case JSON; 5 tests conformance |
| Research útil | RESEARCH_ITEM por lab; simuladores ejecutables; kill criteria explícitos |

---

## 3. QUÉ SIGUE ABIERTO

| Área | Estado |
|-----|--------|
| Light-client privacy | Simulador modela amenaza (naive query 100%); diseño viable no existe |
| Network metadata | Simulador modela gossip vs relay; integración wallet no existe |
| Supply correctness serio | MVP prueba conservación con amounts visibles; ZK no existe |
| blockDAG | Harness define conflicto; DAG no implementado |
| Disclosure composición | Stub documenta experimento; modelo formal no existe |
| Stable unit | RESEARCH_ITEM; diseño y simulador no existen |
| Pagos rápidos L2 | Conceptual; no demostrado |
| Multi-implementación | Principios; financiación y coordinación abiertos |

---

## 4. QUÉ ESTÁ MAL Y NO SE HA CONSIDERADO SUFICIENTEMENTE

### Si la ambición es "verdadera criptomoneda que supere estos problemas":

**a) Privacidad: pseudonimato vs anonimato vs disclosure**

- **Pseudonimato** (IOTA, muchas L1): identidad verificable por diseño; trazabilidad para compliance; eficiencia y validadores visibles. El proyecto rechaza esto como base.
- **Anonimato fuerte** (Monero): ring signatures, stealth addresses; no hay identidad verificable por defecto. El proyecto apunta aquí para la base.
- **Disclosure selectivo**: pruebas estrechas (pago, recibo) sin revelar grafo completo. El proyecto lo quiere; la composición no está modelada.
- **Gap no cerrado:** No hay construcción que combine anonimato fuerte + supply auditable + disclosure selectivo. El MVP modela la semántica con hashes; no hay proofs.

**b) Una cadena vs pila multicapa**

La visión honesta **exige pila multicapa**: L0 transporte, L1 base, L2 pagos rápidos, L3 estable, L4 disclosure. Hoy solo L1 base existe (y parcial). L0, L2, L3, L4 son conceptuales o stub. No se puede "superar problemas" con una sola cadena; la arquitectura asume capas que no existen.

**c) Lo que no se promete (correctamente)**

- Coerción física: no se derrota
- Regulación: no se evade
- Adopción por decreto: no existe
- Economía circular: no hay tooling real (mercados, oráculos, integraciones)
- Fantasía cypherpunk: el corpus evita esto; kill criteria y downgrade paths son antídoto

**d) IOTA como contrapunto**

IOTA prioriza eficiencia y coordinación sobre anonimato. Identidad verificable, Coordinador en transición, Tangle. El proyecto CoinLab toma la dirección opuesta: privacidad por defecto, PoW, sin identidad en base. No es blueprint; es contraste: pseudonimato vs anonimato, identidad vs privacidad, eficiencia vs soberanía.

**e) Qué falta considerar**

- **Economía real:** no hay modelo de liquidez, mercados, oráculos, integración con sistemas legados
- **UX de privacidad:** el usuario no sabe cuándo está "protegido" vs "degradado"; no hay indicadores
- **Coste de verificación:** si ZK es >100 ms/tx, la validación se centraliza
- **Light client:** full sync no revela en el modelo; pero full sync en móvil puede ser 2 GB+; el trade-off no está medido

---

## 5. QUÉ MATARÍA EL PROGRAMA

| Bloqueante | Efecto |
|------------|--------|
| Supply correctness no auditable | No hay downgrade; mata todo |
| Light client >50% correlacionable | Restringe a full node; mata ambición móvil |
| blockDAG ordering ambiguo | Downgrade a lineal; no mata |
| Privacidad de red inusable en móvil | Modos degradados; no mata |
| Stable unit requiere custodio único | Posponer capa; no mata |
| Disclosure composición >60% leaky | Reducir tipos; no mata |

---

## 6. QUÉ SERÍA HONESTO CONSTRUIR HOY

1. **L1 base endurecida:** ya está. Cadena lineal, notas, nullifiers, integridad constitucional.
2. **Conformance:** fixture multi-bloque, invalid-cases; ya está.
3. **Research ejecutable:** RESEARCH_ITEM, simuladores, kill criteria; ya está.
4. **No construir:** blockDAG, ZK real, light client, unit estable, disclosure amplio como si estuvieran cerrados.
5. **Siguiente paso honesto:** especificar diseño candidato para supply correctness (circuito/proof); o aceptar que el techo es laboratorio y no producto.

---

## 7. TOP 10 AFIRMACIONES REBAJADAS EPISTEMOLÓGICAMENTE

| # | Afirmación inflada | Rebaja |
|---|--------------------|--------|
| 1 | "Supply correctness" | MVP prueba conservación con amounts visibles; no hay proofs |
| 2 | "Light client privado" | Simulador modela amenaza; diseño viable no existe |
| 3 | "Privacidad de red" | Simulador modela gossip vs relay; no integrado |
| 4 | "blockDAG" | Harness define conflicto; DAG no implementado |
| 5 | "Conformance" | Fixture e invalid-cases existen; vectors supply/ordering bloqueados |
| 6 | "Research útil" | RESEARCH_ITEM y simuladores existen; no cierran bloqueantes |
| 7 | "Disclosure selectivo" | Conceptual; composición no modelada |
| 8 | "Unidad estable" | RESEARCH_ITEM; mecanismo vacío |
| 9 | "Criptomoneda de producción" | Laboratorio; no seguridad real |
| 10 | "Versión mínima defendible" | Monero endurecido; no teoría monetaria nueva |

---

## 8. 5 BLOQUEANTES MÁS SEVEROS

| # | Bloqueante | Severidad |
|---|------------|-----------|
| 1 | Supply correctness no auditable sin revelar | Mata programa |
| 2 | Light client no viable (>50% correlacionable) | Mata ambición móvil |
| 3 | Privacidad de red inusable en móvil | Obliga modos degradados |
| 4 | blockDAG inviable (ordering, coste) | Obliga lineal |
| 5 | Disclosure composición leaky | Obliga reducir tipos |

---

## 9. TABLA FINAL

| Área | Estado | Evidencia | Comentario brutal |
|------|--------|----------|-------------------|
| Integridad del bloque | Cerrado | blocks.block_hash, test_block_integrity | Coinbase + chain_params en hash; alterar rompe prev_hash |
| Integridad payload tx | Cerrado | tx_id_from_payload, verify_tx_id, test_tx_payload_integrity | Alterar payload invalida merkle |
| Atomicidad | Cerrado | chain.add_block temp_state, test_atomicity | add_block y reorg atómicos |
| Restart/reload | Cerrado | config_for_chain, test_restart_reload | Fail-fast en config alterada |
| Wallet local | Parcial | wallets.json, test_wallet_partial_state | Cache de demo; no reconcile; no fuente canónica |
| Conformance | Parcial | fixture 2 bloques, input_inexistente.json, 5 tests | vectors supply/ordering bloqueados |
| Research usefulness | Parcial | RESEARCH_ITEM, 5 simuladores | Útil para estructura; no cierra bloqueantes |
| Light-client privacy | Abierto | run_leakage_simulator | Modela amenaza; naive query 100%; diseño viable no existe |
| Network metadata | Abierto | run_correlation_simulator | Modela gossip vs relay; no integrado |
| Supply correctness seria | Bloqueante | run_supply_correctness, test_supply | MVP con amounts visibles; ZK no existe |
| Consenso lineal | Cerrado | chain.py, 97 tests | PoW, reorg por trabajo |
| blockDAG | Abierto | run_nullifier_conflict_simulator | Harness; DAG no implementado |
| Stable unit | Abierto | RESEARCH_ITEM | Diseño y simulador no existen |
| Selective disclosure | Abierto | run_composition_simulator (stub) | Modelo formal no existe |
| Honest product path | Parcial | docs, kill criteria | Techo: Monero endurecido; no producto |

---

## 10. FRASE FINAL OBLIGATORIA

**Laboratorio de cadena lineal PoW con notas privadas y integridad constitucional cerrada; bloqueantes de supply ZK, light client y privacidad de red abiertos; techo honesto: Monero endurecido, no criptomoneda de producción.**
