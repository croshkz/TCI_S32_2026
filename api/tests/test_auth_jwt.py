"""Login con JWT: credenciales, firma, expiración y rol tomado del token."""

from datetime import datetime, timedelta, timezone

import jwt
import pytest
from sqlmodel import select

from app import config
from app.auth import crear_token
from app.models import Cuenta, Rol
from app.seed import CUENTAS_DEMO, PASSWORD_DEMO, sembrar


def login(client, usuario: str, password: str = PASSWORD_DEMO):
    return client.post("/auth/login", json={"usuario": usuario, "password": password})


@pytest.mark.parametrize("cuenta", CUENTAS_DEMO, ids=lambda c: c.usuario)
def test_login_devuelve_un_token_con_el_rol_de_la_cuenta(client, cuenta):
    respuesta = login(client, cuenta.usuario)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["token_type"] == "bearer"
    assert cuerpo["usuario"] == {"nombre": cuenta.nombre, "rol": cuenta.rol}
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {cuerpo['access_token']}"})
    assert me.json()["rol"] == cuenta.rol


def test_el_token_dura_un_turno(client):
    cuerpo = login(client, "mantenimiento").json()
    claims = jwt.decode(cuerpo["access_token"], config.JWT_SECRET, algorithms=["HS256"])

    assert cuerpo["expira_en"] == config.JWT_MINUTOS * 60
    assert claims["exp"] - claims["iat"] == config.JWT_MINUTOS * 60
    assert claims["sub"] == "mantenimiento"


@pytest.mark.parametrize(("usuario", "password"), [("mantenimiento", "incorrecta"), ("nadie", PASSWORD_DEMO)])
def test_credenciales_invalidas_dan_401_sin_revelar_cual_fallo(client, usuario, password):
    respuesta = login(client, usuario, password)

    assert respuesta.status_code == 401
    assert respuesta.json() == {"codigo": "CREDENCIALES_INVALIDAS", "mensaje": "Usuario o contraseña incorrectos."}


def test_cuenta_desactivada_no_puede_entrar(client, session):
    cuenta = session.exec(select(Cuenta).where(Cuenta.usuario == "operario")).one()
    cuenta.activa = False
    session.commit()

    assert login(client, "operario").status_code == 401


def test_login_sin_datos_da_422(client):
    assert client.post("/auth/login", json={"usuario": "", "password": ""}).status_code == 422


def test_token_vencido_da_401(client):
    token = crear_token("mantenimiento", "Mantenimiento Demo", Rol.MANTENIMIENTO, minutos=-1)

    respuesta = client.get("/repuestos/REP-6204", headers={"Authorization": f"Bearer {token}"})

    assert respuesta.status_code == 401
    assert respuesta.json()["codigo"] == "NO_AUTENTICADO"


def test_token_firmado_con_otra_clave_da_401(client):
    ahora = datetime.now(timezone.utc)
    falso = jwt.encode(
        {"sub": "x", "nombre": "Intruso", "rol": "ENCARGADO", "iat": ahora, "exp": ahora + timedelta(hours=1)},
        "otra-clave-que-no-es-la-del-servidor-1234",
        algorithm="HS256",
    )

    assert client.get("/auth/me", headers={"Authorization": f"Bearer {falso}"}).status_code == 401


def test_no_se_puede_subir_el_rol_editando_el_token(client):
    """Cambiar el rol en el payload sin volver a firmar invalida la firma."""
    token = login(client, "operario").json()["access_token"]
    cabecera, _, firma = token.split(".")
    claims = jwt.decode(token, options={"verify_signature": False})
    claims["rol"] = "ENCARGADO"
    payload = jwt.utils.base64url_encode(jwt.api_jws.json.dumps(claims).encode()).decode()

    respuesta = client.get("/auth/me", headers={"Authorization": f"Bearer {cabecera}.{payload}.{firma}"})

    assert respuesta.status_code == 401


def test_token_sin_algoritmo_no_se_acepta(client):
    ahora = datetime.now(timezone.utc)
    sin_firma = jwt.encode(
        {"sub": "x", "nombre": "Intruso", "rol": "ENCARGADO", "iat": ahora, "exp": ahora + timedelta(hours=1)},
        None,
        algorithm="none",
    )

    assert client.get("/auth/me", headers={"Authorization": f"Bearer {sin_firma}"}).status_code == 401


def test_la_contrasena_no_se_guarda_en_texto_plano(session):
    for cuenta in session.exec(select(Cuenta)).all():
        assert PASSWORD_DEMO not in cuenta.password_hash
        assert cuenta.password_hash.startswith("pbkdf2_sha256$")


def test_el_seed_es_idempotente(session):
    cuentas_antes = len(session.exec(select(Cuenta)).all())

    sembrar(session)
    sembrar(session)

    assert len(session.exec(select(Cuenta)).all()) == cuentas_antes == len(CUENTAS_DEMO)
