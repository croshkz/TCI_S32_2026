# Registro de decisiones de arquitectura (ADR)

Cada ADR documenta una decisión que condiciona el diseño: el contexto, qué se decidió y qué consecuencias trae. Un ADR aceptado no se edita para cambiar la decisión: si cambia, se escribe uno nuevo que lo reemplaza y el viejo se marca como `Reemplazado por ADR-XXXX`.

El responsable de cada ADR lo mantiene al día y revisa los PR que tocan esa decisión.

| ADR | Decisión | Estado | Responsable |
| --- | --- | --- | --- |
| [0001](0001-concurrencia-del-stock.md) | Concurrencia del stock: bloqueo de fila + CHECK en la base | Aceptado | Tiziano Hurst |
| [0002](0002-contrato-openapi-fuente-de-verdad.md) | `openapi.yaml` es la fuente de verdad del contrato | Aceptado | Cristian Hrynkiewicz |
| [0003](0003-autenticacion-jwt.md) | Autenticación con JWT y rol firmado en el token | Aceptado | Tiziano Hurst |
| [0004](0004-arquitectura-en-capas.md) | Backend en capas: routers → services → repositories | Aceptado | Tiziano Hurst |
| [0005](0005-notificaciones-por-puerto.md) | Notificaciones detrás de un puerto, con adaptador de log | Aceptado | Nahuel Hernández Ulanio |
| [0006](0006-nginx-punto-unico-de-entrada.md) | Nginx como punto único de entrada | Aceptado | Nahuel Hernández Ulanio |
| [0007](0007-trazabilidad-por-movimientos.md) | Trazabilidad a partir de movimientos de stock inmutables | Aceptado | Cristian Hrynkiewicz |

## Plantilla

```markdown
# ADR-XXXX: Título corto

- **Estado:** Propuesto | Aceptado | Reemplazado por ADR-YYYY
- **Fecha:** AAAA-MM-DD
- **Responsable:** Nombre Apellido

## Contexto
Qué problema hay y qué restricciones aplican.

## Decisión
Qué se decidió.

## Alternativas consideradas
Qué otras opciones había y por qué no se eligieron.

## Consecuencias
Qué se gana, qué se pierde y qué queda pendiente.
```
