from fastapi import APIRouter
from app.schemas.categoria import Categoria
from app.crud import categorias as crud_categoria

router = APIRouter()


#Endpoint para obtener todas las categorías
@router.get("/categorias/", response_model=list[Categoria])
def read_categorias():
    return crud_categoria.get_all_categorias()


#Endipoint para crear una nueva categoría
@router.post("/categorias/", response_model=Categoria)
def create_categoria(categoria: Categoria):
    return crud_categoria.create_categoria(categoria)   

#Endpoint para actualizar una categoría existente
@router.put("/categorias/{categoria_id}", response_model=Categoria)
def update_categoria(categoria_id: int, categoria: Categoria):
    categoria.CategoriaID = categoria_id
    return crud_categoria.update_categoria(categoria)

#Endpoint para eliminar una categoría por ID
@router.delete("/categorias/{categoria_id}")
def delete_categoria(categoria_id: int):
    return crud_categoria.delete_categoria(categoria_id)

#Endpoint para obtener una categoría por ID
@router.get("/categorias/{categoria_id}", response_model=Categoria)
def read_categoria(categoria_id: int):
    categoria = crud_categoria.search_categoria(categoria_id)
    if categoria is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria



