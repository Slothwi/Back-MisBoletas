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
    existing = db.query(Usuario).filter(Usuario.Email == user.correo).first()
    if existing:
        raise HTTPException(400, "El email ya está registrado")
    
    # Crear nuevo usuario
    db_user = Usuario(
        NombreUsuario=user.nombre,
        Email=user.correo,
        ContrasenaHash=hash_password(user.contrasena)
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserRead(
        idUsuario=db_user.UsuarioID,
        nombre=db_user.NombreUsuario,
        correo=db_user.Email,
        fechaRegistro=db_user.FechaRegistro
    )

# ===== OBTENER USUARIO PARA LOGIN =====
def get_user_for_login(db: Session, email: str) -> Optional[dict]:
    """Obtiene usuario con hash de contraseña para validación de login."""
    user = db.query(Usuario).filter(Usuario.Email == email).first()
    
    if not user:
        return None
    
    return {
        "idUsuario": user.UsuarioID,
        "nombre": user.NombreUsuario,
        "correo": user.Email,
        "contrasenaHash": user.ContrasenaHash,
        "fechaRegistro": user.FechaRegistro
    }

# ===== ACTUALIZAR CONTRASEÑA =====
def update_user_password(db: Session, user_id: int, new_password: str) -> UserRead:
    """Cambia la contraseña de un usuario."""
    user = db.query(Usuario).filter(Usuario.UsuarioID == user_id).first()
    
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    
    user.ContrasenaHash = hash_password(new_password)
    db.commit()
    db.refresh(user)
    
    return UserRead(
        idUsuario=user.UsuarioID,
        nombre=user.NombreUsuario,
        correo=user.Email,
        fechaRegistro=user.FechaRegistro
    )

# ===== ELIMINAR USUARIO =====
def delete_user(db: Session, user_id: int) -> None:
    """Elimina un usuario y sus datos relacionados (cascada)."""
    user = db.query(Usuario).filter(Usuario.UsuarioID == user_id).first()
    
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    
    db.delete(user)
    db.commit()

# ===== OBTENER LISTA DE USUARIOS =====
def get_users_list(db: Session) -> List[UserRead]:
    """Obtiene todos los usuarios ordenados por fecha de registro."""
    users = db.query(Usuario).order_by(Usuario.FechaRegistro.desc()).all()
    
    return [
        UserRead(
            idUsuario=u.UsuarioID,
            nombre=u.NombreUsuario,
            correo=u.Email,
            fechaRegistro=u.FechaRegistro
        ) for u in users
    ]

# ===== BUSCAR USUARIO POR ID =====
def search_user(db: Session, user_id: int) -> Optional[UserRead]:
    """Busca un usuario por su ID."""
    user = db.query(Usuario).filter(Usuario.UsuarioID == user_id).first()
    
    if not user:
        return None
    
    return UserRead(
        idUsuario=user.UsuarioID,
        nombre=user.NombreUsuario,
        correo=user.Email,
        fechaRegistro=user.FechaRegistro
    )

# ===== ACTUALIZAR USUARIO =====
def update_user(db: Session, user_id: int, user: UserCreate) -> UserRead:
    """Actualiza los datos de un usuario."""
    db_user = db.query(Usuario).filter(Usuario.UsuarioID == user_id).first()
    
    if not db_user:
        raise HTTPException(404, "Usuario no encontrado")
    
    # Verificar si el email ya está en uso por otro usuario
    if user.correo != db_user.Email:
        existing = db.query(Usuario).filter(Usuario.Email == user.correo).first()
        if existing:
            raise HTTPException(400, "El email ya está registrado")
    
    db_user.NombreUsuario = user.nombre
    db_user.Email = user.correo
    
    if user.contrasena:
        db_user.ContrasenaHash = hash_password(user.contrasena)
    
    db.commit()
    db.refresh(db_user)
    
    return UserRead(
        idUsuario=db_user.UsuarioID,
        nombre=db_user.NombreUsuario,
        correo=db_user.Email,
        fechaRegistro=db_user.FechaRegistro
    )