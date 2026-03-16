# Lo que hoy sí sería honesto intentar construir

## Qué sí construir ya

**Solo prototipos mínimos para validar hipótesis.** No implementación de protocolo.

| Qué | Dónde | Objetivo |
|-----|-------|----------|
| Prototipo de ordering DAG | research/consensus-lab, simulations/dag-ordering | Validar si blockDAG + nullifiers produce orden determinístico |
| Circuito de conservación de valor | research/privacy-lab | Validar si supply correctness es auditable sin revelar grafos |
| Prototipo de light client que pide lotes | research/light-client-lab | Medir correlación que un proveedor puede inferir |
| Relay staging (Dandelion-like) | research/network-lab | Medir inferencia de origen vs. gossip plano |
| Modelo formal de composición de disclosure | research/disclosure-lab, simulations/disclosure-composition | Medir % de grafo reconstruible con N pruebas |
| Fixtures y vectores de conformance | conformance/ | Para que los prototipos tengan casos de prueba |

---

## Qué solo prototipar

**No implementar como producción.** Solo validar viabilidad.

| Qué | Razón |
|-----|-------|
| blockDAG completo | Si el prototipo de ordering falla, downgrade a lineal |
| Sistema de pruebas ZK | Si no existe construcción, kill criterion |
| Light client móvil | Si correlación >50%, aborto de ambición masiva |
| Mixnet/relay | Si latencia o batería inusable, modos degradados |
| Unidad estable | Mecanismo vacío; solo diseño y simulación de estrés |

---

## Qué no tocar todavía

**No iniciar hasta que lo anterior produzca evidencia favorable.**

| Qué | Bloqueante que debe cerrar primero |
|-----|-----------------------------------|
| Implementación de nodo completo | Supply correctness, consensus ordering |
| Implementación de wallet de producción | Light client viable o decisión de restringir |
| Capa de pagos rápidos | Hipótesis H4; base debe existir |
| Unidad estable | Bloqueante B5; base + pagos deben existir |
| Multi-implementación | Gobernanza; no es prioridad hasta que el protocolo exista |
| Mainnet, testnet público | Todos los kill criteria deben estar en verde o con downgrade aceptado |

---

## Orden de intento

1. **Supply correctness** — Prototipo de circuito. Si falla, no hay programa.
2. **Consensus ordering** — Prototipo DAG. Si falla, downgrade a lineal.
3. **Light client** — Prototipo de consulta. Si falla, restringir ambición.
4. **Network privacy** — Prototipo de relay. Si falla, modos degradados.
5. **Producto mínimo** — Solo después de 1–4. Flujos de wallet, merchant.
6. **Disclosure** — Solo después de 5. Composición.
7. **Stable unit** — Solo si la visión la exige y 1–6 están cerrados.
8. **Gobernanza** — Última. Depende de qué capas sobrevivan.

---

## Resumen

Hoy sería honesto: construir prototipos de investigación para los bloqueantes, en el orden definido. No sería honesto: escribir código de nodo, wallet o protocolo como si fuera mainnet-ready; tratar los bloqueantes como backlog; o presentar la versión máxima como alcanzable.
