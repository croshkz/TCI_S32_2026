# ADR-0001: Concurrencia del stock con bloqueo de fila y CHECK en la base

- **Estado:** Aceptado
- **Fecha:** 2026-11-02
- **Responsable:** Tiziano Hurst

## Contexto

RN-01 exige que el stock físico nunca quede negativo, y RN-05 que lo reservado no se use en otra incidencia. Dos empleados pueden registrar el uso del mismo repuesto casi al mismo tiempo desde el celular. Si cada request lee el stock, valida y después escribe, los dos pueden leer el mismo valor, pasar la validación y dejar el stock en negativo (*lost update*).

## Decisión

1. **Bloqueo pesimista de la fila del repuesto.** Toda operación que modifica stock (uso, recepción, reserva, liberación, ejecución) lee el repuesto con `SELECT ... FOR UPDATE` (`RepuestoRepository.obtener_por_codigo(..., bloquear=True)`). La segunda transacción espera a que la primera haga commit y valida contra el valor ya actualizado.
2. **Orden fijo de bloqueo.** Primero se bloquea el repuesto y después la reserva, en todas las operaciones (`ReservaService._reserva_activa`). Así dos transacciones no quedan esperándose mutuamente (*deadlock*).
3. **CHECK en la tabla como última barrera.** `repuesto` tiene `CHECK (stock_fisico >= 0)`, y las líneas de uso, reservas y recepciones tienen `CHECK (cantidad >= 1)`. Si por un error de código se saltea una validación, la base rechaza la escritura y la transacción se revierte entera.

## Alternativas consideradas

- **Bloqueo optimista con columna de versión:** obliga a reintentar ante un conflicto. Con el volumen de una planta (pocos usos simultáneos del mismo repuesto), esperar unos milisegundos es más simple que reintentar.
- **`UPDATE repuesto SET stock_fisico = stock_fisico - :n WHERE stock_fisico >= :n`:** resuelve RN-01, pero no RN-05, que necesita sumar las reservas activas antes de decidir.
- **Validar solo en Python:** no protege ante concurrencia.

## Consecuencias

- RN-01 y RN-05 se cumplen aunque lleguen requests simultáneos sobre el mismo repuesto.
- Las operaciones sobre un mismo repuesto se serializan. Sobre repuestos distintos siguen siendo concurrentes.
- Depende de PostgreSQL (`FOR UPDATE`). Por eso los tests corren contra PostgreSQL y no contra SQLite.
- `test_rn01_descuento_por_uso.py` verifica que la CHECK rechaza un stock negativo escrito directamente en la base.
