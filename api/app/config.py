import logging
import os
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://planta:planta@localhost:5432/planta")
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./uploads"))

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALGORITMO = "HS256"
JWT_MINUTOS = int(os.getenv("JWT_MINUTOS", "480"))  # un turno de 8 horas

if not JWT_SECRET:
    JWT_SECRET = "solo-desarrollo-cambiar-en-produccion"
    logging.getLogger(__name__).warning("JWT_SECRET no está definido: se usa una clave de desarrollo.")
