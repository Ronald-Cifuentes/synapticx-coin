# Product

## Propósito

Flujos de producto: wallet, merchant, business. **No** es implementación de app final. Son especificaciones de flujo, wireframes conceptuales y criterios de usabilidad para validar hipótesis de producto.

## Directorios

| Directorio | Contenido |
|------------|-----------|
| wallet-flows | Envío, recepción, distinción de capas, privacy mode, finality |
| merchant-flows | Factura, cobro, recibo, reembolso |
| business-flows | Nómina, disclosure, conciliación, auditoría acotada |

## Qué se investiga aquí

- ¿El usuario distingue settlement de pago rápido? (TP-004, H4)
- ¿La ruta más fácil es custodial? (Kill criterion)
- ¿Los flujos de merchant funcionan con disclosure acotado?
- ¿El usuario entiende privacy mode y finality?

## Qué NO debe meterse aquí

- App de producción antes de cerrar bloqueantes
- Flujos que asumen light client masivo si no está validado
- UX que oculta custodia o degradación de privacidad

## Bloqueante que intenta cerrar

Hipótesis H4 (capa de pagos rápidos) y H5 (wallet honesta). Kill criterion: ruta custodial por defecto.
