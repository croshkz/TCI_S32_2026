# ADR-0007: Trazabilidad a partir de movimientos de stock inmutables

- **Estado:** Aceptado
- **Fecha:** 2026-11-19
- **Responsable:** Cristian Hrynkiewicz

## Contexto

RN-06 pide reconstruir la historia interna de cada repuesto: pedido de compra → recepción (RN-08) → uso. El stock del repuesto es un número que se sobrescribe, así que por sí solo no dice de dónde vino ni a dónde fue cada unidad.

## Decisión

- Cada operación que cambia el stock registra, en la misma transacción, una fila en `movimientostock` con el tipo (`entrada`, `consumo`, `reserva`, `liberacion`), la cantidad, el usuario, la fecha y una **referencia al origen**: `REC-xxxx` (recepción), `INC-xxxx` (incidencia) o `RES-xxxx` (reserva).
- Los movimientos son **inmutables**: no se editan ni se borran. Una corrección se registra como un movimiento nuevo.
- `GET /repuestos/{codigo}/movimientos` devuelve el historial del repuesto en orden cronológico. Lo puede consultar cualquier usuario autenticado, incluida la Gerencia.
- Si una operación se rechaza (por ejemplo, por stock insuficiente), la transacción se revierte y no queda ningún movimiento.

## Alternativas consideradas

- **Reconstruir la historia uniendo recepciones, líneas de uso y reservas:** cada tabla tiene su forma y la consulta crece con cada tipo nuevo de operación.
- **Event sourcing completo (calcular el stock desde los movimientos):** más complejo de lo que pide el alcance. El stock se sigue guardando en el repuesto y los movimientos funcionan como registro de auditoría.

## Consecuencias

- La historia de un repuesto se obtiene con una sola consulta.
- El primer eslabón de RN-06 (el pedido de compra) todavía no existe. Cuando se implementen los pedidos (RN-03, RN-09), la recepción va a referenciar al pedido y la cadena queda completa.
- La tabla crece con cada operación. Con el volumen de una planta no hace falta paginar por ahora.
