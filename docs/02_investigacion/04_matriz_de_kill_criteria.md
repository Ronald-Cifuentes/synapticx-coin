# Matriz de kill criteria

## Propósito

Tabla severa con: criterio, síntoma, impacto, decisión requerida. Incluye campo de severidad: mata todo el programa / mata una capa / obliga a simplificar.

---

| Criterio | Síntoma | Impacto | Decisión requerida | Severidad |
|----------|---------|---------|--------------------|-----------|
| Cliente ligero requiere filtración catastrófica | Cualquier diseño práctico revela >50% de actividad al proveedor | Adopción masiva = privacidad suicida | Restringir a full node; abandonar ambición móvil masiva | Mata ambición fuerte |
| Supply correctness no auditable | No existe construcción que pruebe conservación sin revelar grafos | No se puede distinguir dinero sano de inflación | Abandonar visión de dinero privado auditable | Mata todo el programa |
| blockDAG ordering ambiguo o prohibitivo | Ordering no determinístico o verificación >200 ms/bloque | Geometría DAG inviable | Downgrade a cadena lineal | Obliga a simplificar |
| Privacidad de red inusable en móvil | Latencia >2 min o batería >8%/h para protección material | Usuarios normalizarán modo degradado | Modos degradados explícitos; no fingir protección | Obliga a simplificar |
| Stable unit requiere custodio único | Todo diseño creíble centraliza | Estabilidad contamina soberanía | Posponer capa estable | Mata capa estable |
| Uso empresarial requiere transparencia total | Bancos/auditores solo aceptan historial completo | Disclosure acotado inútil | Reducir tipos de prueba; o abandonar interoperabilidad legal amplia | Mata capa disclosure amplia |
| Ruta más fácil es custodial | UX empuja a custodios por defecto | Soberanía erosionada por producto | Rediseñar producto; rechazar custodia como path principal | Mata ambición fuerte |
| Una implementación define el protocolo | Segundo cliente no viable o no financiado | Monopolio de implementación | Aceptar monopolio temporal; o no lanzar hasta pluralidad | Obliga a simplificar |
| Emergencia se vuelve gobierno permanente | Grupo de emergencia no se disuelve | Captura por coordinación | Rediseñar gobernanza de emergencia | Mata gobernanza |

---

## Resumen por severidad

| Severidad | Criterios |
|-----------|-----------|
| **Mata todo el programa** | Supply correctness no auditable |
| **Mata ambición fuerte** | Cliente ligero suicida; ruta custodial |
| **Mata una capa** | Stable unit centralizada; disclosure inútil |
| **Obliga a simplificar** | blockDAG inviable; privacidad de red inusable; monopolio de implementación; emergencia permanente |
