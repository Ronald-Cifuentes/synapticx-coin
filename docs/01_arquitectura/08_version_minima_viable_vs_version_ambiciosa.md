# Versión mínima viable vs. versión ambiciosa

## Propósito

Este documento compara dos rutas: la versión mínima honesta y la versión ambiciosa / especulativa. Para cada componente se clasifica: entra en MVP, no entra en MVP, o depende de investigación abierta.

---

## 1. Tabla de componentes

| Componente | MVP | Ambiciosa | Depende de |
|------------|-----|-----------|------------|
| PoW como base | Sí | Sí | — |
| Cadena lineal | Sí (fallback) | No | blockDAG debe sobrevivir validación |
| blockDAG | No | Sí | [BLOQUEANTE] ordering + privado |
| Notas privadas + nullifiers | Sí | Sí | — |
| Supply correctness auditable | Requerido; no cerrado | Requerido | [BLOQUEANTE] construcción criptográfica; sin esto no hay MVP |
| Privacidad de red obligatoria | Sí | Sí | — |
| Relay/mixnet | Sí, con degraded modes | Sí | [BLOQUEANTE] usable en móvil |
| Full node | Sí | Sí | — |
| Cliente ligero privado | Solo si no suicida; si no, restringido | Sí, masivo | [BLOQUEANTE] constitucional |
| Pagos rápidos (acotados) | Sí, si diseño sobrevive | Sí | [HIPÓTESIS] no demostrado |
| Disclosure: pago, recibo, factura | Sí | Sí | — |
| Disclosure: nómina, auditoría, reservas | No | Sí | [BLOQUEANTE] composición |
| Unidad estable | No | Sí | [BLOQUEANTE] mecanismo vacío |
| Multi-implementación | No (objetivo) | Sí | [BLOQUEANTE] financiación, coordinación |
| Gobernanza formal completa | Principios | Mecanismos | [BLOQUEANTE] |

---

## 2. Versión mínima honesta

**Incluye:**
- PoW + cadena lineal (o blockDAG solo si validado)
- Notas privadas + nullifiers
- Supply correctness auditable
- Privacidad de red con modos degradados explícitos
- Full node como anchor
- Light client solo si existe diseño no suicida; si no, lanzamiento restringido
- Pagos rápidos con exposición acotada
- Disclosure: pago, recibo, factura
- Kill criteria y downgrade paths

**Excluye:**
- Unidad estable (pospuesta)
- Disclosure amplio (nómina, auditoría, reservas)
- Multi-implementación desde día uno
- Gobernanza con mecanismos completos

---

## 3. Versión ambiciosa / especulativa

**Añade:**
- blockDAG (si sobrevive validación)
- Cliente ligero móvil masivo
- Unidad estable overcollateralizada privada
- Disclosure amplio (nómina, auditoría, reservas)
- Multi-implementación desde inicio
- Mecanismos formales de gobernanza

**Condición:** Cada una de estas piezas depende de investigación abierta. No están cerradas. La versión ambiciosa es especulativa.

---

## 4. Mayor diferencia entre mínima y ambiciosa

| Dimensión | Mínima | Ambiciosa |
|-----------|--------|-----------|
| **Ledger** | Lineal, seguro | blockDAG, si viable |
| **Cliente** | Full node o light restringido | Light móvil masivo |
| **Unidad estable** | No | Sí, privada no custodial |
| **Disclosure** | Esencial (3 tipos) | Amplio (nómina, auditoría, reservas) |
| **Gobernanza** | Principios | Mecanismos + multi-implementación |

**Resumen:** La diferencia principal es que la versión ambiciosa asume que se resuelven los bloqueantes (cliente ligero, supply correctness, blockDAG, unidad estable, gobernanza). La versión mínima no los asume; opera dentro de lo que sí está cerrado o tiene downgrade path explícito.
