"""
Excepciones personalizadas para la aplicación MisBoletas.

Define errores específicos del dominio:
- Errores de autenticación
- Errores de validación de datos
- Errores de base de datos
- Errores de negocio

"""

from fastapi import HTTPException, status

class MisBoletasException(Exception):
    """Excepción base para la aplicación MisBoletas."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class AuthenticationError(MisBoletasException):
    """Error de autenticación de usuario."""
    pass

class AuthorizationError(MisBoletasException):
    """Error de autorización de usuario."""
    pass

class ValidationError(MisBoletasException):
    """Error de validación de datos."""
    pass

class DatabaseError(MisBoletasException):
    """Error de base de datos."""
    pass

class NotFoundError(MisBoletasException):
    """Error cuando un recurso no se encuentra."""
    pass

class DuplicateError(MisBoletasException):
    """Error cuando se intenta crear un recurso duplicado."""
    pass

# Nuevas excepciones específicas de BD
class DatabaseConnectionError(DatabaseError):
    """Error de conexión a la base de datos."""
    pass

class DatabaseIntegrityError(DatabaseError):
    """Error de integridad de datos (unique, foreign key, etc.)."""
    pass

class DatabaseOperationError(DatabaseError):
    """Error durante operación de base de datos."""
    pass

# Funciones helper para crear HTTPExceptions comunes
def create_http_exception(status_code: int, detail: str) -> HTTPException:
    """Crea una HTTPException con el código y detalle especificados."""
    return HTTPException(status_code=status_code, detail=detail)

def unauthorized_exception(detail: str = "No autorizado") -> HTTPException:
    """Crea una excepción 401 Unauthorized."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

def forbidden_exception(detail: str = "Prohibido") -> HTTPException:
    """Crea una excepción 403 Forbidden."""
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )

def not_found_exception(detail: str = "No encontrado") -> HTTPException:
    """Crea una excepción 404 Not Found."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
    )

def conflict_exception(detail: str = "Conflicto") -> HTTPException:
    """Crea una excepción 409 Conflict."""
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail,
    )

def validation_exception(detail: str = "Error de validación") -> HTTPException:
    """Crea una excepción 422 Unprocessable Entity."""
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=detail,
    )

def database_exception(detail: str = "Error de base de datos") -> HTTPException:
    """Crea una excepción 500 Internal Server Error para errores de BD."""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail,
    )

# Funciones para manejo de excepciones SQLAlchemy específicas
def handle_database_error(error: Exception) -> HTTPException:
    """
    Maneja errores de base de datos y los convierte en HTTPExceptions apropiadas.
    
    Args:
        error: Error de SQLAlchemy
        
    Returns:
        HTTPException apropiada
    """
    from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
    import logging
    
    logger = logging.getLogger(__name__)
    logger.error(f"Error de base de datos: {str(error)}")
    
    if isinstance(error, IntegrityError):
        # Error de integridad (unique constraint, foreign key, etc.)
        if "UNIQUE constraint failed" in str(error) or "duplicate key" in str(error).lower():
            return conflict_exception("El recurso ya existe")
        elif "foreign key" in str(error).lower():
            return validation_exception("Referencia inválida a otro recurso")
        else:
            return validation_exception("Error de integridad de datos")
    
    elif isinstance(error, OperationalError):
        # Error operacional (conexión, sintaxis, etc.)
        if "no such table" in str(error).lower():
            return database_exception("Tabla no encontrada en la base de datos")
        elif "database is locked" in str(error).lower():
            return database_exception("Base de datos temporalmente no disponible")
        else:
            return database_exception("Error de conexión a la base de datos")
    
    elif isinstance(error, SQLAlchemyError):
        # Otros errores de SQLAlchemy
        return database_exception("Error interno de base de datos")
    
    else:
        # Error genérico
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )