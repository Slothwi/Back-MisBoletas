"""
CRUD operations para Usuarios usando SQLAlchemy ORM.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional

from app.models.user import Usuario
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password

# ===== CREAR USUARIO (REGISTER) =====
def create_user(db: Session, user: UserCreate) -> UserRead:
    """Crea un nuevo usuario con contraseña hasheada."""
    # Verificar si el email ya existe
    existing = db.query(Usuario).filter(Usuario.email == user.correo).first()
    if existing:
        raise HTTPException(400, "El email ya está registrado")
    
    # Crear nuevo usuario
    db_user = Usuario(
        nombreusuario=user.nombre,
        email=user.correo,
        contrasenahash=hash_password(user.contrasena)
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserRead(
        idUsuario=db_user.usuarioid,
        nombre=db_user.nombreusuario,
        correo=db_user.email,
        fechaRegistro=db_user.fecharegistro
    )

# ===== OBTENER USUARIO PARA LOGIN =====
def get_user_for_login(db: Session, email: str) -> Optional[dict]:
    """Obtiene usuario con hash de contraseña para validación de login."""
    user = db.query(Usuario).filter(Usuario.email == email).first()
    
    if not user:
        return None
    
    return {
        "idUsuario": user.usuarioid,
        "nombre": user.nombreusuario,
        "correo": user.email,
        "contrasenaHash": user.contrasenahash,
        "fechaRegistro": user.fecharegistro
    }

# ===== ACTUALIZAR CONTRASEÑA =====
def update_user_password(db: Session, user_id: int, new_password: str) -> UserRead:
    """Cambia la contraseña de un usuario."""
    user = db.query(Usuario).filter(Usuario.usuarioid == user_id).first()
    
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    
    user.contrasenahash = hash_password(new_password)
    db.commit()
    db.refresh(user)
    
    return UserRead(
        idUsuario=user.usuarioid,
        nombre=user.nombreusuario,
        correo=user.email,
        fechaRegistro=user.fecharegistro
    )

# ===== ELIMINAR USUARIO =====
def delete_user(db: Session, user_id: int) -> None:
    """Elimina un usuario y sus datos relacionados (cascada)."""
    user = db.query(Usuario).filter(Usuario.usuarioid == user_id).first()
    
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    
    db.delete(user)
    db.commit()

# ===== OBTENER LISTA DE USUARIOS =====
def get_users_list(db: Session) -> List[UserRead]:
    """Obtiene todos los usuarios ordenados por fecha de registro."""
    users = db.query(Usuario).order_by(Usuario.fecharegistro.desc()).all()
    
    return [
        UserRead(
            idUsuario=u.usuarioid,
            nombre=u.nombreusuario,
            correo=u.email,
            fechaRegistro=u.fecharegistro
        ) for u in users
    ]

# ===== BUSCAR USUARIO POR ID =====
def search_user(db: Session, user_id: int) -> Optional[UserRead]:
    """Busca un usuario por su ID."""
    user = db.query(Usuario).filter(Usuario.usuarioid == user_id).first()
    
    if not user:
        return None
    
    return UserRead(
        idUsuario=user.usuarioid,
        nombre=user.nombreusuario,
        correo=user.email,
        fechaRegistro=user.fecharegistro
    )

# ===== ACTUALIZAR USUARIO =====
def update_user(db: Session, user_id: int, user: UserCreate) -> UserRead:
    """Actualiza los datos de un usuario."""
    db_user = db.query(Usuario).filter(Usuario.usuarioid == user_id).first()
    
    if not db_user:
        raise HTTPException(404, "Usuario no encontrado")
    
    # Verificar si el email ya está en uso por otro usuario
    if user.correo != db_user.email:
        existing = db.query(Usuario).filter(Usuario.email == user.correo).first()
        if existing:
            raise HTTPException(400, "El email ya está registrado")
    
    db_user.nombreusuario = user.nombre
    db_user.email = user.correo
    
    if user.contrasena:
        db_user.contrasenahash = hash_password(user.contrasena)
    
    db.commit()
    db.refresh(db_user)
    
    return UserRead(
        idUsuario=db_user.usuarioid,
        nombre=db_user.nombreusuario,
        correo=db_user.email,
        fechaRegistro=db_user.fecharegistro
    )