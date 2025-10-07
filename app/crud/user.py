from app.models.user import Usuario
from app.schemas.user import UserCreate, UserRead
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.core.security import hash_password

# ===== FUNCIONES ESENCIALES PARA LOGIN/REGISTER =====

# Crear usuario usando SP (para REGISTER)
def create_user(db: Session, user: UserCreate):
    try:
        # Hash de la contraseña
        hashed_password = hash_password(user.contrasena)
        
        # Ejecutar stored procedure para crear usuario
        result = db.execute(
            text("""
                EXEC sp_CreateUser 
                @NombreUsuario = :nombre, 
                @Email = :email, 
                @ContraseñaHash = :password
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
            idUsuario=created_user.UsuarioID,
            nombre=created_user.NombreUsuario,
            correo=created_user.Email,
            fechaRegistro=created_user.FechaRegistro
        )
        
    except Exception as e:
        db.rollback()
        error_message = str(e)
        if "ya está registrado" in error_message:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {error_message}")

# Buscar usuario para login usando SP (para AUTENTICACIÓN)
def get_user_for_login(db: Session, email: str):
    try:
        result = db.execute(text("EXEC sp_GetUserForLogin @Email = :email"), 
                                {"email": email})
        user = result.fetchone()
        
        if not user:
            return None
            
        return {
            "idUsuario": user.UsuarioID,
            "nombre": user.NombreUsuario,
            "correo": user.Email,
            "contrasenaHash": user.ContraseñaHash,
            "fechaRegistro": user.FechaRegistro
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en autenticación: {str(e)}")

# Cambiar contraseña usando SP (para RECUPERAR CONTRASEÑA)
def update_user_password(db: Session, user_id: int, new_password: str):
    try:
        # Hash de la nueva contraseña
        hashed_password = hash_password(new_password)
        
        # Ejecutar stored procedure para cambiar contraseña
        result = db.execute(
            text("EXEC sp_UpdateUserPassword @UsuarioID = :user_id, @NuevaContraseñaHash = :password"),
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
            idUsuario=updated_user.UsuarioID,
            nombre=updated_user.NombreUsuario,
            correo=updated_user.Email,
            fechaRegistro=updated_user.FechaRegistro
        )
        
    except Exception as e:
        db.rollback()
        error_message = str(e)
        if "no encontrado" in error_message:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        raise HTTPException(status_code=500, detail=f"Error al cambiar contraseña: {error_message}")

# Eliminar cuenta usando SP (para ELIMINAR CUENTA)
def delete_user_account(db: Session, user_id: int):
    try:
        # Ejecutar stored procedure para eliminar cuenta completa
        result = db.execute(
            text("EXEC sp_DeleteUserAccount @UsuarioID = :user_id"),
            {"user_id": user_id}
        )
        
        response = result.fetchone()
        db.commit()
        
        if response and response.Mensaje:
            return {"message": response.Mensaje}
        else:
            return {"message": "Cuenta eliminada exitosamente"}
            
    except Exception as e:
        db.rollback()
        error_message = str(e)
        if "no encontrado" in error_message:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        raise HTTPException(status_code=500, detail=f"Error al eliminar cuenta: {error_message}")

# ===== FUNCIONES DE TESTING (SQLAlchemy directo) =====

# Obtener todos los usuarios (solo para testing)
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

# Buscar usuario por ID (solo para testing)
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

# Actualizar usuario (solo para testing)
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

# Eliminar usuario (solo para testing)
def delete_user(db: Session, user_id: int):
    u = db.query(Usuario).filter(Usuario.UsuarioID == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(u)
    db.commit()
