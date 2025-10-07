"""
Dependencias de autenticación para proteger endpoints.

Proporciona:
- get_current_user: Verifica token JWT y devuelve usuario actual
- get_current_active_user: Usuario activo verificado
- Middleware de autenticación opcional
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import verify_token
from app.crud import user as crud_user
from app.db.session import get_db
from app.schemas.user import UserRead

# Configuración de autenticación Bearer
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserRead:
    """
    Dependencia para obtener el usuario actual desde el token JWT.
    
    Uso en endpoints:
    ```python
    @router.get("/protected")
    async def protected_endpoint(current_user: UserRead = Depends(get_current_user)):
        return {"message": f"Hola {current_user.nombre}"}
    ```
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Extraer token del header
        token = credentials.credentials
        
        # Verificar y decodificar token
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
        
        # Obtener email del token
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if email is None or user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Buscar usuario en la base de datos
    try:
        user = crud_user.search_user(db, user_id)
        if user is None:
            raise credentials_exception
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar usuario: {str(e)}"
        )

async def get_current_active_user(
    current_user: UserRead = Depends(get_current_user)
) -> UserRead:
    """
    Dependencia para obtener usuario activo (extensible para agregar validaciones).
    
    Por ahora solo verifica que el usuario exista, pero se puede extender para:
    - Verificar si la cuenta está activa
    - Verificar permisos específicos
    - Verificar roles
    """
    # TODO: Agregar validaciones adicionales si es necesario
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    return current_user

# Dependencia opcional para endpoints que pueden usar auth o no
async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> UserRead | None:
    """
    Dependencia opcional que devuelve el usuario si hay token válido, None si no.
    
    Útil para endpoints públicos que pueden mostrar contenido diferente si hay usuario logueado.
    """
    if credentials is None:
        return None
        
    try:
        token = credentials.credentials
        payload = verify_token(token)
        
        if payload is None:
            return None
            
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
            
        user = crud_user.search_user(db, user_id)
        return user
        
    except Exception:
        # Si hay cualquier error, simplemente devolver None
        return None

# Decorador para marcar endpoints como protegidos (opcional, para documentación)
def require_auth():
    """
    Decorador que documenta que un endpoint requiere autenticación.
    
    Uso:
    ```python
    @require_auth()
    @router.get("/protected")
    async def protected_endpoint(current_user: UserRead = Depends(get_current_user)):
        pass
    ```
    """
    def decorator(func):
        func.__doc__ = (func.__doc__ or "") + "\n\n🔒 Requiere autenticación (Bearer token)"
        return func
    return decorator
