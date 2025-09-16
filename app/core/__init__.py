"""
Paquete core de la aplicación MisBoletas.

Contiene:
- config: Configuración centralizada desde .env
- security: Funciones de hash, JWT y autenticación  
- exceptions: Excepciones personalizadas del dominio

"""

from .config import settings
# from .security import hash_password, verify_password, create_access_token, verify_token
from .exceptions import (
    MisBoletasException,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    DatabaseError,
    NotFoundError,
    DuplicateError,
    unauthorized_exception,
    forbidden_exception,
    not_found_exception,
    conflict_exception,
    validation_exception,
)

__all__ = [
    "settings",
    # Security functions (commented until dependencies installed)
    # "hash_password",
    # "verify_password", 
    # "create_access_token",
    # "verify_token",
    # Exceptions
    "MisBoletasException",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "DatabaseError",
    "NotFoundError",
    "DuplicateError",
    "unauthorized_exception",
    "forbidden_exception",
    "not_found_exception",
    "conflict_exception",
    "validation_exception",
]