# ADR-0002: `openapi.yaml` es la fuente de verdad del contrato

- **Estado:** Aceptado
- **Fecha:** 2026-11-01
- **Responsable:** Cristian Hrynkiewicz

## Contexto

El front y el backend se desarrollan en paralelo y por personas distintas. En M2 el front se maquetó contra un mock antes de que existiera la API. Hacía falta un acuerdo único sobre rutas, campos y códigos de respuesta que no se desincronizara del código.

## Decisión

- El contrato vive en [`openapi.yaml`](../../openapi.yaml), en la raíz, y se escribe **antes** que el código (*contract-first*).
- El front usa un cliente tipado generado desde el contrato (`openapi-typescript` + `openapi-fetch`). Si el front llama a una ruta o a un campo que no existe, no compila.
- El backend se verifica contra el contrato en `test_contrato.py`: tiene que implementar exactamente las operaciones de `openapi.yaml`, con los mismos códigos de éxito.
- El CI valida el contrato (`redocly lint`) y falla si `web/src/api/schema.d.ts` no está regenerado (`pnpm check:cliente`).
- Mientras se desarrolla el front se puede usar el mock (Prism), que responde con los ejemplos del contrato.

## Alternativas consideradas

- **Code-first (generar el contrato desde FastAPI):** el contrato cambiaría cada vez que alguien toca un modelo, sin una revisión explícita, y el front no podría empezar antes que el backend.
- **Cliente escrito a mano:** sin verificación de tipos contra el contrato.

## Consecuencias

- Todo cambio de API empieza por un cambio en `openapi.yaml`, que se revisa en el PR.
- Hay que commitear `schema.d.ts` junto con el contrato.
- [`M2/openapi.yaml`](../../M2/openapi.yaml) queda congelado como entrega del hito M2. La versión vigente es la de la raíz.
