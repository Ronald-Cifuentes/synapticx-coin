# Mapa epistemológico del corpus

## Propósito

Este documento clasifica el corpus completo según la taxonomía obligatoria. Debe quedar claro qué partes son sólidas (convicciones), cuáles son especulativas (hipótesis o bloqueantes) y cuáles están explícitamente descartadas.

---

## A. Convicciones estructurales

| Afirmación | Fuente | Justificación |
|------------|--------|---------------|
| La base debe ser privada por defecto | PRD, Spec 03, 06 | Invariante; no depende de investigación futura |
| No PoS/dPoS/BFT visible en capa base | PRD, Spec 01, 09 | Descarte estructural justificado |
| Privacidad de red obligatoria | PRD, Spec 05 | Parte del modelo de amenazas |
| Separación base / unidad estable | PRD, Spec 07 | Decisión conceptual; la base no es estable |
| Disclosure acotado, no transparencia total | PRD, Spec 06 | Objetivo de interoperabilidad legal |
| No custodios en la base | PRD, criterios de descarte | Validez no depende de terceros |
| Supply correctness debe ser auditable en agregado | Spec 03, RF-4 | Requisito de integridad monetaria |
| Clientes ligeros no deben filtrar vida financiera | PRD 4.6, Spec 04 | Invariante; mecanismo puede estar abierto |
| Kill criteria y downgrade paths son necesarios | Spec 11, C-02 | Disciplina anti-autoengaño |
| Modelo de notas privadas con nullifiers | Spec 03 | Forma de representar estado; compatible con invariantes |

---

## B. Hipótesis de diseño

| Afirmación | Fuente | Estado |
|------------|--------|--------|
| PoW es la piedra angular menos mala | Spec 01, 02 | Razonable por descarte de PoS; no demostrado para esta combinación |
| blockDAG con ordering determinístico es viable | Spec 01 | Preferencia condicional; fallback a lineal |
| Capa de pagos rápidos separada mejora UX sin romper soberanía | Spec 02 (Task Breakdown), U-01 | Inspiración Cashu/Fedimint; no confirmado |
| Selective disclosure puede servir comercio real | Spec 06 | Dirección Penumbra; composición no resuelta |
| Wallet honesta puede reducir traición por producto | Spec 10 | Objetivo de UX; no validado |
| Memory-hard PoW retrasa oligopolio | Spec 02 | Menos malo que ASIC-first; presión sigue existiendo |
| Overcollateralización es familia preferida para stable | Spec 07 | Filosóficamente correcta; mecanismo vacío |
| Fair-launch + tail emission preserva security budget | Spec 08 | Coherente; no probado bajo estrés |
| Multi-implementación evita monopolio | Spec 09 | Principio correcto; mecanismo de financiación abierto |

---

## C. Bloqueantes de investigación

| Bloqueante | Fuente | Gravedad | Kill/Downgrade asociado |
|------------|--------|----------|-------------------------|
| Cliente ligero privado usable sin filtración catastrófica | Spec 04, RB-05 | Constitucional | Kill: si no existe ruta viable, arquitectura falla |
| Supply correctness bajo privacidad fuerte | Spec 03, RB-06 | Constitucional | Kill: si no auditable, diseño inválido |
| blockDAG + transacciones privadas + ordering manejable | Spec 01, RB-01 | Estructural | Downgrade: cadena lineal |
| Sistema de pruebas para conservación oculta + nullifiers + issuance | Spec 03, RB-03 | Criptográfico de primer orden | No es "elegir familia ZK"; es diseño de circuito |
| Red de transporte privada usable en móvil | Spec 05, RB-07 | Operacional | Degraded mode explícito si falla |
| Unidad estable privada no custodial creíble | Spec 07, RB-12 | Económico | Downgrade: posponer capa estable |
| Gobernanza multiimplementación no capturada | Spec 09, RB-13 | Político | Sin mecanismo de financiación definido |
| Disclosure composition no reconstruye grafo completo | Spec 06, RB-09 | Legal/interoperabilidad | Downgrade: reducir tipos de prueba |

---

## D. Descartes estructurales

| Enfoque descartado | Razón |
|-------------------|-------|
| PoS, dPoS, BFT visible como base | Convierte capital previo en poder de consenso; capturable |
| Privacidad opcional | Fragmenta conjunto de anonimato; degrada fungibilidad |
| Custodios en capa base | Punto único de fallo; contradice soberanía |
| Transparencia total para legalidad | Invalida objetivo de privacidad civil |
| eCash/Cashu/Fedimint como núcleo soberano | Custodian fondos; no son settlement base |
| "Usa Tor por tu cuenta" como diseño | Privacidad opcional es débil |
| ASIC-maximalist PoW como target | Oligopolio hardware demasiado rápido |
| Algoritmo reflexivo puro para stable | Frágil bajo pánico; no creíble |
| Un solo implementador define protocolo | Riesgo de monopolio y captura |

---

## E. Resumen por solidez

| Categoría | Cantidad aproximada | Implicación |
|-----------|---------------------|-------------|
| Convicciones estructurales | ~10 | Sólidas; no se negocian |
| Hipótesis de diseño | ~9 | Plausibles; pueden fallar |
| Bloqueantes de investigación | ~8 | Sin solución conocida; pueden matar o simplificar |
| Descartes estructurales | ~9 | Excluidos por diseño |

---

## F. Zonas de mayor incertidumbre

1. **Consenso × estado privado:** Ordering en DAG con nullifiers y reorgs. Complejidad no modelada completamente.
2. **Estado privado × cliente ligero:** Descubrimiento de notas sin filtrar grafo. Problema abierto.
3. **Privacidad de red × UX móvil:** Latencia y batería vs. protección de metadatos. Trade-off no resuelto.
4. **Capa estable × privacidad:** Overcollateralización privada con oráculos y liquidaciones. Mecanismo vacío.
5. **Gobernanza × pluralidad real:** Cómo financiar múltiples implementaciones sin fundación central.
