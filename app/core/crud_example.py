"""
Ejemplo de CRUD mejorado con manejo de errores de BD.

Muestra cómo usar las nuevas excepciones y manejadores:
- Manejo de errores SQLAlchemy
- Logging apropiado
- Respuestas HTTP correctas
- Transacciones seguras

"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from app.models.user import Usuario
from app.schemas.user import User
from app.core.exceptions import handle_database_error, not_found_exception
import logging

logger = logging.getLogger(__name__)

def create_user_with_error_handling(db: Session, user_data: User) -> Usuario:
    """
    Crea un usuario con manejo completo de errores.
    
    Ejemplo de cómo usar las nuevas excepciones.
    """
    try:
        # Verificar si ya existe (evitar duplicados)
        existing = db.query(Usuario).filter(Usuario.Email == user_data.email).first()
        if existing:
            logger.warning(f"Intento de crear usuario duplicado: {user_data.email}")
            raise handle_database_error(
                IntegrityError("duplicate key", None, None)
            )
        
        # Crear nuevo usuario
        db_user = Usuario(
            NombreUsuario=user_data.name,
            Email=user_data.email,
            ContraseñaHash="temp_hash"  # En el futuro usar security.hash_password()
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"Usuario creado exitosamente: {db_user.UsuarioID}")
        return db_user
        
    except IntegrityError as e:
        logger.error(f"Error de integridad al crear usuario: {str(e)}")
        db.rollback()
        raise handle_database_error(e)
        
    except OperationalError as e:
        logger.error(f"Error operacional al crear usuario: {str(e)}")
        db.rollback()
        raise handle_database_error(e)
        
    except Exception as e:
        logger.error(f"Error inesperado al crear usuario: {str(e)}")
        db.rollback()
        raise handle_database_error(e)

def get_user_with_error_handling(db: Session, user_id: int) -> Usuario:
    """
    Obtiene un usuario con manejo de errores.
    """
    try:
        user = db.query(Usuario).filter(Usuario.UsuarioID == user_id).first()
        if not user:
            logger.warning(f"Usuario no encontrado: {user_id}")
            raise not_found_exception(f"Usuario con ID {user_id} no encontrado")
        
        logger.info(f"Usuario obtenido exitosamente: {user_id}")
        return user
        
    except Exception as e:
        logger.error(f"Error al obtener usuario {user_id}: {str(e)}")
        if "no encontrado" in str(e):
            raise  # Re-raise si ya es un error manejado
        raise handle_database_error(e)

# Ejemplo de uso en endpoint:
"""
from fastapi import Depends
from app.db.session import get_db

@router.post("/users/", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # El manejo de errores se hace automáticamente
        db_user = create_user_with_error_handling(db, user)
        return UserResponse.from_orm(db_user)
    except HTTPException:
        # Los errores ya están manejados, solo re-raise
        raise
"""