# Team Charter

Acuerdos de trabajo del equipo. Comisión S32 · Desarrollo de Software 2026.

## Integrantes

Ver la tabla de Integrantes del `README.md` (legajo, nombre y email de cada uno).

## Comunicación

- Canal principal: grupo de WhatsApp del equipo.
- Discusión técnica de un cambio: en los comentarios del Pull Request, para que quede registro.
- Frecuencia mínima de encuentro: una reunión semanal + los días de cursada.
- Tiempo máximo de respuesta esperado: 24 hs en día hábil.

## Rol de representante (integrador)

- El rol rota por etapa, según el cronograma de la cátedra.
- El representante gestiona el fork, los contributors y la sincronización con `upstream`.

## Convención de commits

Usamos Conventional Commits (`feat`, `fix`, `docs`, `chore`, `refactor`, `test`).
El detalle está en `CONTRIBUTING.md`.

## Reglas de Pull Requests

- Nadie pushea directo a `main`. Todo entra por PR.
- Mínimo 1 aprobación de un compañero.
- El autor no aprueba ni mergea su propio PR.
- Los PR van siempre a `main` del fork del equipo, nunca al repo de la cátedra.
- Título del PR con el mismo formato que los commits: `tipo: descripción corta`.
- Un PR sin revisar más de 48 hs se avisa por el canal del equipo.

## Definición de Terminado (DoD)

Un cambio está terminado cuando:

1. Está en su propia rama, con commits que siguen la convención.
2. Tiene un PR abierto contra `main` del fork del equipo.
3. Fue revisado y aprobado por al menos un compañero.
4. No rompe nada de lo que ya estaba (README, archivos de otros).
5. Está mergeado y la rama se borró.

## Si alguien no aporta

1. Se le avisa primero por el canal del equipo.
2. Si en una semana no hay respuesta, se habla en la reunión del equipo.
3. Si sigue sin haber aporte, se le informa al docente antes de la entrega.

El registro de aportes es el historial de commits y PRs del repo.