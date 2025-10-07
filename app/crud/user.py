from app.models.user import Usuario
from app.schemas.user import UserCreate, UserRead
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.core.security import hash_password

# ===== FUNCIONES ESENCIALES PARA LOGIN/REGISTER =====

# Crear usuario usando función PostgreSQL (para REGISTER)
def create_user(db: Session, user: UserCreate):
    try:
        # Hash de la contraseña
        hashed_password = hash_password(user.contrasena)
        
        # Ejecutar función PostgreSQL para crear usuario
        result = db.execute(
            text("""
                SELECT * FROM fn_createuser(
                    :nombre, 
                    :email, 
                    :password
                )
            """),
            {
                "nombre": user.nombre,
                "email": user.correo,
                "password": hashed_password
            }
        )
        
        # Obtener el resultado antes del commit
        created_user = result.fetchone()
        
        # Hacer commit después de obtener los datos
        db.commit()
        
        if not created_user:
            raise HTTPException(status_code=400, detail="Error al crear usuario")
            
        return UserRead(
            idUsuario=created_user.usuarioid,
            nombre=created_user.nombreusuario,
            correo=created_user.email,
            fechaRegistro=created_user.fecharegistro
        )
        
    except Exception as e:
        db.rollback()
        error_message = str(e)
        if "ya está registrado" in error_message:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {error_message}")

# Buscar usuario para login usando función PostgreSQL
def get_user_for_login(db: Session, email: str):
    try:
        result = db.execute(
            text("""
                SELECT * FROM fn_getuserforlogin(:email)
            """),
            {"email": email}
        )
        user = result.fetchone()
        
        if not user:
            return None
            
        return {
            "idUsuario": user.usuarioid,
            "nombre": user.nombreusuario,
            "correo": user.email,
            "contrasenaHash": user.contrasenahash,
            "fechaRegistro": user.fecharegistro
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en autenticación: {str(e)}")

# Cambiar contraseña usando función PostgreSQL
def update_user_password(db: Session, user_id: int, new_password: str):
    try:
        # Hash de la nueva contraseña
        hashed_password = hash_password(new_password)
        
        # Ejecutar función PostgreSQL para cambiar contraseña
        result = db.execute(
            text("""
                SELECT * FROM fn_updateuserpassword(
                    :user_id, 
                    :password
                )
            """),
            {
                "user_id": user_id,
                "password": hashed_password
            }
        )
        
        updated_user = result.fetchone()
        db.commit()
        
        if not updated_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
        return UserRead(
            idUsuario=updated_user.usuarioid,
            nombre=updated_user.nombreusuario,
            correo=updated_user.email,
            fechaRegistro=updated_user.fecharegistro
        )
        
    except Exception as e:
        db.rollback()
        error_message = str(e)
        if "no encontrado" in error_message:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        raise HTTPException(status_code=500, detail=f"Error al actualizar contraseña: {error_message}")

# Eliminar usuario y sus datos relacionados
def delete_user(db: Session, user_id: int):
    try:
        # Buscar el usuario
        user = db.query(Usuario).filter(Usuario.usuarioid == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Eliminar el usuario y todos sus datos relacionados (cascada)
        db.delete(user)
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")
        
# Obtener lista de usuarios (para administración)
def get_users_list(db: Session):
    try:
        # Ejecutar consulta directa para obtener todos los usuarios
        result = db.execute(
            text("""
                SELECT 
                    usuarioid, 
                    nombreusuario, 
                    email, 
                    fecharegistro 
                FROM usuarios 
                ORDER BY fecharegistro DESC
            """)
        )
        users = result.fetchall()
        
        if not users:
            return []
            
        # Convertir los resultados a la estructura esperada
        return [
            UserRead(
                idUsuario=user.usuarioid,
                nombre=user.nombreusuario,
                correo=user.email,
                fechaRegistro=user.fecharegistro
            ) for user in users
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

# Buscar usuario por ID
def search_user(db: Session, user_id: int):
    try:
        result = db.execute(
            text("""
                SELECT usuarioid, nombreusuario, email, fecharegistro 
                FROM usuarios 
                WHERE usuarioid = :user_id
            """),
            {"user_id": user_id}
        )
        user = result.fetchone()
        if not user:
            return None
        return UserRead(
            idUsuario=user.usuarioid,
            nombre=user.nombreusuario,
            correo=user.email,
            fechaRegistro=user.fecharegistro
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar usuario: {str(e)}")

# Actualizar datos de usuario
def update_user(db: Session, user_id: int, user: UserCreate):
    try:
        u = db.query(Usuario).filter(Usuario.usuarioid == user_id).first()
        if not u:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        u.nombreusuario = user.nombre
        u.email = user.correo
        if user.contrasena:
            u.contrasenahash = hash_password(user.contrasena)
        
        db.commit()
        db.refresh(u)
        
        return UserRead(
            idUsuario=u.usuarioid,
            nombre=u.nombreusuario,
            correo=u.email,
            fechaRegistro=u.fecharegistro
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")