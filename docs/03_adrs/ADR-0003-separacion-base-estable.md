# ADR-0003: Separación base / unidad estable

## Contexto

Mezclar soberanía y estabilidad en una sola capa crea punto único de fallo y captura. La base debe poder sobrevivir aunque la capa estable falle. La estabilidad requiere mecanismos (colateral, oráculos, liquidaciones) que contradicen la privacidad y soberanía de la base si se fusionan.

## Decisión

La base y la unidad estable son capas separadas. La base no será forzada a ser unidad estable final. La estabilidad diaria no puede contaminar la base con custodios, oráculos centrales o transparencia universal. Si la capa estable falla, la base sigue intacta.

## Estado epistemológico

[CONVICCIÓN ESTRUCTURAL]. Cerrado. La separación es conceptual; no depende de que exista un diseño concreto de unidad estable.

## Consecuencias

- La capa estable es opcional para el lanzamiento mínimo
- Si la stable unit no puede construirse sin recentralización, se pospone
- La base se diseña para operar sin estabilidad

## Qué lo invalidaría

Un cambio de objetivo que priorice estabilidad sobre soberanía. O evidencia de que la separación es técnicamente imposible (p. ej. que toda estabilidad requiera control directo del consenso base). No hay tal evidencia hoy.
