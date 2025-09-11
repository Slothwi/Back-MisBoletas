from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    id: int
    name: str
    email: str

class Product(BaseModel):
    ProductoID: int
    NombreProducto: str
    FechaCompra: date
    DuracionGarantia: int
    Marca: str
    Modelo: str
    Tienda: str
    Notas: str
    UsuarioID: int