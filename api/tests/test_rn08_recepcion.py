"""RN-08: al recibir una compra se carga el stock físico y su ubicación."""

import pytest
from sqlmodel import select

from app.models import MovimientoStock, Recepcion, Rol, TipoMovimiento
from tests.conftest import auth, repuesto

MANTENIMIENTO = auth(Rol.MANTENIMIENTO)
ENCARGADO = auth(Rol.ENCARGADO)
OPERARIO = auth(Rol.OPERARIO)


def test_registrar_recepcion_incrementa_stock_y_actualiza_ubicacion(client, session):
    respuesta = client.post(
        "/repuestos/REP-6204/recepciones",
        headers=MANTENIMIENTO,
        data={"lote": "L-2026-099", "cantidad": 8, "ubicacion": "A-03-13"},
        files={"remito": ("remito_099.pdf", b"%PDF-1.4-falso", "application/pdf")},
    )

    assert respuesta.status_code == 201
    assert respuesta.json()["stock_fisico"] == 20

    actualizado = repuesto(session, "REP-6204")
    assert actualizado.stock_fisico == 20
    assert actualizado.lote == "L-2026-099"
    assert actualizado.ubicacion_codigo == "A-03-13"

    recepcion = session.exec(select(Recepcion)).one()
    movimiento = session.exec(select(MovimientoStock)).one()
    assert (recepcion.lote, recepcion.cantidad, recepcion.ubicacion_codigo) == ("L-2026-099", 8, "A-03-13")
    assert recepcion.remito_ruta is not None
    assert (movimiento.tipo, movimiento.cantidad, movimiento.referencia) == (TipoMovimiento.ENTRADA, 8, "REC-0001")


def test_rechaza_recepcion_si_la_ubicacion_no_existe(client, session):
    respuesta = client.post(
        "/repuestos/REP-6204/recepciones",
        headers=ENCARGADO,
        data={"lote": "L-2026-100", "cantidad": 5, "ubicacion": "Z-99-99"},
    )

    assert respuesta.status_code == 404
    assert repuesto(session, "REP-6204").stock_fisico == 12


def test_rechaza_recepcion_si_el_repuesto_no_existe(client):
    respuesta = client.post(
        "/repuestos/REP-NO-EXISTE/recepciones",
        headers=ENCARGADO,
        data={"lote": "L-2026-100", "cantidad": 5, "ubicacion": "A-03-12"},
    )

    assert respuesta.status_code == 404


@pytest.mark.parametrize("cantidad", [0, -3])
def test_rechaza_recepcion_con_cantidad_invalida(client, session, cantidad):
    respuesta = client.post(
        "/repuestos/REP-6204/recepciones",
        headers=MANTENIMIENTO,
        data={"lote": "L-2026-100", "cantidad": cantidad, "ubicacion": "A-03-12"},
    )

    assert respuesta.status_code == 422
    assert repuesto(session, "REP-6204").stock_fisico == 12


def test_operario_no_puede_registrar_recepcion_de_compra(client):
    respuesta = client.post(
        "/repuestos/REP-6204/recepciones",
        headers=OPERARIO,
        data={"lote": "L-2026-100", "cantidad": 5, "ubicacion": "A-03-12"},
    )

    assert respuesta.status_code == 403