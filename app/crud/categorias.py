from app.schemas.categorias import Categoria
from fastapi import HTTPException

# Lista temporal de categorías para almacenamiento en memoria
categorias_list = [
    Categoria(CategoriaID=1, NombreCategoria="Electrónica", NotasCategoria="Dispositivos y gadgets", productos=[]),
    Categoria(CategoriaID=2, NombreCategoria="Hogar", NotasCategoria="Artículos para el hogar", productos=[])
]

# Función para buscar una categoría por ID
def search_categoria(categoria_id: int):
    for c in categorias_list:
        if c.CategoriaID == categoria_id:
            return c
    return None 

# Función para crear una nueva categoría
def create_categoria(categoria: Categoria):
    if search_categoria(categoria.CategoriaID):
        raise HTTPException(status_code=400, detail="Categoría ya existe")
    categorias_list.append(categoria)
    return categoria

# Función para actualizar una categoría existente
def update_categoria(categoria: Categoria):
    for index, c in enumerate(categorias_list):
        if c.CategoriaID == categoria.CategoriaID:
            categorias_list[index] = categoria
            return categoria
    raise HTTPException(status_code=404, detail="Categoría no encontrada")

# Función para eliminar una categoría por ID
def delete_categoria(categoria_id: int):
    for index, c in enumerate(categorias_list):
        if c.CategoriaID == categoria_id:
            del categorias_list[index]
            return {"message": "Categoría eliminada"}
    raise HTTPException(status_code=404, detail="Categoría no encontrada")

# Función para obtener todas las categorías
def get_all_categorias():
    return categorias_list