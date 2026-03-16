# Programa general de investigación

## Qué es esto

Este documento define un **programa de investigación formal** con condiciones de aborto. No es un backlog de features. No es un roadmap de implementación. Es un conjunto de preguntas abiertas, hipótesis a validar y criterios que determinan si el programa continúa, se simplifica o se abandona.

---

## Categorías de problemas abiertos

Todo tema abierto entra en una de estas categorías:

| Categoría | Descripción | Ejemplo |
|-----------|-------------|---------|
| **Problema abierto de investigación** | Sin solución conocida; puede no existir | Cliente ligero privado usable |
| **Problema de ingeniería difícil pero acotado** | Solución conocida en principio; implementación no trivial | (ninguno con private tx: el DAG+privado es investigación) |
| **Problema de producto** | UX, usabilidad, adopción | Wallet honesta sin confundir capas |
| **Problema político / social no resoluble solo con tecnología** | Coordinación, financiación, captura | Gobernanza multiimplementación |

---

## Lo que este programa no es

- **No es un roadmap** que asume que las piezas existirán. Un roadmap dice "cuándo"; este programa dice "si existe evidencia de que X es viable".
- **No es un plan de implementación** que trata bloqueantes como ítems de backlog. Los bloqueantes constitucionales pueden invalidar el programa; no son tareas a tachar.
- **No es optimismo estructurado.** Cada frente tiene criterios de éxito, de fracaso y de simplificación explícitos.

---

## Fases del programa

| Fase | Objetivo | Salida |
|------|----------|--------|
| **Investigar** | Determinar si algo es viable | Evidencia a favor o en contra |
| **Diseñar** | Especificar cómo, dado que es viable | Especificación validada |
| **Implementar** | Construir según especificación | Prototipo o producción |

No se diseña lo que no se ha investigado. No se implementa lo que no se ha diseñado y validado.

---

## Condiciones de aborto

El programa tiene kill criteria explícitos. Si se cumple alguno, la decisión requerida es: abortar la visión máxima, simplificar a la versión mínima, o abandonar el programa. No hay "seguir adelante y ver".

---

## Referencias

- Bloqueantes constitucionales: `01_bloqueantes_constitucionales.md`
- Hipótesis a validar: `02_hipotesis_de_diseno_a_validar.md`
- Experimentos: `03_experimentos_y_prototipos_minimos.md`
- Kill criteria: `04_matriz_de_kill_criteria.md`
- Downgrade paths: `05_matriz_de_downgrade_paths.md`
- Orden de investigación: `06_orden_serio_de_investigacion.md`
- Qué podría invalidar todo: `07_que_podria_invalidar_todo.md`
