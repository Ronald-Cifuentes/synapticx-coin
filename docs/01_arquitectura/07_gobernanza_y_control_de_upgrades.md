# Gobernanza y control de upgrades

## Estado epistemológico del capítulo

- **Cerrado:** Principios: no monopolio de una implementación, no poder discrecional permanente, no captura de fundación. Clases de cambio (no-consenso, compatibilidad, consenso, constitucional, emergencia). Invariantes no alterables por gobernanza rutinaria.
- **Abierto:** Mecanismo de financiación de múltiples implementaciones. Coordinación de emergencias sin centralizar temporalmente. Composición y sunset de grupos de emergencia. Cómo distinguir pluralidad real de pluralidad cosmética.
- **Qué lo mataría:** Que una implementación defina el protocolo por sí sola; que el poder de emergencia se vuelva permanente; que la financiación compre autoridad constitucional.

---

## 1. Principios vs. mecanismo

[CONVICCIÓN ESTRUCTURAL] Los principios de gobernanza están claros: no monopolio, no poder permanente, no captura. Las invariantes (privacidad, no PoS, supply auditable, separación base/estable) no son alterables por gobernanza rutinaria.

[BLOQUEANTE DE INVESTIGACIÓN] "Principios de gobernanza" no equivalen a "mecanismo de gobernanza". El corpus no responde:

- Cómo se financia el desarrollo de múltiples implementaciones sin crear una fundación que se convierta en centro de poder.
- Cómo se coordina un fork de emergencia sin centralizar temporalmente el poder.
- Qué ocurre si los "múltiples implementadores" son en realidad el mismo equipo bajo distintos nombres. Cómo se distingue pluralidad real de cosmética.

---

## 2. Clases de cambio

[CONVICCIÓN ESTRUCTURAL] Los cambios se clasifican por severidad:

| Clase | Ejemplos | Carga de gobernanza |
|-------|----------|---------------------|
| No-consenso | Docs, UX, tooling | Baja |
| Compatibilidad | Performance, bugs sin cambio de reglas | Moderada |
| Consenso | Ordering, proof system, PoW params | Alta |
| Constitucional | Issuance, privacidad opcional, base/stable boundary | Extrema |
| Emergencia | Inflation bug, proof break, consensus split | Excepcional, acotada |

---

## 3. Poder de emergencia

[CONVICCIÓN ESTRUCTURAL] El poder de emergencia puede existir para: publicar avisos, coordinar parches, clasificar incidentes. No puede: convertirse en oficina soberana permanente, tomar control del treasury, redefinir política monetaria.

[KILL CRITERION] Si la coordinación de emergencia se vuelve estructura de gobierno permanente, el diseño ha fallado.

---

## 4. Multi-implementación

[HIPÓTESIS DE DISEÑO] Múltiples implementaciones independientes reducen riesgo de monopolio y captura. Es un objetivo razonable.

[BLOQUEANTE DE INVESTIGACIÓN] El mecanismo para alcanzarlo no está cerrado. Quién paga la segunda implementación, cómo se mantiene la conformance, cómo se evita que la "fundación" o el "equipo core" sean el real soberano a pesar de la formalidad de múltiples clientes — todo eso sigue abierto.

---

## 5. Resumen de etiquetas

| Componente | Etiqueta |
|------------|----------|
| Principios de gobernanza | [CONVICCIÓN ESTRUCTURAL] |
| No monopolio, no poder permanente | [CONVICCIÓN ESTRUCTURAL] |
| Mecanismo de gobernanza | [BLOQUEANTE DE INVESTIGACIÓN] |
| Poder de emergencia acotado | [CONVICCIÓN ESTRUCTURAL] |
| Emergencia permanente | [KILL CRITERION] |
