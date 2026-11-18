"""Flujo de incidencias: reporte con máquina/fotos, transición a reparación y destinos de uso."""

from sqlmodel import select

from app.models import EstadoIncidencia, FotoIncidencia, Incidencia, Rol, Turno
from tests.conftest import auth

OPERARIO = auth(Rol.OPERARIO)
MANTENIMIENTO = auth(Rol.MANTENIMIENTO)
CONSULTA = auth(Rol.CONSULTA)


def test_operario_reporta_incidencia_con_foto_y_queda_reportada(client, session):
    respuesta = client.post(
        "/incidencias",
        headers=OPERARIO,
        data={
            "codigo_maquina": "MAQ-0003",
            "descripcion": "Vibración anormal en motor principal",
            "turno": Turno.MANANA.value,
        },
        files=[("fotos", ("falla.jpg", b"contenido-imagen-falso", "image/jpeg"))],
    )

    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["estado"] == EstadoIncidencia.REPORTADA.value

    incidencia = session.exec(select(Incidencia).where(Incidencia.id == int(datos["id"].split("-")[1]))).one()
    assert incidencia.descripcion == "Vibración anormal en motor principal"
    assert incidencia.turno == Turno.MANANA
    assert session.exec(select(FotoIncidencia).where(FotoIncidencia.incidencia_id == incidencia.id)).one()


def test_rechaza_reporte_si_la_maquina_no_existe(client):
    respuesta = client.post(
        "/incidencias",
        headers=OPERARIO,
        data={"codigo_maquina": "MAQ-9999", "descripcion": "Falla eléctrica"},
    )

    assert respuesta.status_code == 404


def test_rol_consulta_no_puede_reportar_incidencia(client):
    respuesta = client.post(
        "/incidencias",
        headers=CONSULTA,
        data={"codigo_maquina": "MAQ-0003", "descripcion": "Intento desde gerencia"},
    )

    assert respuesta.status_code == 403


def test_iniciar_reparacion_cambia_estado_y_habilita_destino_de_uso(client):
    creada = client.post(
        "/incidencias",
        headers=OPERARIO,
        data={"codigo_maquina": "MAQ-0003", "descripcion": "Sensor obstruido"},
    ).json()
    codigo_inc = creada["id"]

    # Antes de iniciar reparación no aparece como destino válido para usar repuestos
    destinos_antes = [item["id"] for item in client.get("/destinos-uso", headers=MANTENIMIENTO).json()]
    assert codigo_inc not in destinos_antes

    # Mantenimiento inicia la reparación (REPORTADA -> EN_REPARACION)
    reparacion = client.post(f"/incidencias/{codigo_inc}/reparacion", headers=MANTENIMIENTO)
    assert reparacion.status_code == 200
    assert reparacion.json()["estado"] == EstadoIncidencia.EN_REPARACION.value

    # Ahora sí figura en /destinos-uso para que el bloque de stock pueda descontar repuestos
    destinos_despues = [item["id"] for item in client.get("/destinos-uso", headers=MANTENIMIENTO).json()]
    assert codigo_inc in destinos_despues


def test_rechaza_iniciar_reparacion_si_ya_estaba_en_reparacion(client):
    respuesta = client.post("/incidencias/INC-0001/reparacion", headers=MANTENIMIENTO)

    assert respuesta.status_code == 409
    assert respuesta.json()["codigo"] == "TRANSICION_INVALIDA"