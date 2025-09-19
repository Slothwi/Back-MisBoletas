from app.schemas.user import User
from app.models.user import Usuario
from app.db.session import SessionLocal
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

# Función para buscar un usuario por ID en la BBDD
def search_user(user_id: int):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.UsuarioID == user_id).first()
    db.close()
    if not usuario:
        return None
    return {
        "idUsuario": usuario.UsuarioID,
        "nombre": usuario.NombreUsuario,
        "apellido": usuario.Apellido,
        "correo": usuario.Email,
        "fechaRegistro": usuario.FechaRegistro
    }

# Función para obtener todos los usuarios
def get_users():
    db = SessionLocal()
    usuarios = db.query(Usuario).all()
    db.close()
    return [
        {
            "idUsuario": u.UsuarioID,
            "nombre": u.NombreUsuario,
            "apellido": u.Apellido,
            "correo": u.Email,
            "fechaRegistro": u.FechaRegistro
        }
        for u in usuarios
    ]

# Función para crear un nuevo usuario en la BBDD
def create_user(user: User):
    db = SessionLocal()
    # Verificar si el usuario ya existe por correo
    if db.query(Usuario).filter(Usuario.Email == user.email).first():
        db.close()
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    nuevo_usuario = Usuario(
        NombreUsuario=user.name,
        Apellido=user.apellido,
        Email=user.email,
        Contrasena=user.password
    )
    db.add(nuevo_usuario)
    try:
        db.commit()
        db.refresh(nuevo_usuario)
    except IntegrityError:
        db.rollback()
        db.close()
        raise HTTPException(status_code=400, detail="Error de integridad al crear usuario")
    db.close()
    return {
        "idUsuario": nuevo_usuario.UsuarioID,
        "nombre": nuevo_usuario.NombreUsuario,
        "apellido": nuevo_usuario.Apellido,
        "correo": nuevo_usuario.Email,
        "fechaRegistro": nuevo_usuario.FechaRegistro
    }

# Función para actualizar un usuario existente en la BBDD
def update_user(user: User):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.UsuarioID == user.id).first()
    if not usuario:
        db.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.NombreUsuario = user.name
    usuario.Apellido = user.apellido
    usuario.Email = user.email
    db.commit()
    db.refresh(usuario)
    db.close()
    return {
        "idUsuario": usuario.UsuarioID,
        "nombre": usuario.NombreUsuario,
        "apellido": usuario.Apellido,
        "correo": usuario.Email
    }

# Función para eliminar un usuario por ID en la BBDD
def delete_user(user_id: int):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.UsuarioID == user_id).first()
    if not usuario:
        db.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    db.close()
    return {"message": "Usuario eliminado"}
