from pydantic import BaseModel
from datetime import date

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