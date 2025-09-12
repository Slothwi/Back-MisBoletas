"""
Configuración de la sesión de base de datos SQL Server.

Este módulo maneja:
- Conexión a SQL Server usando SQLAlchemy + pyodbc
- Configuración de variables de entorno desde .env
- Creación del engine y sessions para la aplicación
- Dependencia get_db() para inyección en endpoints FastAPI

"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la base de datos SQL Server
SQLSERVER_SERVER = os.getenv("SQLSERVER_SERVER", "localhost")
SQLSERVER_DATABASE = os.getenv("SQLSERVER_DATABASE", "MisBoletas")
SQLSERVER_USERNAME = os.getenv("SQLSERVER_USERNAME", "")
SQLSERVER_PASSWORD = os.getenv("SQLSERVER_PASSWORD", "")

# Validar que las variables críticas estén configuradas
if not SQLSERVER_USERNAME or not SQLSERVER_PASSWORD:
    raise ValueError(
        "ERROR: Variables de entorno faltantes!\n"
        "Crea un archivo .env con:\n"
        "SQLSERVER_USERNAME=tu_usuario\n"
        "SQLSERVER_PASSWORD=tu_contraseña\n"
        "Ver .env.example para más detalles."
    )

# Cadena de conexión para SQL Server con driver ODBC
# Formato: mssql+pyodbc://usuario:contraseña@servidor:puerto/basedatos?driver=ODBC+Driver+17+for+SQL+Server
DATABASE_URL = f"mssql+pyodbc://{SQLSERVER_USERNAME}:{SQLSERVER_PASSWORD}@{SQLSERVER_SERVER}:1433/{SQLSERVER_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"

# Crear el motor de SQLAlchemy (sin crear tablas automáticamente)
engine = create_engine(DATABASE_URL, echo=True)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()