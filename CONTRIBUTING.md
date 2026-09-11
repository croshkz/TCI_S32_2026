# Cómo colaborar en este repositorio

## Modelo de ramas: Feature Branch Flow

feature branch → PR → review.

No mezclamos dos cambios distintos en la misma rama. Si no tienen relación, son dos ramas y dos PRs.

## Nombres de rama

- `feat/<descripcion>` — funcionalidad nueva
- `fix/<algo>` — corrección
- `docs/<tema>` — documentación
- `chore/<tarea>` — mantenimiento

En minúsculas y con guiones: `feat/login-usuario`, `docs/team-charter`.

## Antes de empezar una feature

Sincronizá tu `main` con la cátedra y con el equipo:

```bash
git checkout main
git pull upstream main    # lo nuevo de la cátedra
git pull origin main      # lo nuevo que mergeó el equipo
git checkout -b feat/mi-feature
```

## A dónde van los Pull Requests

Los PR van **siempre** a la rama `main` del fork del equipo.
**Nunca** al repo base de la cátedra (`desasoftfrlptn/TCI_S32_2026`): de ahí solo recibimos con `pull`.

Al abrir el PR, revisá que en **base** figure el fork del equipo. GitHub por defecto propone el repo original.

## Convención de commits: Conventional Commits
<tipo>(<alcance opcional>): <descripción en imperativo>

Tipos que usamos:

| Tipo | Cuándo |
|---|---|
| `feat` | funcionalidad nueva |
| `fix` | corrección de un error |
| `docs` | documentación (README, este archivo, etc.) |
| `chore` | tareas de mantenimiento, config, dependencias |
| `refactor` | cambio de código sin alterar el comportamiento |
| `test` | agregar o corregir tests |

Reglas:

- La descripción va en minúscula, en imperativo y sin punto final: `agrego`, no `agregado` ni `Agrega.`.
- Máximo 50 caracteres en la primera línea.
- Si el cambio rompe compatibilidad, se marca con `!` y se explica en el cuerpo: `feat!: cambio el formato del README`.
- El mensaje responde al QUÉ y al POR QUÉ, no "arreglos varios".

Ejemplos:
docs: agrego mi registro de integrante 
feat(login): valido el formato del email 
fix: corrijo la tabla de integrantes rota


## Commits chicos y seguidos

Un commit por idea atómica. No "todo junto al final".

## Cómo se revisan los PR

- Mínimo 1 aprobación de un compañero.
- El autor NO se mergea su propio PR.
- El revisor mira **Files changed**: que el cambio haga lo que dice el título y que no pise trabajo de otro.
- Si algo no va, se usa **Request changes** con un comentario concreto.
- Aprobado el PR, el revisor mergea y se borra la rama.

## Nunca

- Pushear directo a `main`.
- Subir credenciales, tokens o secretos.
- Mergear tu propio PR.


## Workflow elegido y justificación

Elegimos **GitHub Flow** por los siguientes motivos:

1. **Tamaño del equipo.** Somos 3 integrantes en el TCI. Un modelo con
   `develop`, `release/*` y `hotfix/*` implicaría más ramas de larga vida que
   personas trabajando, y cada cambio habría que integrarlo dos veces. GitHub
   Flow nos da lo mínimo necesario sin agregar complejidad que no vamos a usar.

2. **Claridad del historial.** Con una única rama estable (`main`) y una rama
   corta por cada feature, siempre está claro qué se está desarrollando y dónde.
   `main` queda permanentemente actualizada y en condiciones de ser entregada,
   así que cualquier desarrollo nuevo parte de una base confiable.

3. **Revisión cruzada obligatoria.** Al integrar todo mediante Pull Request con
   aprobación de un compañero, ningún cambio entra sin que al menos dos personas
   lo hayan visto. Esto distribuye el conocimiento del proyecto entre los tres,
   evita que alguien quede desactualizado respecto de lo que hicieron los demás
   y detecta errores antes de que lleguen a `main`.


## Acciones concretas que nos demanda el flow

1. **main nunca se toca directo.** Activamos la protección de rama en GitHub
   para que no se pueda pushear directo y todo entre por Pull Request.

2. **Cada tarea = una rama nueva desde `main` actualizado.** Antes de empezar,
   actualizamos `main` local. Una rama por issue, nombrada con el número y una
   descripción corta (`feature/12-login-usuario`).

3. **Commits chicos y frecuentes.** Un commit por cambio con sentido propio,
   mensaje descriptivo en imperativo, y push diario para que el resto vea el avance.

4. **Abrir PR de la rama a `main`.** Con el issue vinculado, qué resuelve y cómo
   probarlo. Se abre apenas hay algo revisable, no después de una semana de trabajo.

5. **Al menos 1 review de un par.** El reviewer baja la rama, la prueba y aprueba
   o deja comentarios. Las correcciones van como commits nuevos en la misma rama.
   Rotamos quién revisa entre los 3.

6. **Merge y limpieza.** Mergea el reviewer, no el autor. Después se borra la rama
   y el resto del equipo actualiza su `main` local.   