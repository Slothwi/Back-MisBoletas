from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserRead, UserCreate
from app.crud import user as crud_user
from app.db.session import get_db
from app.core.security import hash_password

router = APIRouter()

# Obtener todos los usuarios
@router.get("/users/", response_model=List[UserRead])
async def get_users(db: Session = Depends(get_db)):
    usuarios = crud_user.get_users_list(db)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios registrados")
    return usuarios

# Obtener un usuario por ID
@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    usuario = crud_user.search_user(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Crear un usuario nuevo
@router.post("/users/", response_model=UserRead, status_code=201)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hashear la contraseña antes de guardarla
    user.contrasena = hash_password(user.contrasena)
    return crud_user.create_user(db, user)

# Actualizar un usuario existente
@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    if user.contrasena:
        user.contrasena = hash_password(user.contrasena)
    return crud_user.update_user(db, user_id, user)

# Eliminar un usuario
@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud_user.delete_user(db, user_id)
    return {"message": "Usuario eliminado"}
