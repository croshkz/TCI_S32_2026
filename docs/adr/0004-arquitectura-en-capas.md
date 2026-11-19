# ADR-0004: Backend en capas: routers → services → repositories

- **Estado:** Aceptado
- **Fecha:** 2026-11-02
- **Responsable:** Tiziano Hurst

## Contexto

Las reglas de negocio (RN-01, RN-02, RN-05, RN-06, RN-08, RN-10) tienen que poder probarse y modificarse sin depender de HTTP ni de cómo se arman las consultas SQL.

## Decisión

El backend se organiza en tres capas, con dependencias en un solo sentido:

| Capa | Ubicación | Responsabilidad |
| --- | --- | --- |
| Routers | `app/routers/` | HTTP: parámetros, permisos por rol y conversión a los esquemas de respuesta. Sin reglas de negocio. |
| Services | `app/services.py` | Reglas de negocio y límites de transacción (un `commit` por operación). |
| Repositories | `app/repositories.py` | Consultas a la base (SQLModel), incluidos los bloqueos de fila. |

- Los errores de negocio se lanzan como excepciones de dominio (`ReglaDeNegocio`, `NoEncontrado`, `PermisoDenegado`) y un manejador global en `app/main.py` las traduce al formato `Error` del contrato.
- Los services reciben sus dependencias (sesión, notificador) por inyección de FastAPI (`app/dependencias.py`), lo que permite reemplazarlas en los tests.

## Alternativas consideradas

- **Lógica dentro de los endpoints:** más rápido al principio, pero mezcla HTTP, reglas y SQL, y hace difícil probar las reglas.

## Consecuencias

- Cada regla de negocio está en un solo lugar y se identifica con un comentario `RN-XX`.
- Un cambio de esquema de la base afecta a repositories y modelos, no a los routers.
- Agrega algo de código repetido entre capas.
