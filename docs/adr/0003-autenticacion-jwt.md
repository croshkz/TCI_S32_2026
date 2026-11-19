# ADR-0003: Autenticación con JWT y rol firmado en el token

- **Estado:** Aceptado
- **Fecha:** 2026-11-17
- **Responsable:** Tiziano Hurst

## Contexto

Las reglas de negocio dependen del rol: solo Mantenimiento y Encargado registran usos y cargan stock, y solo el Encargado libera reservas (RN-05). La primera versión usaba un *stub* que tomaba el rol de un header, así que cualquiera podía hacerse pasar por Encargado. El front es una SPA y la API no guarda sesiones.

## Decisión

- `POST /auth/login` valida usuario y contraseña y devuelve un JWT firmado con **HS256** y la clave `JWT_SECRET`.
- El token lleva el usuario, el nombre y el **rol** como claims, y vence a las **8 horas** (un turno, configurable con `JWT_MINUTOS`).
- En cada request se verifica la firma y la expiración y se reconstruye el usuario desde los claims. Los permisos se declaran por endpoint con `requiere_rol(...)`.
- Sin token o con un token inválido la API responde `401`. Con un rol no permitido responde `403`.
- Las contraseñas se guardan con PBKDF2-SHA256 (600.000 iteraciones y sal aleatoria), usando la biblioteca estándar de Python.
- El front guarda el token en `sessionStorage`, que se borra al cerrar la pestaña.

## Alternativas consideradas

- **Sesiones en el servidor con cookie:** obliga a guardar estado y a protegerse de CSRF.
- **Leer el rol de la base en cada request:** más consultas, sin necesidad mientras los roles no cambien durante un turno.

## Consecuencias

- La API no guarda estado de sesión.
- Modificar el rol dentro del token invalida la firma (`test_auth_jwt.py`).
- Si a un usuario se le cambia el rol, el cambio rige recién cuando vence su token. No hay revocación antes de la expiración.
- En cualquier entorno que no sea desarrollo hay que definir `JWT_SECRET`.
