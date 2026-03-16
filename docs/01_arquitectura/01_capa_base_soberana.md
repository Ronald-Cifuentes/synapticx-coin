# Capa base soberana

## Estado epistemológico del capítulo

- **Cerrado:** Invariantes de diseño (privacidad por defecto, no PoS, no custodios, supply auditable). Descarte de PoS/dPoS/BFT visible.
- **Abierto:** PoW concreto, geometría del ledger (lineal vs. blockDAG), sistema de pruebas para conservación oculta.
- **Qué lo mataría:** Supply correctness no auditable; consenso que dependa de stake o validadores visibles; privacidad opcional.

---

## 1. Invariantes de la capa base

### 1.1 Privacidad por defecto

[CONVICCIÓN ESTRUCTURAL] La capa base debe ser privada por defecto. No existe modo transparente coexistente.

Si la privacidad es opcional, el conjunto de anonimato se fragmenta y la fungibilidad se degrada. Los usuarios en modo transparente se convierten en outliers identificables.

### 1.2 No custodial

[CONVICCIÓN ESTRUCTURAL] La validez del settlement no puede depender de custodios. El gasto debe ser verificable sin confiar en terceros.

La custodia reintroduce punto único de fallo y captura. Se mantiene aunque existan capas superiores con modelos custodiales acotados (ej. eCash con exposición limitada).

### 1.3 No PoS / dPoS / BFT visible

[DESCARTADO] PoS, dPoS y BFT con validadores visibles están rechazados para la capa base.

**Razones:** Convierten capital previo en poder de consenso; producen actores visibles y regulables; facilitan captura a través de custodios de stake. Para un sistema cuyo objetivo prioritario es resistencia a captura, el mecanismo de stake es estructuralmente incompatible.

### 1.4 Supply correctness auditable en agregado

[CONVICCIÓN ESTRUCTURAL] El suministro total debe poder auditarse con garantías suficientes para descartar inflación, sin exponer la vida financiera de los usuarios.

[KILL CRITERION] Si supply correctness no es independientemente auditable, el diseño falla constitucionalmente.

---

## 2. PoW como base de consenso

### 2.1 PoW por descarte

[HIPÓTESIS DE DISEÑO] PoW es la piedra angular menos mala para este objetivo. No se elige por pureza; se elige porque el descarte de PoS deja PoW como la opción que ancla el coste de ataque a un recurso externo, no a tenencia previa.

**Lo que no se afirma:** Que PoW sea perfecto. Pools, presión energética, geografía, latencia probabilística y deriva a hardware especializado son heridas abiertas.

### 2.2 Memory-hard, commodity-accessible

[HIPÓTESIS DE DISEÑO] La familia PoW preferida es memory-hard y accesible a hardware commodity, para retrasar oligopolio ASIC. No elimina la especialización; la retrasa y la hace más costosa.

---

## 3. Geometría del ledger: lineal vs. blockDAG

### 3.1 blockDAG como target condicional

[BLOQUEANTE DE INVESTIGACIÓN] PoW + blockDAG + transacciones privadas es una combinación que nadie ha implementado satisfactoriamente. Requiere:

- Ordering determinístico sobre un DAG.
- Resolución de conflictos vía nullifiers con transacciones ocultas.
- Verificación de pruebas ZK sobre un grafo paralelo.
- Reorgs bien definidos bajo ordering complejo.

La interacción entre estos elementos puede ser computacionalmente prohibitiva o lógicamente ambigua. No está cerrada.

[DOWNGRADE PATH] Si blockDAG no sobrevive validación adversarial: downgrade a cadena lineal PoW. Se preserva consenso y privacidad; se pierde throughput paralelo.

### 3.2 Modelo de notas y nullifiers

[CONVICCIÓN ESTRUCTURAL] El modelo de estado usa notas privadas con nullifiers como marcadores de conflicto públicos. Cada gasto revela un nullifier único; la duplicación indica double spend.

La forma concreta (árbol de compromisos, acumulador, sistema de pruebas) sigue abierta. La decisión de usar nullifiers como puente entre privacidad y consenso es estructural; la implementación criptográfica es [BLOQUEANTE DE INVESTIGACIÓN].

---

## 4. Resumen de etiquetas

| Componente | Etiqueta |
|------------|----------|
| Privacidad por defecto | [CONVICCIÓN ESTRUCTURAL] |
| No custodial | [CONVICCIÓN ESTRUCTURAL] |
| No PoS/dPoS/BFT | [DESCARTADO] |
| Supply auditable | [CONVICCIÓN ESTRUCTURAL] + [KILL CRITERION] |
| PoW como base | [HIPÓTESIS DE DISEÑO] |
| blockDAG + privado | [BLOQUEANTE DE INVESTIGACIÓN] + [DOWNGRADE PATH] |
| Notas + nullifiers (modelo) | [CONVICCIÓN ESTRUCTURAL] |
| Implementación criptográfica | [BLOQUEANTE DE INVESTIGACIÓN] |
