from app.models.user import Usuario
from app.schemas.user import UserCreate, UserRead
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.core.security import hash_password

# Obtener todos los usuarios
def get_users_list(db: Session):
    usuarios = db.query(Usuario).all()
    return [
        UserRead(
            idUsuario=u.UsuarioID,
            nombre=u.NombreUsuario,
            correo=u.Email,
            fechaRegistro=u.fechaRegistro
        )
        for u in usuarios
    ]

# Buscar usuario por ID
def search_user(db: Session, user_id: int):
    u = db.query(Usuario).filter(Usuario.UsuarioID == user_id).first()
    if not u:
        return None
    return UserRead(
        idUsuario=u.UsuarioID,
        nombre=u.NombreUsuario,
        correo=u.Email,
        fechaRegistro=u.fechaRegistro
    )

# Crear usuario
def create_user(db: Session, user: UserCreate):
    # Verificar si el correo ya existe
    if db.query(Usuario).filter(Usuario.Email == user.correo).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Crear instancia del usuario con contraseña hasheada y fecha sin microsegundos
    nuevo_usuario = Usuario(
        NombreUsuario=user.nombre,
        Email=user.correo,
        ContraseñaHash=hash_password(user.contrasena),
        fechaRegistro=datetime.now().replace(microsecond=0)  # quitar microsegundos
    )

    db.add(nuevo_usuario)
    try:
        db.commit()
        db.refresh(nuevo_usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al crear usuario")

    # Retornar usuario sin la contraseña
    return UserRead(
        idUsuario=nuevo_usuario.UsuarioID,
        nombre=nuevo_usuario.NombreUsuario,
        correo=nuevo_usuario.Email,
        fechaRegistro=nuevo_usuario.fechaRegistro
    )

# Actualizar usuario
def update_user(db: Session, user_id: int, user: UserCreate):
    u = db.query(Usuario).filter(Usuario.UsuarioID == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    u.NombreUsuario = user.nombre
    u.Email = user.correo
    if user.contrasena:
        u.ContraseñaHash = hash_password(user.contrasena)
    
    db.commit()
    db.refresh(u)
    
    return UserRead(
        idUsuario=u.UsuarioID,
        nombre=u.NombreUsuario,
        correo=u.Email,
        fechaRegistro=u.fechaRegistro
    )

# Eliminar usuario
def delete_user(db: Session, user_id: int):
    u = db.query(Usuario).filter(Usuario.UsuarioID == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(u)
    db.commit()
