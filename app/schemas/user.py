from pydantic import BaseModel, EmailStr
from datetime import datetime

# Schema que se usa para respuestas (sin contraseña)
class UserRead(BaseModel):
    idUsuario: int
    nombre: str
    correo: EmailStr
    fechaRegistro: datetime

    class Config:
        from_attributes = True

# Schema que se usa para crear usuarios (incluye contraseña)
class UserCreate(BaseModel):
    nombre: str
    correo: EmailStr
    contrasena: str

# Schema para login
class UserLogin(BaseModel):
    correo: EmailStr
    contrasena: str

# Schema para respuesta de login (con token)
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserRead

# Schema para cambiar contraseña
class PasswordChangeRequest(BaseModel):
    nueva_contrasena: str

# Schema para confirmar eliminación de cuenta
class AccountDeleteRequest(BaseModel):
    confirmar_eliminacion: bool = False