from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from .config import settings

# === CONFIGURACIÓN DE SEGURIDAD ===

# Configuración para hash de contraseñas (bcrypt es muy seguro)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración para tokens JWT - AHORA DESDE CONFIG
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_EXPIRE_MINUTES

# === FUNCIONES DE CONTRASEÑAS ===

def hash_password(password: str) -> str:
    """
    Convierte una contraseña normal en un hash seguro.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña es correcta comparándola con su hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

# === FUNCIONES DE TOKENS JWT (para autenticación futura) ===

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un token JWT para mantener al usuario logueado.
    """
    # Copiar los datos para no modificar el original
    to_encode = data.copy()
    
    # Calcular cuándo expira el token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Agregar tiempo de expiración al token
    to_encode.update({"exp": expire})
    
    # Crear y devolver el token encriptado
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Verifica si un token JWT es válido.
    """
    try:
        # Intentar decodificar el token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Token inválido (expirado, modificado, etc.)
        return None
