"""Autenticación con JWT (HS256).

El token lleva el usuario, el nombre y el rol firmados con JWT_SECRET. Para cada request
se verifica la firma y la expiración y se reconstruye el Usuario a partir de los claims:
el rol sale del token, no de lo que mande el cliente. Los routers solo usan
`usuario_actual` y `requiere_rol`, así que no cambian respecto del stub de M4.
"""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app import config
from app.errores import NoAutenticado, PermisoDenegado
from app.models import Rol


@dataclass(frozen=True)
class Usuario:
    nombre: str
    rol: Rol


esquema_bearer = HTTPBearer(auto_error=False)


def crear_token(usuario: str, nombre: str, rol: Rol, *, minutos: int | None = None) -> str:
    emitido = datetime.now(timezone.utc)
    claims = {
        "sub": usuario,
        "nombre": nombre,
        "rol": rol.value,
        "iat": emitido,
        "exp": emitido + timedelta(minutes=config.JWT_MINUTOS if minutos is None else minutos),
    }
    return jwt.encode(claims, config.JWT_SECRET, algorithm=config.JWT_ALGORITMO)


def leer_token(token: str) -> Usuario:
    try:
        claims = jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITMO],
            options={"require": ["sub", "exp", "iat"]},
        )
        return Usuario(nombre=claims["nombre"], rol=Rol(claims["rol"]))
    except (jwt.InvalidTokenError, KeyError, ValueError) as error:
        raise NoAutenticado() from error


def usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(esquema_bearer),
) -> Usuario:
    if credenciales is None:
        raise NoAutenticado()
    return leer_token(credenciales.credentials)


def requiere_rol(*roles: Rol) -> Callable[[Usuario], Usuario]:
    def dependencia(usuario: Usuario = Depends(usuario_actual)) -> Usuario:
        if usuario.rol not in roles:
            raise PermisoDenegado()
        return usuario

    return dependencia
