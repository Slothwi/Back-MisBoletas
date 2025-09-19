"""
Manejadores de errores para la aplicación MisBoletas.

¿Qué hace esto?
Cuando algo sale mal en la API (error de BD, validación, etc.),
estos manejadores "atrapan" el error y devuelven una respuesta HTTP amigable.

Solo llamar setup_exception_handlers(app) en main.py
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import logging
from .exceptions import handle_database_error

logger = logging.getLogger(__name__)

def setup_exception_handlers(app: FastAPI):

    # Configura todos los manejadores de errores globales.

    @app.exception_handler(SQLAlchemyError)
    async def database_error_handler(request: Request, exc: SQLAlchemyError):
        # Maneja errores de base de datos.

        url = str(request.url.path)
        logger.error(f"Error de BD en {url}: {str(exc)}")
        
        # Convertir error técnico a mensaje amigable
        http_exception = handle_database_error(exc)
        
        return JSONResponse(
            status_code=http_exception.status_code,
            content={
                "error": "Error de base de datos",
                "message": http_exception.detail,
                "path": url
            }
        )
    
    @app.exception_handler(ValidationError) 
    async def validation_error_handler(request: Request, exc: ValidationError):
        # Maneja errores de validación de datos.

        url = str(request.url.path)
        logger.error(f" Error de validación en {url}: {str(exc)}")
        
        # Extraer errores específicos para el frontend
        errors = []
        for error in exc.errors():
            field = " → ".join(str(loc) for loc in error["loc"])
            errors.append(f"{field}: {error['msg']}")
        
        return JSONResponse(
            status_code=422,
            content={
                "error": "Datos inválidos",
                "message": "Por favor revisa los datos enviados",
                "details": errors,
                "path": url
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException):
        # Maneja errores HTTP estándar.

        url = str(request.url.path)
        
        # Solo loguear errores 5xx como errores, 4xx como warnings
        if exc.status_code >= 500:
            logger.error(f" Error {exc.status_code} en {url}: {exc.detail}")
        else:
            logger.warning(f" HTTP {exc.status_code} en {url}: {exc.detail}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": f"Error {exc.status_code}",
                "message": exc.detail,
                "path": url
            }
        )
    
    @app.exception_handler(Exception)
    async def catch_all_handler(request: Request, exc: Exception):
        # Maneja cualquier error no controlado.

        url = str(request.url.path)
        error_type = type(exc).__name__
        
        logger.error(
            f" Error inesperado en {url}: {error_type} - {str(exc)}", 
            exc_info=True  # Incluye stack trace completo
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Error interno del servidor",
                "message": "Algo salió mal. Por favor contacta al administrador.",
                "type": error_type,
                "path": url
            }
        )
    
    logger.info(" Manejadores de errores configurados")
    logger.info(" Los errores ahora se mostrarán de forma amigable")