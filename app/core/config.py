"""
Este archivo lee las variables de entorno del archivo .env
y las hace disponibles para toda la aplicación.
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic.
    Lee automáticamente del archivo .env
    """
    
    # === CONFIGURACIÓN DE BASE DE DATOS ===
    DATABASE_URL: str                     # DESDE .ENV (Render la proporciona)
    EXTERNAL_DATABASE_URL: Optional[str] = None  # DESDE .ENV (opcional, para conexiones externas)
    ENV: str = "local"                # local

    # === CONFIGURACIÓN DE SEGURIDAD ===
    SECRET_KEY: str                           # DESDE .ENV
    JWT_ALGORITHM: str = "HS256"              # Algoritmo JWT
    JWT_EXPIRE_MINUTES: int = 30              # Minutos de expiración del token
    
    # === CONFIGURACIÓN DE LA APP ===
    DEBUG: bool = True                    # Modo debug para desarrollo
    API_PREFIX: str = "/api"              # Prefijo para todas las rutas
    ALLOW_ORIGIN: str = "*"               # Orígenes permitidos para CORS

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        """
        Devuelve la URL que debe usar SQLAlchemy según el entorno:
        - local -> EXTERNAL_DATABASE_URL
        - render -> DATABASE_URL
        """
        if self.ENV == "render":
            return self.DATABASE_URL
        return self.EXTERNAL_DATABASE_URL
    class Config:
        # Archivo donde están las variables de entorno
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True  # Las variables deben tener exactamente el mismo nombre

# Instancia global de configuración
# Usar en toda la app como: from app.core.config import settings
settings = Settings()