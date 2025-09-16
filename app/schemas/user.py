from pydantic import BaseModel
from datetime import date

# Modelo Pydantic para la validación de datos de usuarios
class User(BaseModel):
    id: int          # ID único del usuario
    name: str        # Nombre completo del usuario
    email: str       # Correo electrónico del usuario

