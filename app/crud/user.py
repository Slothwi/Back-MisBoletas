from app.schemas.user import User
from fastapi import HTTPException

users_list = [User(id= 1,name="Simon", email="simon@gmail.com"),
            User(id=2, name="Gabriel", email="gabriel@correo.xd"),
            User(id=3, name="Lirit", email="lirit@correo.cdi")]

def search_user(user_id: int):
    user = next((u for u in users_list if u.id == user_id), None)
    if not user:
        return None
    return user

def create_user(user: User):
    if search_user(user.id):
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    users_list.append(user)
    return user

def update_user(user: User):
    for index, u in enumerate(users_list):
        if u.id == user.id:
            users_list[index] = user
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

def delete_user(user_id: int):
    for index, u in enumerate(users_list):
        if u.id == user_id:
            del users_list[index]
            return {"message": "Usuario eliminado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")