"""RN-06: de cada repuesto se reconstruye su historia interna (recepción → uso)."""

from app.models import Rol
from tests.conftest import auth

MANTENIMIENTO = auth(Rol.MANTENIMIENTO)
ENCARGADO = auth(Rol.ENCARGADO)
CONSULTA = auth(Rol.CONSULTA)


def resumen(movimientos: list[dict]) -> list[tuple[str, int, str]]:
    return [(m["tipo"], m["cantidad"], m["referencia"]) for m in movimientos]


def test_repuesto_sin_movimientos_devuelve_lista_vacia(client):
    respuesta = client.get("/repuestos/REP-6204/movimientos", headers=CONSULTA)

    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_historial_reconstruye_recepcion_uso_y_reserva_en_orden(client):
    client.post(
        "/repuestos/REP-6204/recepciones",
        headers=MANTENIMIENTO,
        data={"lote": "L-2026-045", "cantidad": 10, "ubicacion": "A-03-12"},
    )
    client.post("/repuestos/REP-6204/usos", headers=MANTENIMIENTO, json={"destino_id": "INC-0001", "cantidad": 3})
    client.post(
        "/reservas",
        headers=MANTENIMIENTO,
        json={"repuesto_codigo": "REP-6204", "cantidad": 4, "motivo": "Preventivo caldera"},
    )
    client.post("/reservas/RES-0001/liberacion", headers=ENCARGADO)

    respuesta = client.get("/repuestos/REP-6204/movimientos", headers=CONSULTA)

    assert respuesta.status_code == 200
    assert resumen(respuesta.json()) == [
        ("entrada", 10, "REC-0001"),
        ("consumo", 3, "INC-0001"),
        ("reserva", 4, "RES-0001"),
        ("liberacion", 4, "RES-0001"),
    ]
    assert {m["usuario"] for m in respuesta.json()} >= {"Mantenimiento Demo"}


def test_historial_solo_incluye_movimientos_del_repuesto_pedido(client):
    client.post("/repuestos/REP-0100/usos", headers=MANTENIMIENTO, json={"destino_id": "INC-0001", "cantidad": 1})

    respuesta = client.get("/repuestos/REP-6204/movimientos", headers=CONSULTA)

    assert respuesta.json() == []


def test_uso_rechazado_no_deja_movimiento(client):
    client.post("/repuestos/REP-6204/usos", headers=MANTENIMIENTO, json={"destino_id": "INC-0001", "cantidad": 99})

    assert client.get("/repuestos/REP-6204/movimientos", headers=CONSULTA).json() == []


def test_historial_de_repuesto_inexistente_devuelve_404(client):
    assert client.get("/repuestos/REP-NO-EXISTE/movimientos", headers=CONSULTA).status_code == 404


def test_historial_sin_token_devuelve_401(client):
    assert client.get("/repuestos/REP-6204/movimientos").status_code == 401
