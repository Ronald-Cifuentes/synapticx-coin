# Qué podría invalidar todo

## Propósito

Documento corto y brutal. Sin adornos. Qué hallazgos podrían obligar a abandonar la visión máxima.

---

## 1. Supply correctness no auditable

Si no existe construcción criptográfica que permita auditar emisión y conservación de valor sin exponer montos ni grafos, el sistema no puede distinguir dinero sano de inflación oculta. No hay downgrade. El programa de dinero privado auditable muere.

---

## 2. Cliente ligero siempre filtra

Si cualquier diseño práctico de light client requiere que el usuario revele al proveedor información que permite correlacionar la mayoría de su actividad, la adopción masiva implica privacidad suicida. La visión de dinero privado civilmente útil se invalida. Downgrade: restringir a full node. La visión máxima muere.

---

## 3. Ruta más fácil es custodial

Si la presión de producto y usabilidad hace que la ruta por defecto sea custodial (exchange, wallet custodial, indexer de confianza), el sistema ha traicionado su objetivo. La soberanía se erosiona por diseño. No hay parche. Hay que rediseñar o aceptar que el sistema no es soberano.

---

## 4. Dependencias cruzadas irresolubles

Si resolver un bloqueante invalida la solución de otro (ej. blockDAG que rompe light clients; light clients que debilitan privacidad de red; disclosure usable que abre compositional leakage), el programa puede no tener ruta coherente. La visión máxima asume que los bloqueantes son independientes o secuenciales. Si son contradictorios, no hay camino.

---

## 5. No existe equipo ni horizonte que lo cruce

Pregunta implícita: ¿Existe equipo, financiamiento y horizonte temporal que pueda resolver los bloqueantes en el orden definido sin que la solución de uno invalide otro? Si la respuesta es no, el programa es un mapa de un territorio que no se sabe si es cruzable. La visión máxima es especulativa; la mínima puede ser el techo real.

---

## Resumen

| Hallazgo | Efecto |
|----------|--------|
| Supply no auditable | Mata todo |
| Light client suicida | Mata ambición masiva |
| Ruta custodial por defecto | Mata soberanía |
| Bloqueantes contradictorios | No hay camino coherente |
| Recursos/horizonte insuficientes | Visión máxima especulativa |
