"""
Configuración de la sesión de base de datos PostgreSQL.

Este módulo maneja:
- Conexión a PostgreSQL usando SQLAlchemy.
- Uso de la variable de entorno DATABASE_URL.
- Creación del engine y sessions para la aplicación.
- Dependencia get_db() para inyección en endpoints FastAPI.

NOTA: Se eliminaron las referencias a SQL Server (pyodbc, variables separadas).
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from typing import Generator


# Usamos directamente la DATABASE_URL que es leída  Render
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Crear el motor de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True,
    echo=True # Deja 'echo=True' para ver las consultas SQL en la consola si lo deseas
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos (inyección de dependencias de FastAPI)
def get_db() -> Generator:
    """Proporciona una sesión de base de datos y la cierra al finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
