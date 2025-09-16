from pydantic import BaseModel;

#Modelo Pydantic para la validación de datos de categorías

class Categoria(BaseModel):
    CategoriaID: int       # ID único de la categoría
    NombreCategoria: str   # Nombre de la categoría
    NotasCategoria: str    # Notas adicionales sobre la categoría
    productos: list = []  # Lista de productos asociados a la categoría
