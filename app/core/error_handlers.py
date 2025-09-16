"""
Manejadores globales de errores para la aplicación MisBoletas.

Captura y maneja errores no controlados:
- Errores de base de datos SQLAlchemy
- Errores de validación Pydantic
- Errores HTTP 404, 500, etc.
- Logging de errores para debugging

"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import logging
from .exceptions import handle_database_error

logger = logging.getLogger(__name__)

def setup_exception_handlers(app: FastAPI):
    """
    Configura manejadores globales de excepciones.
    """
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """Maneja errores de SQLAlchemy globalmente."""
        logger.error(f"Error SQLAlchemy en {request.url}: {str(exc)}")
        http_exception = handle_database_error(exc)
        return JSONResponse(
            status_code=http_exception.status_code,
            content={"detail": http_exception.detail}
        )
    
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        """Maneja errores de validación Pydantic."""
        logger.error(f"Error de validación en {request.url}: {str(exc)}")
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Error de validación de datos",
                "errors": exc.errors()
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Maneja HTTPExceptions y las logea."""
        logger.warning(f"HTTP {exc.status_code} en {request.url}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Maneja cualquier error no controlado."""
        logger.error(f"Error no controlado en {request.url}: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Error interno del servidor",
                "type": type(exc).__name__
            }
        )
    
    logger.info("Manejadores de errores configurados")