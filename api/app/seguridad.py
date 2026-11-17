"""Hash de contraseñas con PBKDF2-SHA256 (biblioteca estándar, sin dependencias extra).

Formato guardado: pbkdf2_sha256$<iteraciones>$<sal_b64>$<hash_b64>
"""

import base64
import hashlib
import hmac
import secrets

ALGORITMO = "pbkdf2_sha256"
ITERACIONES = 600_000  # recomendación OWASP 2023 para PBKDF2-SHA256


def _derivar(password: str, sal: bytes, iteraciones: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), sal, iteraciones)


def hashear(password: str) -> str:
    sal = secrets.token_bytes(16)
    derivada = _derivar(password, sal, ITERACIONES)
    return f"{ALGORITMO}${ITERACIONES}${base64.b64encode(sal).decode()}${base64.b64encode(derivada).decode()}"


def verificar(password: str, guardado: str) -> bool:
    try:
        algoritmo, iteraciones, sal, esperado = guardado.split("$")
    except ValueError:
        return False
    if algoritmo != ALGORITMO:
        return False
    derivada = _derivar(password, base64.b64decode(sal), int(iteraciones))
    return hmac.compare_digest(derivada, base64.b64decode(esperado))
