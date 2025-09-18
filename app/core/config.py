"""
Configuración central de la aplicación MisBoletas.

Este archivo lee las variables de entorno del archivo .env
y las hace disponibles para toda la aplicación.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic.
    Lee automáticamente del archivo .env
    """
    
    # === CONFIGURACIÓN DE BASE DE DATOS ===
    SQLSERVER_SERVER: str      # Servidor SQL Server (ej: localhost)
    SQLSERVER_DATABASE: str    # Nombre de la base de datos
    SQLSERVER_USERNAME: str    # Usuario de BD
    SQLSERVER_PASSWORD: str    # Contraseña de BD
    
    # === CONFIGURACIÓN DE SEGURIDAD ===
    SECRET_KEY: str = "mi-clave-super-secreta-cambiar-en-produccion"
    
    # === CONFIGURACIÓN DE LA APP ===
    DEBUG: bool = True                    # Modo debug para desarrollo
    API_PREFIX: str = "/api"              # Prefijo para todas las rutas
    ALLOW_ORIGIN: str = "*"               # Orígenes permitidos para CORS

    class Config:
        # Archivo donde están las variables de entorno
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True  # Las variables deben tener exactamente el mismo nombre

# Instancia global de configuración
# Usar en toda la app como: from app.core.config import settings
settings = Settings()