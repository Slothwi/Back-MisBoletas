from fastapi import APIRouter
from app.schemas.user import User
from app.crud import user as crud_user


router=APIRouter()

@router.get("/users")
async def get_users():
    return crud_user.users_list

#Path
@router.get("/user/{id}")
async def get_user(id: int):
    user = crud_user.search_user(id)
    if not user:
        return {"error": "Usuario no encontrado"}
    return user
    

#Query
@router.get("/user/")
async def get_user_query(id: int):
    user = crud_user.search_user(id)
    if not user:
        return {"error": "Usuario no encontrado"}
    return user


##Insertar usuario
@router.post("/user/", status_code=201)
async def create_user(user: User):
    return crud_user.create_user(user)

##Modificar usuario
async def update_user(user: User):
    return crud_user.update_user(user)

## Delete Usuario
@router.delete("/user/{id}")
async def delete_user(id: int):
    return crud_user.delete_user(id)


