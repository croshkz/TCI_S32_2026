# Cómo colaborar en este repositorio

## Modelo de ramas: Feature Branch Flow

Una feature = una rama = un PR. `main` siempre queda estable.

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