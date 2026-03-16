# Rebajas epistemológicas aplicadas

## De arquitectura cerrada → hipótesis

| Afirmación original | Rebaja |
|---------------------|--------|
| "blockDAG con complejidad implementable" | "Complejidad por validar; no está demostrada manejable" |
| "Supply correctness auditable en MVP" | "Requerido; no cerrado. Sin esto no hay MVP" |
| "Pagos rápidos (acotados) en MVP" | "Sí, si diseño sobrevive. [HIPÓTESIS] no demostrado" |
| "Ordering determinístico en DAG es ingeniería difícil pero acotada" | Eliminado. Con private tx es investigación abierta, no ingeniería. |

---

## De hipótesis → bloqueante

| Afirmación original | Rebaja |
|---------------------|--------|
| "Notas + nullifiers" como modelo cerrado | Modelo es convicción; implementación criptográfica es [BLOQUEANTE DE INVESTIGACIÓN] |
| "Composición de disclosure" como subproblema de H3 | Composición explícitamente [BLOQUEANTE DE INVESTIGACIÓN]; si leaky, disclosure colapsa |

---

## De feature → problema abierto

| Afirmación original | Rebaja |
|---------------------|--------|
| "Harnesses y stubs para validar hipótesis" | "Estructura para prototipos, simulaciones y conformance". No hay harnesses implementados. |
| "Arquitectura conceptual honesta" | "Marco conceptual con restricciones explícitas" |
| "Conformance para validar implementaciones" | "No hay implementaciones. Directorio alimenta prototipos; hoy vacío o con placeholders." |
| "Labs con prototipos" | "Labs vacíos o con stubs. El código que parezca mainnet-ready antes de cerrar bloqueantes es engañoso." |

---

## De lenguaje grandilocuente → sobrio

| Original | Rebajado |
|----------|----------|
| "Adición genuinamente útil" | "Obligan a definir condiciones de aborto. Pocos proyectos los incluyen." |
| "Más honesto que la mayoría de whitepapers" | Eliminado. |
| "Punto de partida honesto" | "Punto de partida desde el que crecer o reconocer límites" |
| "Puede construirse" | "Se intentaría construir" |
| "Arquitectura mínima honesta" (título) | "Versión mínima defendible" + advertencia de que no es diseño listo para construir |

---

## Advertencias frontales añadidas

- README: "No hay nada mainnet-ready."
- README: "La versión mínima (Monero endurecido) es el techo si los bloqueantes no se cierran."
- 00_resumen_ejecutivo: "La versión mínima es más visible y defendible que la versión máxima."
- 06_arquitectura_minima: "No es un diseño listo para construir."
- research/README: "No hay implementación de protocolo."
- conformance/README: "No hay implementaciones de protocolo."
