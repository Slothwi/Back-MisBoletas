"""
Configuración simplificada para desarrollo local con SQL Server
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Configuración de la aplicación - Lee variables de entorno automáticamente
    """
    
    # === CONFIGURACIÓN DE ENTORNO ===
    ENV: str = "local"
    
    # === CONFIGURACIÓN DE BASE DE DATOS (SQL Server) ===
    SQLSERVER_SERVER: str = "localhost"
    SQLSERVER_DATABASE: str = "MisBoletas"
    SQLSERVER_USERNAME: str = "olave"
    SQLSERVER_PASSWORD: str = "123"
    
    # === URL DE BASE DE DATOS ===
    DATABASE_URL: str = "mssql+pyodbc://olave:123@localhost/MisBoletas?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    
    # === CONFIGURACIÓN DE SEGURIDAD ===
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # === CONFIGURACIÓN DE LA APP ===
    DEBUG: bool = False  # Cambiado a False por defecto
    API_PREFIX: str = "/api"
    ALLOW_ORIGIN: str = "*"
    
    # === GOOGLE CLOUD (OPCIONAL) ===
    GOOGLE_CLOUD_PROJECT: Optional[str] = None
    GOOGLE_CLOUD_BUCKET: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    
    @property
    def is_local_env(self) -> bool:
        """True si estamos en entorno local"""
        return self.ENV == "local"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

# Instancia global de configuración
# Usar en toda la app como: from app.core.config import settings
settings = Settings()