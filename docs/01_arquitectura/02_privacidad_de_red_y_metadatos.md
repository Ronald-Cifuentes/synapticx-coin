# Privacidad de red y metadatos

## Estado epistemológico del capítulo

- **Cerrado:** Privacidad de red es obligatoria, no opcional. "Usa Tor por tu cuenta" no es diseño suficiente. El ledger privado sin transporte privado es incompleto.
- **Abierto:** Mecanismo concreto (mixnet, relay staging, Dandelion-like). Usabilidad en móvil bajo restricciones de batería y latencia.
- **Qué lo mataría:** Que la privacidad de red sea tratada como opcional; que el diseño asuma que el usuario se protege por su cuenta.

---

## 1. Por qué privacidad de ledger no basta

[CONVICCIÓN ESTRUCTURAL] La privacidad del ledger es insuficiente si el transporte filtra IP, timing, patrones de retransmisión y tipo de cliente.

Un observador con visibilidad parcial de red puede inferir origen de transacciones, agrupar comportamiento de wallets y correlacionar actividad sin romper criptografía. La capa de red debe ser parte del modelo de amenazas, no una práctica opcional.

### 1.1 Privacidad de red obligatoria

[CONVICCIÓN ESTRUCTURAL] La capa base debe asumir mixnet, relay privacy o un sistema equivalente. No se acepta "usa Tor por tu cuenta" como diseño suficiente.

---

## 2. Objetivos de la capa de red

- **Origen ambiguo:** Un observador remoto no debe distinguir trivialmente originador, relay o re-broadcaster.
- **Timing de-correlacionado:** Reducir la fiabilidad de inferencia por timing.
- **Resistencia a spy nodes:** Un conjunto de peers hostiles no debe poder agrupar comportamiento de wallet con alta confianza.
- **Resistencia a eclipse:** Dificultar el aislamiento de un nodo o wallet en una vista maliciosa.

---

## 3. Red privada usable en móvil

[BLOQUEANTE DE INVESTIGACIÓN] La red privada usable en móvil sigue siendo un reto central. Los mixnets añaden latencia. El móvil tiene restricciones de batería, conectividad intermitente y ancho de banda. El trade-off entre protección de metadatos y experiencia usable no está resuelto.

[DOWNGRADE PATH] Si la privacidad de red es inusable en móvil: definir modos degradados explícitos y comunicarlos con honestidad al usuario. No fingir protección fuerte cuando no la hay.

---

## 4. Modos degradados explícitos

[CONVICCIÓN ESTRUCTURAL] Cuando la privacidad de red se degrada (conectividad débil, relay no disponible, etc.), el sistema debe degradar de forma explícita, no silenciosa.

| Modo | Descripción | Comunicación al usuario |
|------|-------------|-------------------------|
| Fuerte | Relay/mixnet disponible, multi-provider sano | "Privacidad de red activa" |
| Reducido | Funcionalidad intacta, protección de metadatos debilitada | Advertencia visible |
| Emergencia | Fondos operables, privacidad de red materialmente debilitada | Advertencia clara; no mostrar "privado" genérico |

[KILL CRITERION] Si los modos degradados son silenciosos y el usuario cree estar protegido cuando no lo está, el diseño falla en honestidad.

---

## 5. Resumen de etiquetas

| Componente | Etiqueta |
|------------|----------|
| Privacidad de red obligatoria | [CONVICCIÓN ESTRUCTURAL] |
| Ledger solo no basta | [CONVICCIÓN ESTRUCTURAL] |
| Red privada en móvil | [BLOQUEANTE DE INVESTIGACIÓN] |
| Modos degradados explícitos | [CONVICCIÓN ESTRUCTURAL] |
| Degradación silenciosa | [KILL CRITERION] |
