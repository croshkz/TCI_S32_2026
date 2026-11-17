"""Carga datos de ejemplo si la base está vacía. Se ejecuta después de las migraciones.

Es idempotente: cuentas y datos de planta se siembran por separado y cada parte solo se
carga si su tabla está vacía, así que correrlo dos veces no duplica nada.
"""

from dataclasses import dataclass
from functools import cache

from sqlmodel import Session, select

from app.db import engine
from app.models import Cuenta, EstadoIncidencia, Incidencia, Maquina, Repuesto, Rol, Turno, Ubicacion
from app.seguridad import hashear

PASSWORD_DEMO = "planta2026"


@dataclass(frozen=True)
class CuentaDemo:
    usuario: str
    nombre: str
    rol: Rol


CUENTAS_DEMO = [
    CuentaDemo("operario", "Operario Demo", Rol.OPERARIO),
    CuentaDemo("mantenimiento", "Mantenimiento Demo", Rol.MANTENIMIENTO),
    CuentaDemo("encargado", "Encargado Demo", Rol.ENCARGADO),
    CuentaDemo("gerencia", "Gerencia Demo", Rol.CONSULTA),
]


@cache
def _hash_demo(usuario: str) -> str:
    # El hash es lento a propósito; se calcula una vez por cuenta y proceso (acelera los tests).
    return hashear(PASSWORD_DEMO)


def sembrar(session: Session) -> None:
    _sembrar_cuentas(session)
    _sembrar_planta(session)


def _sembrar_cuentas(session: Session) -> None:
    if session.exec(select(Cuenta)).first() is not None:
        return
    session.add_all(
        Cuenta(usuario=c.usuario, nombre=c.nombre, rol=c.rol, password_hash=_hash_demo(c.usuario))
        for c in CUENTAS_DEMO
    )
    session.commit()


def _sembrar_planta(session: Session) -> None:
    if session.exec(select(Repuesto)).first() is not None:
        return

    session.add_all(
        [
            Ubicacion(codigo="A-03-12", descripcion="Estantería A, nivel 3, posición 12"),
            Ubicacion(codigo="A-03-13", descripcion="Estantería A, nivel 3, posición 13"),
            Ubicacion(codigo="B-01-04", descripcion="Estantería B, nivel 1, posición 4"),
        ]
    )
    caldera = Maquina(codigo="MAQ-0001", nombre="Caldera 2", tipo="caldera")
    fraccionador = Maquina(codigo="MAQ-0002", nombre="Fraccionador 1", tipo="fraccionador")
    banda = Maquina(codigo="MAQ-0003", nombre="Banda 3", tipo="banda de transporte")
    session.add_all([caldera, fraccionador, banda])
    session.flush()

    session.add_all(
        [
            Repuesto(
                codigo="REP-6204",
                nombre="Rodamiento 6204",
                lote="L-2026-031",
                ubicacion_codigo="A-03-12",
                stock_fisico=12,
                umbral_minimo=5,
            ),
            Repuesto(
                codigo="REP-0100",
                nombre="Correa dentada HTD 8M",
                lote="L-2026-018",
                ubicacion_codigo="B-01-04",
                stock_fisico=3,
                umbral_minimo=2,
            ),
            Incidencia(
                maquina_id=caldera.id,
                descripcion="La caldera pierde presión al arrancar.",
                turno=Turno.TARDE,
                estado=EstadoIncidencia.EN_REPARACION,
                reportada_por="Operario Demo",
            ),
            Incidencia(
                maquina_id=fraccionador.id,
                descripcion="Ruido metálico en el eje principal.",
                turno=Turno.MANANA,
                estado=EstadoIncidencia.EN_REPARACION,
                reportada_por="Operario Demo",
            ),
        ]
    )
    session.commit()


if __name__ == "__main__":
    with Session(engine) as session:
        sembrar(session)
