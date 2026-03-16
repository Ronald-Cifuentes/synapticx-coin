# Auditoría correctiva final — Limpieza de incoherencias

**Documento histórico:** Registro de correcciones aplicadas en sesión anterior. Los valores (97 tests, 5 conformance, etc.) reflejan el estado en ese momento. **Estado actual:** 108 tests; ver AUDITORIA_EPISTEMOLOGICA.md o README.md.

---

## 1. CONTRADICCIONES REALES CONFIRMADAS (en ese momento)

| Contradicción | Ubicación | Corrección |
|---------------|-----------|------------|
| "No existe harness" cuando stub existe | research/disclosure-lab/RESEARCH_ITEM.md | "Existe stub ejecutable; no hay experimento completo" |
| "solo README" en disclosure-composition | docs/04_testplans/TP-STACK-MODEL.md | "Stub run_composition_simulator.py existe" |
| "L4 vacío" cuando stub existe | TP-STACK-MODEL tabla L4 | "disclosure-composition (stub)" en columna Simulado |
| "96 tests" | README, AUDITORIA_EPISTEMOLOGICA | 97 tests |
| "4 conformance" | AUDITORIA_EPISTEMOLOGICA | 5 conformance |
| "invalid-cases vacía" | AUDITORIA_EPISTEMOLOGICA | input_inexistente.json existe |
| "integridad constitucional cerrada" | FASE4 | "endurecida (tests)" |
| "Cerrado" en tabla FASE4 | FASE4 | "Endurecido" (no verificación formal) |
| run_tests.sh hace pip install que falla | scripts/run_tests.sh | Eliminado pip install; requiere instalación previa |

---

## 2. ARCHIVOS MODIFICADOS

| Archivo | Cambio |
|---------|--------|
| research/disclosure-lab/RESEARCH_ITEM.md | Deliverables, Dependencies, Experimento razonable |
| docs/04_testplans/TP-STACK-MODEL.md | L4 tabla, Evidencia Disclosure |
| scripts/run_tests.sh | Eliminado pip install; comentario requisito |
| AUDITORIA_EPISTEMOLOGICA.md | Tests 97, conformance 5, invalid-cases, fixture 2 bloques |
| FASE4_AUDITORIA_FINAL_BRUTAL.md | Cerrado→Endurecido; integridad endurecida; Research 5+1 stub |
| README.md | 97 tests; requisito pip install; disclosure stub en lista |

---

## 3. CLAIMS REBAJADOS

| Claim original | Rebaja |
|----------------|--------|
| "integridad constitucional cerrada" | "endurecida (tests documentan rechazo de mutaciones)" |
| "Cerrado" (tabla) | "Endurecido" — no hay verificación formal |
| "no existe harness" (disclosure) | "existe stub; no experimento completo" |
| "solo README" (disclosure) | "stub run_composition_simulator.py" |
| "L4 vacío" | "stub; no produce métricas" |

---

## 4. COMANDOS REALMENTE REPRODUCIBLES

| Comando | Funciona | Requisito |
|---------|----------|-----------|
| `./scripts/run_demo.sh` | Sí | pip install -e . (el script lo ejecuta) |
| `./scripts/run_tests.sh` | Sí | pip install -e ".[dev]" previo |
| `python -m coinlab.cli run-demo` | Sí | pip install -e . previo |
| `./scripts/run_research_simulations.sh` | Sí | pip install -e . previo; PYTHONPATH implícito (desde raíz) |
| `pytest tests/ -v` | Sí | pip install -e ".[dev]" previo |

**Nota:** Todos requieren `pip install -e .` o `pip install -e ".[dev]"` desde raíz. No requieren PYTHONPATH explícito si se ejecuta desde raíz con paquete instalado.

---

## 5. DIFF STAT

```
research/disclosure-lab/RESEARCH_ITEM.md     | 8 +-
docs/04_testplans/TP-STACK-MODEL.md          | 3 +-
scripts/run_tests.sh                         | 3 +-
AUDITORIA_EPISTEMOLOGICA.md                  | 8 +-
FASE4_AUDITORIA_FINAL_BRUTAL.md              | 12 +-
README.md                                    | 5 +-
AUDITORIA_LIMPIEZA_FINAL.md                  | nuevo
```

---

## 6. RESULTADO DE TESTS (en ese momento)

```
97 passed in 0.69s
```

---

## 7. TABLA FINAL (estado tras esa sesión)

| Área | Antes | Después | Evidencia |
|------|-------|---------|-----------|
| Disclosure harness | "no existe" | Stub existe | run_composition_simulator.py ejecutable |
| Disclosure experimento | "no hay" | "no hay completo" | Stub no produce métricas |
| TP-STACK L4 | "vacío" | "stub" | Tabla y evidencia corregidas |
| Tests count | 96 | 97 | pytest |
| Conformance | 4 tests | 5 tests | test_invalid_case_input_inexistente_from_json |
| invalid-cases | "vacía" | input_inexistente.json | Archivo existe |
| Integridad | "cerrada" | "endurecida" | Tests; no verificación formal |
| run_tests.sh | pip install falla | pytest directo | Requiere install previo |

---

## Addendum: consistencia residual (segunda pasada)

| Archivo | Corrección |
|---------|------------|
| AUDITORIA_EPISTEMOLOGICA | 96→97, 4→5, disclosure "solo README"→stub existe, invalid-cases vacía→input_inexistente.json |
| README | 96→97 en estructura |
| FORENSIC_BASELINE_FASE1 | 96→97, 4→5, invalid-cases, disclosure-composition |
