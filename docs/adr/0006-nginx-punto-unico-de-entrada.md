# ADR-0006: Nginx como punto único de entrada

- **Estado:** Aceptado
- **Fecha:** 2026-11-01
- **Responsable:** Nahuel Hernández Ulanio

## Contexto

El front (SPA) y la API son dos servicios distintos. Si el navegador llamara a la API en otro puerto, habría que habilitar CORS y el front tendría que conocer la URL de la API en cada entorno. Además, Swagger tiene que poder abrirse desde la misma URL que la aplicación.

## Decisión

- El contenedor `web` sirve el build del front con Nginx en el puerto 8080 y reenvía a la API ([`web/nginx.conf`](../../web/nginx.conf)):
  - `/api/*` → API, quitando el prefijo `/api`;
  - `/health`, `/docs` y `/openapi.json` → API, sin cambios.
- Cualquier otra ruta devuelve `index.html`, para que funcione el ruteo de la SPA.
- El contrato declara `servers: [{ url: /api }]`, así que el cliente del front usa rutas relativas.
- En desarrollo, Vite hace el mismo reenvío de `/api` hacia `localhost:8000`.

## Alternativas consideradas

- **Front y API en orígenes distintos con CORS:** más configuración y una URL distinta por entorno.

## Consecuencias

- Front y API comparten origen: no hace falta CORS.
- La aplicación, Swagger y el health check se acceden desde http://localhost:8080.
- El mock (Prism) no forma parte del despliegue. Solo se usa para desarrollar el front.
- Cada ruta nueva de la API que no vaya bajo `/api` necesita su propio `location` en `nginx.conf`.
