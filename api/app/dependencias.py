from fastapi import Depends
from sqlmodel import Session

from app.db import get_session
from app.notificaciones import Notificador, get_notificador
from app.services import AuthService, IncidenciaService, ReservaService, StockService


def stock_service(
    session: Session = Depends(get_session),
    notificador: Notificador = Depends(get_notificador),
) -> StockService:
    return StockService(session, notificador)


def incidencia_service(session: Session = Depends(get_session)) -> IncidenciaService:
    return IncidenciaService(session)


def reserva_service(
    session: Session = Depends(get_session),
    notificador: Notificador = Depends(get_notificador),
) -> ReservaService:
    return ReservaService(session, notificador)


def auth_service(session: Session = Depends(get_session)) -> AuthService:
    return AuthService(session)
