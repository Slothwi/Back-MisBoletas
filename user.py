from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app=FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str


users_list = [User(id= 1,name="Simon", email="simon@gmail.com"),
            User(id=2, name="Gabriel", email="gabriel@correo.xd"),
            User(id=3, name="Lirit", email="lirit@correo.cdi")]


@app.get("/users")
async def users():
    return users_list

#Path
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    

#Query
@app.get("/user/")
async def userquery(id: int):
    return search_user(id)


##Insertar usuario
@app.post("/user/", status_code=201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        HTTPException(status_code=404, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user

##Modificar usuario
@app.put("/user/") 
async def user(user: User):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "Usuario no encontrado"}
    return user


@app.delete("/user/{id}")
async def delete_user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return {"message": "Usuario eliminado"}


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "Usuario no encontrado"}
