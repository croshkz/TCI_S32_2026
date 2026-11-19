# Sistema de Gestión de Stock y Mantenimiento de Planta

[![CI](https://github.com/croshkz/TCI_S32_2026/actions/workflows/ci.yml/badge.svg)](https://github.com/croshkz/TCI_S32_2026/actions/workflows/ci.yml)

Trabajo de Campo Integrador · Desarrollo de Software 2026 · Comisión S32 · UTN FR La Plata · Grupo 3

Sistema para que el personal de una planta reporte fallas en las máquinas, registre qué repuestos usa en cada reparación y mantenga el stock al día. El caso de uso principal es **CU-01: Registrar uso de repuesto** ([especificación](docs/spec/EntregaM1.md)).

## Integrantes

| Legajo | Nombre y apellido | Email |
| --- | --- | --- |
| 33112 | HRYNKIEWICZ, CRISTIAN | croshkz@gmail.com |
| 33629 | Tiziano Hurst | tizihurst@gmail.com |
| 33292 | HERNANDEZ ULANIO, NAHUEL | nahuelulanio1@gmail.com |

## Arquitectura

```
navegador ──► web (Nginx :8080) ──/api/*──► api (FastAPI :8000) ──► db (PostgreSQL :5432)
                                  /health, /docs, /openapi.json──►

mock (Prism :4010): sirve respuestas de ejemplo de openapi.yaml, solo para desarrollo del front
```

| Servicio | Tecnología | Qué hace |
| --- | --- | --- |
| `web` | React + Vite, servido por Nginx | Front. Nginx sirve los estáticos y reenvía `/api/*`, `/health`, `/docs` y `/openapi.json` a la API. |
| `api` | FastAPI + SQLModel + Alembic | Reglas de negocio, autenticación JWT y persistencia. Capas: routers → services → repositories. |
| `db` | PostgreSQL 16 | Base de datos. Los datos persisten en el volumen `datos-postgres`. |
| `mock` | Prism | Mock del contrato. El producto desplegado **no** lo usa. |

El contrato de la API es [`openapi.yaml`](openapi.yaml) y es la fuente de verdad: el backend se valida contra él y el cliente del front se genera a partir de él (ver [Contrato y cliente generado](#contrato-y-cliente-generado)).

## Levantar el sistema

Requisito: [Docker Desktop](https://www.docker.com/products/docker-desktop/) (o Docker Engine con el plugin Compose).

```bash
git clone https://github.com/croshkz/TCI_S32_2026.git
cd TCI_S32_2026
docker compose up --build
```

Cuando los servicios estén listos:

| Qué | URL |
| --- | --- |
| Aplicación web | http://localhost:8080 |
| Documentación interactiva de la API (Swagger) | http://localhost:8080/docs |
| Especificación OpenAPI que sirve la API | http://localhost:8080/openapi.json |
| Estado del backend | http://localhost:8080/health |

Swagger también responde directo en http://localhost:8000/docs. El selector **Servers** decide a dónde van los requests de *Try it out*: `/api` pasa por Nginx (es la opción predeterminada) y `/` va directo a la API. Si abrís Swagger en el puerto 8000, elegí `/`.

Al arrancar, el contenedor `api` aplica las migraciones (`alembic upgrade head`) y carga los datos de ejemplo (`python -m app.seed`). El seed solo carga datos si las tablas están vacías, así que reiniciar los contenedores no duplica nada.

Comandos útiles:

```bash
docker compose logs -f api   # ver los avisos de alerta de stock y de reservas liberadas
docker compose down          # apagar, conservando los datos
docker compose down -v       # apagar y BORRAR la base, para volver al estado inicial del seed
```

La clave con la que se firman los tokens se toma de la variable `JWT_SECRET`. Si no está definida, Compose usa una clave de desarrollo; en cualquier otro entorno hay que definirla:

```bash
JWT_SECRET="una-clave-larga-y-secreta-de-al-menos-32-caracteres" docker compose up --build
```

## Cuentas de demo

Todas usan la contraseña **`planta2026`**.

| Usuario | Rol | Puede |
| --- | --- | --- |
| `operario` | Operario | Reportar incidencias. |
| `mantenimiento` | Mantenimiento | Lo anterior, más pasar incidencias a reparación, registrar uso de repuestos, cargar stock, reservar y ejecutar reservas. |
| `encargado` | Encargado | Todo lo de Mantenimiento, más **liberar reservas** (RN-05). |
| `gerencia` | Consulta | Solo consultar. |

El rol viaja firmado dentro del token JWT y la API lo verifica en cada request. Una operación sin token devuelve `401`; una operación que el rol no tiene permitida devuelve `403`.

## Datos iniciales

| Dato | Valor |
| --- | --- |
| Repuesto `REP-6204` | Rodamiento 6204 · stock 12 · mínimo 5 · ubicación A-03-12 |
| Repuesto `REP-0100` | Correa dentada HTD 8M · stock 3 · mínimo 2 · ubicación B-01-04 |
| Incidencia `INC-0001` | Caldera 2 · en reparación |
| Incidencia `INC-0002` | Fraccionador 1 · en reparación |
| Máquinas | `MAQ-0001` Caldera 2 · `MAQ-0002` Fraccionador 1 · `MAQ-0003` Banda 3 |
| Ubicaciones | `A-03-12` · `A-03-13` · `B-01-04` |

## Flujo demo de punta a punta

Los números suponen la base recién creada. Si ya la usaste, corré `docker compose down -v` y después `docker compose up --build`.

### Parte 1: en la aplicación web (http://localhost:8080)

1. **Reportar una falla.** Ingresá como `operario`. En **Incidencia**, escribí el código de máquina `MAQ-0003` (Banda 3) y la descripción "Banda desalineada", y enviá. Se crea `INC-0003` en estado `REPORTADA`.
2. **Registrar uso de un repuesto (CU-01, RN-01).** Salí e ingresá como `mantenimiento`. En **Registrar uso** ya viene cargado `REP-6204` (Rodamiento 6204) con stock disponible 12. Elegí el destino `INC-0001 · Caldera 2`, cantidad 3, y tocá **Registrar uso**. Aparece "Uso registrado. Stock resultante: 9", sin alerta.
3. **Alerta de stock mínimo (RN-02).** Registrá otro uso, cantidad 4. El stock queda en 5, igual al mínimo, y aparece el aviso "El stock llegó al mínimo. El repuesto pasa a la lista de compras.". La alerta también queda en `docker compose logs api`.
4. **Stock insuficiente.** Intentá usar 20 unidades. Aparece "La cantidad supera el stock disponible (5)." y el stock no cambia.
5. **Cargar stock recibido.** En **Cargar stock**, con `REP-6204` cargado, completá lote `L-2026-045`, cantidad 10, ubicación `A-03-12` y tocá **Cargar stock**. Aparece "Stock cargado. Stock resultante: 15".

### Parte 2: reservas en Swagger (http://localhost:8080/docs)

Las reservas todavía no tienen pantalla en el front; se prueban desde Swagger.

1. Ejecutá `POST /auth/login` con `{"usuario": "mantenimiento", "password": "planta2026"}`, copiá el `access_token`, tocá **Authorize** y pegalo.
2. **Reservar (RN-05).** `POST /reservas` con `{"repuesto_codigo": "REP-6204", "cantidad": 10, "motivo": "Preventivo caldera"}`. Responde físico 15, reservado 10, disponible 5, y genera la alerta de umbral.
3. **Lo reservado no se usa en otra incidencia.** `POST /repuestos/REP-6204/usos` con `{"destino_id": "INC-0002", "cantidad": 6}`. Responde `409 STOCK_RESERVADO`.
4. **Solo el Encargado libera.** `POST /reservas/RES-0001/liberacion` con el token de `mantenimiento` responde `403`. Repetí el login con `encargado`, volvé a autorizar y ejecutá la liberación: responde `200`, la reserva queda `LIBERADA` y el aviso aparece en `docker compose logs api`.
5. **Trazabilidad (RN-06).** `GET /repuestos/REP-6204/movimientos` devuelve la historia del repuesto en orden: los consumos en `INC-0001`, la recepción `REC-0001`, la reserva `RES-0001` y su liberación. Cualquier rol puede consultarla.
6. **Pasar la incidencia nueva a reparación.** Con `mantenimiento`, `POST /incidencias/INC-0003/reparacion`. A partir de ahí `INC-0003` aparece como destino válido en **Registrar uso**.

## Tests

La suite corre en GitHub Actions en cada push a `main` y en cada Pull Request ([ver ejecuciones](https://github.com/croshkz/TCI_S32_2026/actions/workflows/ci.yml)). El CI tiene dos jobs:

- **API:** levanta PostgreSQL, aplica las migraciones sobre una base vacía y corre `pytest`.
- **Contrato y web:** valida `openapi.yaml`, verifica que el cliente generado esté sincronizado con el contrato y compila el front.

Para correrla en tu máquina necesitás Docker y [uv](https://docs.astral.sh/uv/):

```bash
docker compose up -d --wait db
cd api
uv run pytest -q
```

O desde la raíz, con pnpm: `pnpm test`.

Los tests usan una base aparte (`planta_test`), que se crea sola y se vacía antes de cada test, así que no tocan los datos de la demo.

| Archivo | Qué cubre |
| --- | --- |
| [`test_rn01_descuento_por_uso.py`](api/tests/test_rn01_descuento_por_uso.py) | RN-01: el uso descuenta del stock físico y el stock nunca queda negativo. |
| [`test_rn02_umbral.py`](api/tests/test_rn02_umbral.py) | RN-02: alerta cuando el disponible queda en el mínimo o por debajo. |
| [`test_rn05_reservas.py`](api/tests/test_rn05_reservas.py) | RN-05: lo reservado no se usa en otra incidencia; solo el Encargado libera, con aviso inmediato. |
| [`test_rn06_trazabilidad.py`](api/tests/test_rn06_trazabilidad.py) | RN-06: historial de movimientos del repuesto (recepción → uso → reservas), en orden y sin movimientos de usos rechazados. |
| [`test_auth_jwt.py`](api/tests/test_auth_jwt.py) | Login, expiración y firma del token, que el rol no se pueda alterar editando el token, contraseñas hasheadas y seed idempotente. |
| [`test_auth_y_endpoints.py`](api/tests/test_auth_y_endpoints.py) | 401 y 403 por rol, alta de incidencias con fotos, paso a reparación, turno y carga de stock (RN-08). |
| [`test_incidencias.py`](api/tests/test_incidencias.py) | Flujo de incidencias: reporte con foto, máquina inexistente, permisos, paso a reparación y transición inválida. |
| [`test_rn08_recepcion.py`](api/tests/test_rn08_recepcion.py) | RN-08: alta de recepción de stock, actualización de lote y ubicación, remito, movimiento `ENTRADA` inmutable y restricción por rol. |
| [`test_contrato.py`](api/tests/test_contrato.py) | El backend implementa exactamente las operaciones de `openapi.yaml`, ni más ni menos. |

## Contrato y cliente generado

- La fuente de verdad es [`openapi.yaml`](openapi.yaml), en la raíz del repo. [`M2/openapi.yaml`](M2/openapi.yaml) es la versión entregada en el hito M2 y no se modifica.
- El cliente del front ([`web/src/api/schema.d.ts`](web/src/api/schema.d.ts)) se genera con `openapi-typescript` y se usa con `openapi-fetch`, así que el front no compila si llama a una ruta o un campo que el contrato no tiene.
- Si cambiás el contrato:

  ```bash
  pnpm lint:contrato   # valida openapi.yaml
  pnpm gen:api         # regenera web/src/api/schema.d.ts
  ```

  Commiteá `schema.d.ts` junto con el cambio del contrato. Si te olvidás de regenerarlo, el CI falla (`pnpm check:cliente`).

## Desarrollo sin Docker para la API y el front

Requisitos: Node 22+, pnpm y uv. La base igual corre en Docker.

```bash
pnpm install:all   # dependencias de la raíz, del front y de la API
pnpm dev           # base + mock :4010 + API :8000 con recarga + front :5173
```

En modo desarrollo, Vite reenvía `/api` a la API real en `localhost:8000`.

## Limitaciones conocidas

- **Notificaciones:** las alertas de stock mínimo y los avisos de reserva liberada se escriben en el log de la API; todavía no se envían por correo. El envío está detrás de una interfaz (`Notificador`), así que se puede agregar sin tocar las reglas de negocio.
- **Cuentas:** son las cuatro cuentas de demo del seed. No hay alta de usuarios ni cambio de contraseña desde la aplicación.
- **Sesión:** el token dura 8 horas (un turno, configurable con `JWT_MINUTOS`) y no se renueva solo. Cuando vence, el front pide volver a ingresar. El token se guarda en `sessionStorage` y se borra al cerrar la pestaña.
- **Front:** las pantallas cubren incidencias, uso de repuestos y carga de stock. El paso de una incidencia a reparación y las reservas se operan desde la API.
- **Escaneo:** el CU-01 prevé escanear el código del envase con la cámara; por ahora el código se ingresa a mano.

## Estructura del repositorio

| Ruta | Contenido |
| --- | --- |
| [`api/`](api/) | Backend: `app/` (routers, services, repositories, modelos), `alembic/` (migraciones), `tests/` |
| [`web/`](web/) | Front: `src/pages/` (pantallas), `src/api/` (cliente generado y hooks), `nginx.conf` |
| [`openapi.yaml`](openapi.yaml) | Contrato de la API |
| [`docs/`](docs/) | Especificación, diagramas y maquetas |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Integración continua |

## Cómo colaborar

Trabajamos con feature branches y Pull Requests a `main`, con al menos una aprobación de otro integrante. El detalle está en [CONTRIBUTING.md](CONTRIBUTING.md) y los acuerdos del equipo en [TEAM_CHARTER.md](TEAM_CHARTER.md).

Este repo es un fork del repositorio de la cátedra. Para traer sus novedades: `git pull upstream main`.
