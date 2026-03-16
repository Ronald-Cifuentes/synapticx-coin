# Estado privado y light clients

## Estado epistemológico del capítulo

- **Cerrado:** Full node como anchor de verdad. Clientes ligeros no deben filtrar vida financiera al proveedor. Modelo de notas con nullifiers.
- **Abierto:** Mecanismo de descubrimiento de notas para light clients. Protocolo de consulta que no revele grafo de actividad. Coste de verificación en dispositivos móviles.
- **Qué lo mataría:** Que la única ruta viable de light client requiera filtrar grafo de actividad al proveedor; que se acepte "confía en el indexer" como diseño.

---

## 1. Full node como anchor

[CONVICCIÓN ESTRUCTURAL] El full node es la fuente de verdad. Reconstruye y verifica estado canónico, raíces de compromiso, nullifiers, accounting de emisión. La validación no puede depender de un servicio remoto de confianza.

---

## 2. El problema del cliente ligero privado

### 2.1 Requisito invariante

[CONVICCIÓN ESTRUCTURAL] No se acepta un modelo donde la wallet móvil promedio filtre media vida financiera al nodo remoto.

Si el camino de adopción masiva exige que el usuario entregue su grafo de actividad a un proveedor, el sistema ha fallado su propósito.

### 2.2 Bloqueante constitucional

[BLOQUEANTE DE INVESTIGACIÓN] El cliente ligero privado usable es un bloqueante constitucional. No es un ítem de backlog; es una pregunta de investigación de alta gravedad sin solución conocida.

**El problema:** El descubrimiento de notas en un sistema privado requiere que el cliente obtenga datos. Si pide datos de forma identificable (por clave, por rango vinculado a wallet), filtra. Si pide todo y filtra localmente, el ancho de banda y la batería pueden ser prohibitivos. Los esquemas de consulta privada (PIR, etc.) son costosos o no escalan en este contexto.

**Estado actual:** Monero documenta debilidades de wallets ligeras. Ningún sistema privado masivo ha resuelto esto de forma satisfactoria.

[KILL CRITERION] Si no existe una ruta de cliente ligero que preserve privacidad de forma aceptable, la ambición masiva del proyecto cae. Las opciones son: (a) restringir lanzamiento a usuarios con full node o infraestructura comunitaria, o (b) aceptar que la adopción móvil masiva implica privacidad suicida — en cuyo caso el diseño ha fallado.

---

## 3. Si esto falla, cae gran parte de la ambición masiva

Si el cliente ligero privado no tiene solución viable:

- **Adopción masiva:** Requiere usuarios móviles. Sin light client usable y privado, la adopción queda restringida a usuarios técnicos con full node o infraestructura propia.
- **Comercio cotidiano:** Los comerciantes y usuarios ordinarios operan desde móvil. Sin light client privado, o se sacrifica privacidad (y se invalida el objetivo) o se excluye a la mayoría.
- **Capa de pagos rápidos:** Depende de wallets usables. Si la wallet es suicida para privacidad, la capa superior hereda el problema.
- **Disclosure:** Las pruebas de pago, recibo, etc. requieren que el usuario tenga acceso a su estado. Si ese acceso pasa por un proveedor que reconstruye el grafo, el disclosure se convierte en filtración.

**Conclusión:** El cliente ligero privado no es una feature. Es una condición de viabilidad para la ambición civil del proyecto. Su fracaso obliga a recortar alcance de forma drástica.

---

## 4. Direcciones de diseño (no cerradas)

[HIPÓTESIS DE DISEÑO] Posibles direcciones, ninguna demostrada:

- **Recuperación remota de candidatos con decripción local:** El cliente pide lotes de candidatos; descifra localmente cuáles le pertenecen. Riesgo: si los lotes son demasiado dirigidos, el proveedor puede inferir.
- **Consultas privadas (PIR, etc.):** Coste de ancho de banda y batería puede ser prohibitivo en móvil.
- **Múltiples proveedores:** Reduce visibilidad de un solo actor; no elimina la correlación si varios coluden.
- **Infraestructura comunitaria:** Usuarios con nodos propios o de confianza. Viable para minoría; no para adopción masiva.

---

## 5. Resumen de etiquetas

| Componente | Etiqueta |
|------------|----------|
| Full node como verdad | [CONVICCIÓN ESTRUCTURAL] |
| Light client no suicida | [CONVICCIÓN ESTRUCTURAL] |
| Cliente ligero privado viable | [BLOQUEANTE DE INVESTIGACIÓN] |
| Fracaso del light client | [KILL CRITERION] |
| Direcciones de diseño | [HIPÓTESIS DE DISEÑO] |
