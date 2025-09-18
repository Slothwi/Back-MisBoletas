from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import User
from app.crud import user as crud_user
from app.db.session import get_db

# Router para endpoints de usuarios
router = APIRouter()

# Endpoint para obtener todos los usuarios
@router.get("/users/", response_model=List[User])
async def get_users(db: Session = Depends(get_db)):
    """Obtiene todos los usuarios desde la base de datos."""
    return crud_user.get_users_list(db)

# Endpoint para obtener un usuario específico por ID (parámetro de ruta)
@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtiene un usuario específico por su ID."""
    return crud_user.search_user_wrapper(db, user_id)

# Endpoint para crear un nuevo usuario
@router.post("/users/", response_model=User, status_code=201)
async def create_user(user: User, db: Session = Depends(get_db)):
    """Crea un nuevo usuario en la base de datos."""
    return crud_user.create_user_wrapper(db, user)

# Endpoint para actualizar un usuario existente
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    """Actualiza un usuario existente."""
    # Asegurar que el ID coincida
    user.id = user_id
    return crud_user.update_user_wrapper(db, user)

# Endpoint para eliminar un usuario por ID
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario de la base de datos."""
    return crud_user.delete_user(db, user_id)


