## Tesis operativa del roadmap

El proyecto debe dividirse en dos capas de ambición:

**Núcleo plausible**

* dinero base privado por defecto
* no custodial
* sin PoS ni validadores visibles como soberanía
* cliente usable sin suicidio total de privacidad
* privacidad de red no opcional
* wallet honesta
* pagos rápidos como capa separada

**Capa especulativa**

* blockDAG privado viable
* unidad estable privada no custodial creíble
* disclosure empresarial robusto sin reconstrucción del grafo
* gobernanza multicapa sin élite técnica dominante

La regla es simple:

**primero se intenta probar el núcleo plausible.**
La capa especulativa solo entra si el núcleo sobrevive.

---

# Roadmap con hitos bien definidos

## Hito 0 — Replanteamiento formal del proyecto

### Objetivo

Corregir el error principal del corpus: dejar de tratar problemas abiertos como si fueran backlog normal.

### Qué se hace

Se reescribe el corpus en tres categorías:

1. **Convicciones estructurales**
2. **Hipótesis de diseño**
3. **Bloqueantes de investigación**

### Entregables

* Documento maestro reetiquetado
* Lista de invariantes no negociables
* Lista de hipótesis revocables
* Lista de bloqueantes constitucionales

### Criterio de salida

Todo el equipo acepta por escrito que:

* esto **no** es una arquitectura cerrada;
* esto **sí** es un programa de investigación con riesgo de aborto;
* la ambición total puede terminar reducida a una versión austera.

### Kill condition

Si aquí no se logra disciplina epistemológica, el resto del roadmap se contamina de autoengaño.

---

## Hito 1 — Viabilidad del dinero base privado

### Objetivo

Probar que el sistema puede tener una base monetaria privada con:

* notas privadas
* nullifiers
* conservación oculta
* auditabilidad agregada del suministro

### Qué se hace

Se trabaja solo la capa base monetaria, sin stable unit, sin gobernanza compleja, sin features de negocio amplias.

### Entregables

* Especificación formal del modelo de notas
* Diseño del esquema de commitments
* Diseño del esquema de nullifiers
* Modelo de conservación de valor oculto
* Modelo de emisión y quema auditable en agregado

### Criterio de salida

Se demuestra que un nodo independiente puede verificar:

* validez de gasto
* no doble gasto
* conservación de valor
* emisión permitida
* contabilidad agregada de supply

### Kill condition

Si no se puede auditar el supply agregado con alta confianza, el proyecto falla en su base.

### Observación brutal

Este hito no es “una parte más”.
Es uno de los dos o tres puntos que pueden matar todo.

---

## Hito 2 — Cliente ligero privado viable

### Objetivo

Responder la pregunta más peligrosa del proyecto:

**¿puede existir un cliente ligero usable que no revele casi toda la actividad del usuario?**

### Qué se hace

Se investiga solo esto:

* descubrimiento de notas
* sincronización remota
* pruebas locales
* multi-provider sync
* patrones de consulta ambiguos

### Entregables

* Prototipo de light client
* Modelo de sincronización
* Métricas de fuga de privacidad
* Evaluación móvil de batería, ancho de banda y latencia

### Criterio de salida

Se logra un cliente que:

* funcione en móvil,
* verifique localmente pruebas relevantes,
* no dependa de un proveedor único,
* y no permita a un proveedor reconstruir de forma trivial el grafo completo del usuario.

### Kill condition

Si la única forma práctica de usar el sistema es con un cliente que filtra la vida financiera al proveedor, **la ambición masiva muere**.

### Ruta de recorte

Si falla:

* se abandona la ambición masiva;
* se pasa a una arquitectura más elitista o self-hosted;
* o se termina en un sistema útil solo para usuarios avanzados.

---

## Hito 3 — Privacidad de red bajo condiciones reales

### Objetivo

Probar que la privacidad del ledger no queda anulada por IP, timing, patrones de sincronización o nodos espía.

### Qué se hace

Se evalúa:

* relay privacy
* difusión en dos etapas
* resistencia a spy nodes
* degradación honesta en móvil
* multi-provider networking

### Entregables

* Protocolo de transporte privado
* Simulación de inferencia de origen
* Pruebas de clustering por observador parcial
* Modelo de modos: fuerte / degradado / emergencia

### Criterio de salida

Se demuestra reducción material de:

* inferencia de origen
* clustering de wallets
* deanonymization por sync pattern

### Kill condition

Si la privacidad de red solo funciona en escritorio, con conectividad ideal o con costos de UX insoportables, el sistema queda relegado a laboratorio.

### Observación brutal

Sin este hito, lo que construyas no será dinero anónimo.
Será solo dinero con cifrado bonito.

---

## Hito 4 — Geometría del ledger: lineal vs blockDAG

### Objetivo

Resolver si el sistema puede soportar blockDAG privado o si eso debe descartarse.

### Qué se hace

Se comparan dos rutas:

**Ruta austera**

* PoW + cadena lineal + transacciones privadas

**Ruta ambiciosa**

* PoW + blockDAG + ordering determinístico + transacciones privadas

### Entregables

* Simulaciones de reorg
* Simulaciones de conflicto con nullifiers
* Costos de verificación
* Complejidad de implementación independiente
* Impacto sobre light client

### Criterio de salida

Elige una y solo una:

* **blockDAG sobrevive** porque aporta valor neto sin volver todo inmanejable;
* **blockDAG muere** y se cae a cadena lineal.

### Kill condition

Si el ordering del DAG con transacciones privadas no es auditable por equipos independientes, se descarta.

### Regla brutal

**No se insiste en DAG por orgullo.**
Si no sobrevive, se corta.

---

## Hito 5 — PoW realista y presupuesto de seguridad

### Objetivo

Cerrar la parte menos romantizada de PoW:

* qué función usar
* qué tan rápido centraliza
* qué tipo de minería favorece
* cómo se financia la seguridad

### Qué se hace

Se modela:

* memory-hard / CPU-biased PoW
* presión de pools
* presión de botnets
* presión de cloud
* efecto de emisión y fees

### Entregables

* Selección provisional de PoW
* Reporte de concentración minera
* Curva de emisión preliminar
* Modelo de security budget de largo plazo

### Criterio de salida

Se demuestra que:

* la captura no es trivial desde el inicio,
* el nodo y la verificación siguen siendo razonables,
* la emisión no mata la legitimidad ni el presupuesto de seguridad.

### Kill condition

Si la seguridad depende desde muy temprano de unos pocos pools o de fee market especulativo, hay que rediseñar PoW o emisión.

---

## Hito 6 — Wallet honesta y capa mínima de uso real

### Objetivo

Construir el primer sistema usable sin traicionar los invariantes.

### Qué se hace

Se implementa solo lo mínimo:

* wallet soberana
* wallet diaria
* pagos básicos
* recibos
* pruebas de pago acotadas
* estados de finality entendibles
* estados de privacidad visibles

### Entregables

* UX base de wallet
* Flujo de envío/recepción
* Flujo de merchant payment básico
* Receipt proof
* Payment proof
* Indicadores de privacidad y finality

### Criterio de salida

Un usuario no técnico puede:

* enviar,
* recibir,
* entender si está usando base o capa rápida,
* entender si está en modo fuerte o degradado,
* y no hacer errores catastróficos todo el tiempo.

### Kill condition

Si la única UX tolerable exige custodios ocultos, se frena el producto.

### Observación brutal

Este hito no es “hacer una app bonita”.
Es probar que el proyecto no necesita mentir para ser usable.

---

## Hito 7 — Disclosure mínimo y comercio limitado

### Objetivo

Demostrar que puede haber comercio sin transparencia por defecto.

### Qué se hace

Se limita la ambición a pruebas estrechas:

* prueba de pago
* prueba de recepción
* prueba de liquidación de factura
* recibos
* refund proof básico

No se entra todavía en auditorías complejas ni contabilidad empresarial completa.

### Entregables

* Catálogo mínimo de disclosure
* Pruebas scopeadas y temporales
* Flujo merchant → invoice → payment → receipt → refund

### Criterio de salida

Los casos de comercio simple funcionan sin exponer:

* historial completo,
* balances completos,
* relaciones comerciales completas.

### Kill condition

Si el uso comercial normal solo funciona mostrando demasiado, el objetivo de privacidad civil queda comprometido.

### Ruta de recorte

Se mantienen solo dos o tres tipos de prueba muy estrechos y se posterga todo lo demás.

---

## Hito 8 — Integrated adversarial testnet

### Objetivo

Dejar de validar piezas aisladas y ver si el sistema sobrevive junto.

### Qué se hace

Se monta un testnet hostil con:

* mineros adversarios
* proveedores hostiles
* relays espía
* merchants defectuosos
* clientes móviles
* fallos de red
* ataques de deanonymization
* simulaciones de crisis

### Entregables

* Testnet adversarial
* Reporte de fallas integradas
* Decisión de continuidad, simplificación o aborto

### Criterio de salida

No puede haber:

* falla constitucional activa,
* ni falla estructural sin plan claro de recorte.

### Kill condition

Si al juntar todo aparecen contradicciones insolubles, se simplifica o se detiene.

---

## Hito 9 — Decisión de bifurcación estratégica

Aquí el proyecto debe elegir uno de dos caminos.

### Camino A — Lanzamiento austero

Se acepta que lo viable hoy es algo cercano a:

* base privada fuerte
* PoW
* cadena lineal o DAG solo si ya sobrevivió
* light client aceptable
* privacidad de red razonable
* wallet honesta
* fast payments acotados
* disclosure mínimo
* sin stable unit al inicio

### Camino B — Investigación extendida

Solo si todo lo anterior sobrevivió se abre la siguiente frontera:

* stable unit
* disclosure empresarial más profundo
* gobernanza multicapa más formal
* operación comercial más compleja

### Regla brutal

**No se entra al Camino B por ansiedad de producto.**
Solo se entra si el Camino A ya es real.

---

## Hito 10 — Stable unit o descarte formal

### Objetivo

Responder si la unidad estable puede existir sin recentralizar el sistema.

### Qué se hace

Se modela una sola familia al inicio:

* sobrecolateralización
* liquidaciones
* aggregate solvency visibility
* depeg states
* treasury boundary

### Entregables

* Prototipo o paper técnico del stable layer
* Stress tests
* Depeg policy
* Treasury boundary charter

### Criterio de salida

La stable layer no debe:

* controlar la base,
* depender de un emisor central confiscable,
* exigir transparencia universal,
* ni esconder insolvencia.

### Kill condition

Si la estabilidad solo sale al costo de recentralizar, se descarta o se posterga indefinidamente.

### Observación brutal

Aquí es donde muchos proyectos mueren fingiendo que siguen vivos.

---

## Hito 11 — Gobernanza mecánica, no filosófica

### Objetivo

Convertir principios de gobernanza en mecanismos reales.

### Qué se hace

Se define:

* clases de cambio
* proceso de activación
* respuesta a emergencias
* multi-implementation conformance
* límites de cualquier grupo de coordinación
* sunset de poderes extraordinarios

### Entregables

* Charter de gobernanza
* Playbooks de emergencia
* Conformance suite
* Reglas de activación por clase

### Criterio de salida

La gobernanza deja de ser:

* eslogan,
* deseo,
* o moralina.

Y pasa a ser un sistema con:

* roles,
* límites,
* disparadores,
* y caducidad.

### Kill condition

Si todo termina dependiendo de un equipo central, una fundación o una “mesa temporal” que se eterniza, el proyecto no logró soberanía de protocolo.

---

# Orden recomendado, sin autoengaño

Este es el orden correcto:

1. **Hito 0** — Replanteamiento formal
2. **Hito 1** — Base monetaria privada
3. **Hito 2** — Cliente ligero privado
4. **Hito 3** — Privacidad de red
5. **Hito 4** — Lineal vs blockDAG
6. **Hito 5** — PoW + security budget
7. **Hito 6** — Wallet honesta + uso mínimo
8. **Hito 7** — Disclosure mínimo comercial
9. **Hito 8** — Testnet adversarial integrado
10. **Hito 9** — Decisión austera vs extendida
11. **Hito 10** — Stable unit solo si todo sobrevivió
12. **Hito 11** — Gobernanza mecánica final

---

# Qué se puede afirmar hoy y qué no

## Se puede afirmar hoy

* La separación entre base soberana y unidad estable es correcta.
* El descarte de PoS/dPoS/BFT visible para la base está bien encaminado.
* La privacidad de red no es opcional.
* Los kill criteria y downgrade paths son imprescindibles.
* El núcleo viable probable se parece más a una **evolución dura de Monero** que a una cadena completamente nueva ya resuelta.

## No se puede afirmar hoy

* Que blockDAG privado sea viable y auditable.
* Que exista ya un cliente ligero privado realmente usable.
* Que exista una stable unit privada no custodial convincente para este sistema.
* Que la gobernanza multicapa esté resuelta.
* Que el territorio completo sea cruzable.