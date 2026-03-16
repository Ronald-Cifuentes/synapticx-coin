# ADR-0001: Taxonomía epistemológica y estados del corpus

## Contexto

El corpus mezcla convicciones estructurales, hipótesis de diseño y bloqueantes de investigación. Sin clasificación explícita, se corre el riesgo de presentar hipótesis como soluciones cerradas o problemas abiertos como backlog de ingeniería.

## Decisión

Se adopta una taxonomía obligatoria para etiquetar toda afirmación relevante:

- **[CONVICCIÓN ESTRUCTURAL]** — Regla dura, no depende de investigación futura
- **[HIPÓTESIS DE DISEÑO]** — Dirección razonable, no demostrada
- **[BLOQUEANTE DE INVESTIGACIÓN]** — Problema abierto cuyo fracaso invalida o recorta
- **[DESCARTADO]** — Enfoque rechazado por razones estructurales
- **[DOWNGRADE PATH]** — Ruta de simplificación si la hipótesis falla
- **[KILL CRITERION]** — Condición que obliga a detener o reiniciar

Todo capítulo de arquitectura debe iniciar con: estado epistemológico, qué está cerrado, qué sigue abierto, qué lo mataría.

## Estado epistemológico

Cerrado. La taxonomía es una decisión de proceso, no de investigación.

## Consecuencias

- Los documentos deben etiquetar explícitamente cada afirmación
- No se presenta como implementable lo que depende de un bloqueante no cerrado
- Los bloqueantes tienen kill criteria o downgrade paths asociados

## Qué lo invalidaría

Nada. La taxonomía es meta. Lo que podría invalidarse es su aplicación consistente si el corpus deja de usarla.
