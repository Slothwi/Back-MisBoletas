from fastapi import APIRouter, HTTPException
from app.schemas.user import User
from app.crud import user as crud_user

# Router para endpoints de usuarios
router = APIRouter()

# Endpoint para obtener todos los usuarios
@router.get("/users/")
async def get_users():
    usuarios = crud_user.get_users()
    if not usuarios:
        return {"message": "No hay usuarios registrados"}
    return usuarios

# Endpoint para obtener un usuario específico por ID (parámetro de ruta)
@router.get("/users/{id}")
async def get_user(id: int):
    user = crud_user.search_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "idUsuario": user.idUsuario,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "correo": user.correo,
        "fechaRegistro": user.fechaRegistro
    }

# Endpoint para crear un nuevo usuario
@router.post("/users/", status_code=201)
async def create_user(user: User):
    return crud_user.create_user(user)

# Endpoint para actualizar un usuario existente
@router.put("/users/")
async def update_user(user: User):
    return crud_user.update_user(user)

# Endpoint para eliminar un usuario por ID
@router.delete("/users/{id}")
async def delete_user(id: int):
    return crud_user.delete_user(id)
