from pydantic import BaseModel, EmailStr
from datetime import datetime

# Schema que se usa para respuestas (sin contraseña)
class UserRead(BaseModel):
    idUsuario: int
    nombre: str
    correo: EmailStr
    fechaRegistro: datetime

    class Config:
        orm_mode = True

# Schema que se usa para crear usuarios (incluye contraseña)
class UserCreate(BaseModel):
    nombre: str
    correo: EmailStr
    contrasena: str