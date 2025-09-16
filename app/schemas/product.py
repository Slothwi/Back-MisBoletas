from pydantic import BaseModel
from datetime import date

# Modelo Pydantic para la validación de datos de productos
class Product(BaseModel):
    ProductoID: int           # ID único del producto
    NombreProducto: str       # Nombre del producto
    FechaCompra: date         # Fecha de compra del producto
    DuracionGarantia: int     # Duración de la garantía en meses
    Marca: str                # Marca del producto
    Modelo: str               # Modelo específico del producto
    Tienda: str               # Tienda donde se compró
    Notas: str                # Notas adicionales sobre el producto
    UsuarioID: int            # ID del usuario propietario del producto