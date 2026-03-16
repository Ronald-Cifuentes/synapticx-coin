# ADR-0004: Light client es bloqueante constitucional

## Contexto

Un usuario móvil necesita descubrir sus notas y verificar estado. Si lo hace pidiendo datos a un proveedor de forma identificable, filtra su grafo de actividad. Si pide todo y filtra localmente, el coste de ancho de banda y batería puede ser prohibitivo. Monero documenta debilidades de wallets ligeras. Ningún sistema privado masivo ha resuelto esto.

## Decisión

El cliente ligero privado usable es un **bloqueante constitucional**, no un ítem de backlog. Si no existe una ruta viable que preserve privacidad, la ambición de adopción móvil masiva cae. Las opciones son: (a) restringir lanzamiento a full node o infra comunitaria, o (b) aceptar privacidad suicida — en cuyo caso el diseño ha fallado.

## Estado epistemológico

[BLOQUEANTE DE INVESTIGACIÓN]. Abierto. Sin solución conocida.

## Consecuencias

- research/light-client-lab existe para investigar, no para implementar "la solución"
- No se presenta el light client como feature a entregar en un roadmap
- Si el bloqueante no se cierra, se aplica downgrade: lanzamiento restringido

## Qué lo invalidaría

Evidencia de que cualquier diseño práctico requiere filtrar >50% de la actividad al proveedor, o que el coste de ancho de banda/batería hace el cliente inusable en móvil. Eso activa el kill criterion y obliga a simplificar.
