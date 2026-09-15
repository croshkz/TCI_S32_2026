# Cronograma del TCI — Aula invertida

**Para alumnos · Desarrollo de Software 2026 · Comisión S32**

---

## 1. El proyecto en una línea

Desarrollar el **Sistema de Gestión de Stock y Mantenimiento de Planta** (ver `dominio.md`), **completo**: frontend + backend + base de datos + seguridad + pruebas, en equipos, con **entregas parciales (muestras)**, **presentación grupal final** y **defensa individual**.

---

## 2. Cómo funciona esta cursada (aula invertida, de verdad)

La lectura la hacés **en casa**; la clase se usa para **hacer**. El ciclo semanal es el siguiente:

| Momento | Dónde | Qué hacés |
|---|---|---|
| **ANTES** (en casa, 30–45 min) | Campus + repo | Leer un **recurso acotado** + entregar un **micro-entregable verificable** (un diagrama en borrador, un commit, o 3 preguntas). |
| **EN CLASE** (taller) | Aula + gabinete | **Clínica** sobre el trabajo de un equipo rotativo (~20 min, formato pecera) + **trabajo de equipo** con el docente circulando. |
| **DESPUÉS** (en casa) | Repo | **PR con review de pares** antes de la clase siguiente. |

> **Reglas de oro:**
> - Si el docente habla más de 20 minutos seguidos, la clase invertida **se dio vuelta sola**. Tu rol es hacer, no escuchar.
> - **Ticket de entrada:** cada semana hay un micro-entregable obligatorio de bajo puntaje. Sin él, el equipo **no entra al taller** (trabaja igual, pero sin acompañamiento docente).

---

## 3. El stack (decidido por la cátedra)

| Capa | Tecnología |
|---|---|
| **Frontend** | **React + TypeScript + Vite + pnpm** |
| **Backend** | **FastAPI + uvicorn + uv** |
| **Datos** | **SQLModel + Alembic + PostgreSQL** |
| **Contrato / mock** | **OpenAPI + Prism** (mock server generado del contrato) |
| **Notificaciones** | Puerto de notificación con **adaptador falso** (log / **Mailhog**) por defecto |
| **Control de versiones** | **Git + GitHub** (Issues, Projects, Pull Requests) |
| **Contenedores** | **Docker + docker-compose** |
| **Testing** | **pytest + TestClient** (backend) · **Vitest + Testing Library** (frontend) |

> **¿Por qué SQLModel?** Unifica Pydantic (validación) + SQLAlchemy (tabla) en una sola clase; es del autor de FastAPI. Migraciones con Alembic.
> **¿Por qué el contrato en M2?** El contrato OpenAPI es una **herramienta de diseño**, no un entregable de cierre. Se define primero, el mock (Prism) sale de él, y el frontend y el backend se construyen **contra el mismo contrato**. Así la integración (M5) deja de ser una lotería.

---

## 4. Las muestras (entregas)

| Muestra | Fecha | Entregable | Qué es lo nuevo / clave |
|---|---|---|---|
| **M1 — Documentación funcional** | vie 11/09 | Contexto + CU + especificación + actividad/secuencia + arquitectura + planificación + **máquinas de estado de Incidencia, Reserva y Pedido** | Las máquinas de estado son el artefacto de modelado de mayor valor |
| **M2 — Contrato + esqueleto desplegado** | vie 02/10 | Prototipo estático **recortado a 3 pantallas** + **contrato OpenAPI v0** + **repo desplegado** (`docker compose up` levanta algo) | El despliegue NO espera a la última semana |
| **M3 — SPA contra el contrato** | vie 16/10 | SPA React+TS consumiendo el **mock generado del contrato** + **walking skeleton** (un `/health` real desplegado) | Frontend y backend hablan el mismo contrato desde acá |
| **M4 — Backend + reglas + tests** | vie 30/10 | API FastAPI + SQLModel + Repository + Service Layer + **tests de RN-01, RN-02 y RN-05 obligatorios** + **auth stub con roles** | Testear es parte de implementar, no un trámite de cierre |
| **M5 — Integración end-to-end** | vie 13/11 | **2 CU end-to-end** (no uno) + **auth real** + Docker | La integración ya está preparada desde M2 |
| **M6 — Congelamiento** | vie 20/11 | **Sin features nuevas.** Todo integrado, Swagger publicado, suite verde | Freeze: de acá al final no se toca código nuevo |
| **FINAL — Entrega + defensa** | lun 30/11 | Sistema desplegado + documentación + exposición + defensa individual | **10 días sin código nuevo**: despliegue, documentación, ensayo |

> ⚠️ **Feriados / sin clases:** lun 21/09 y vie 25/09 (examen) → no hay clase. lun 12/10 y lun 23/11 (feriados) tampoco. Las entregas son por **repo**.

---

## 5. Escalamiento por tamaño de equipo

El alcance **escala con el tamaño del equipo**. No es lo mismo un grupo de 3 que uno de 5:

| Integrantes | Alcance |
|---|---|
| **Núcleo (3)** | Registrar uso de repuesto en reparación (RN-01, RN-02, RN-06) · cargar stock recibido con ubicación (RN-08) · reportar incidencia con QR de máquina · auth con **3 roles** |
| **+1 (4to)** | **Ciclo completo de Reserva** (RN-05 + RN-10 + liberación autorizada). Es el CU más difícil. |
| **+1 (5to)** | **Pedido de compra** con urgencia y notificaciones (RN-03, RN-04, RN-09) **o** alta de maquinaria con generación de lista de repuestos (RN-07). |

---

## 6. Individualización (nadie desaparece sin costo)

- Cada estudiante es **dueño de al menos un CU end-to-end**, desde la especificación hasta el test. Su nombre está en el **issue**, en el **PR** y en el **ADR**.
- Cada estudiante **revisa PRs de al menos dos compañeros distintos** y toca al menos **2 de las 4 áreas**: frontend, backend, datos, infra/tests.
- **La nota individual limita la grupal:** `nota_individual = min(nota_grupal, nota_defensa)`. No se promedia: si no podés defender el sistema, tu nota es la de tu defensa.

---

## 7. Definition of Done (para toda muestra)

Una tarea **está terminada** cuando:

- [ ] El **PR está mergeado por alguien distinto del autor**.
- [ ] El **issue está cerrado** con referencia al commit.
- [ ] Si toca una **regla de negocio**, el **test está verde**.
- [ ] La **documentación** está actualizada.
- [ ] Funciona con `docker compose up` desde **clone limpio**.

---

## 8. Rúbrica (la misma en cada muestra — mirá tu progresión)

Niveles: **I** Insuficiente (1–3) · **ED** En desarrollo (4–5) · **L** Logrado (6–7) · **D** Destacado (8–10).

| Dimensión | I (1–3) | ED (4–5) | L (6–7) | D (8–10) |
|---|---|---|---|---|
| **SABER** | No identifica conceptos o los aplica mal | Identifica pero no fundamenta | Fundamenta y aplica correctamente | Fundamenta, **compara alternativas y justifica** |
| **SABER HACER** | No funciona o no cumple | Funciona parcialmente, con errores | Funciona y cumple; código claro | Funciona, cumple y muestra **calidad** (patrones, tests, buenas prácticas) |
| **SABER SER** | No participa; no documenta; no asiste | Participa irregularmente | Participa y documenta; asiste con tickets | Es **referente** de asistencia entre pares |

---

## 9. Política de recuperación

- Cada muestra se puede **recuperar una sola vez**, entregando las correcciones **antes de la muestra siguiente**.
- La **devolución formativa** llega en **≤ 1 semana** con acciones correctivas explícitas.
- Si una muestra no se recupera en su ventana, ese porcentaje **se pierde** (no se arrastra el problema hasta noviembre).

---

## 10. Mapeo muestra → RA

| Muestra | RAs | Competencias |
|---|---|---|
| **M1** | RA01 (estimación), RA02 (organización), RA04 (seguimiento) | CG1, CG3, CG6, CG7 |
| **M2** | RA03 (herramientas), RA06 (despliegue) | CG1, CG7 |
| **M3** | RA03 | CG2.2 |
| **M4** | RA03, **RA05** (pruebas) | CG2.2 |
| **M5** | RA03, RA04, RA06 | CG2.3 |
| **M6** | RA05, RA06 | CE2.1, CE4.1 |
| **FINAL** | RA06, **RA07** (asistencia entre pares) | CG6, CG7, CG9, CE5.1 |

---

## 11. La muestra final + defensa individual

### 11.1 Entrega final (lun 30/11)
- **Sistema completo desplegado** (instalación limpia o Docker) — RA06.
- **Documentación funcional y técnica** actualizada.
- **Exposición grupal** (~15 min): el equipo muestra cómo resolvió el dominio.

### 11.2 Defensa individual
Cada integrante responde **individualmente**. Se sortean preguntas por nivel:

- **Comprensión:** *"¿Qué hace este fragmento de tu código?"* · *"¿Qué casos de uso implementaste vos y cuáles tus pares?"* · *"¿Por qué eligieron esta arquitectura?"*
- **Análisis:** *"¿Qué pasaría si el cliente cambia esta regla de negocio?"* · *"¿Cómo garantizás que el stock no quede negativo?"* · *"¿Qué pasa si una reserva se libera sin autorización?"*
- **Metacognición (CG9):** *"¿Qué fue lo más difícil y cómo lo resolviste?"* · *"¿Qué harías distinto?"* · *"¿Qué aprendiste de tus pares?"*

> La defensa **arranca con tu autoevaluación** y tu **bitácora de aprendizaje**. No se trata de "recitar" código: se trata de **defender** las decisiones que tomaste.
