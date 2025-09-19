from pydantic import BaseModel
from datetime import date

# Modelo Pydantic para la validación de datos de usuarios
class User(BaseModel):
    nombre: str
    apellido: str
    correo: str
    contrasena: str
    fechaRegistro: date | None = None

