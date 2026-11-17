from fastapi import APIRouter, Depends

from app import config
from app.auth import Usuario, usuario_actual
from app.dependencias import auth_service
from app.schemas import LoginPedido, LoginRespuesta, UsuarioRespuesta
from app.services import AuthService

router = APIRouter(tags=["auth"])


@router.post("/auth/login", response_model=LoginRespuesta)
def iniciar_sesion(pedido: LoginPedido, servicio: AuthService = Depends(auth_service)) -> LoginRespuesta:
    sesion = servicio.iniciar_sesion(pedido.usuario, pedido.password)
    return LoginRespuesta(
        access_token=sesion.token,
        expira_en=config.JWT_MINUTOS * 60,
        usuario=UsuarioRespuesta(nombre=sesion.usuario.nombre, rol=sesion.usuario.rol),
    )


@router.get("/auth/me", response_model=UsuarioRespuesta)
def usuario_logueado(usuario: Usuario = Depends(usuario_actual)) -> UsuarioRespuesta:
    return UsuarioRespuesta(nombre=usuario.nombre, rol=usuario.rol)
