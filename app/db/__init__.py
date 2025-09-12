"""
Paquete de configuración de base de datos.

Exporta las funciones y objetos principales para manejo de BD:
- Base: Clase base para modelos SQLAlchemy
- SessionLocal: Factory para crear sesiones de BD
- engine: Motor de SQLAlchemy configurado
- get_db: Dependencia para inyección en FastAPI endpoints

Uso típico:
    from app.db import get_db, SessionLocal
    
Autor: Configurado para proyecto MisBoletas  
Fecha: 2025-09-11
"""

# Importaciones principales del paquete db
from .session import Base, SessionLocal, engine, get_db

__all__ = [
    "Base",
    "SessionLocal", 
    "engine",
    "get_db"
]