from fastapi import APIRouter
from app.schemas.product import Product
from app.crud import product as crud_product

# Router para endpoints de productos
router = APIRouter()

# Endpoint para obtener todos los productos
@router.get("/products/")
async def get_products():
    return crud_product.products_list

# Endpoint para obtener un producto específico por ID
@router.get("/products/{id}")
async def get_product(id: int):
    product = crud_product.search_product(id)
    if not product:
        return {"error": "Producto no encontrado"}
    return product

# Endpoint para obtener todos los productos de un usuario específico
@router.get("/products/user/{user_id}")
async def get_products_by_user(user_id: int):
    user_products = [p for p in crud_product.products_list if p.UsuarioID == user_id]
    return user_products

# Endpoint para crear un nuevo producto
@router.post("/products/", status_code=201)
async def create_product(product: Product):
    return crud_product.create_product(product)

# Endpoint para actualizar un producto existente
@router.put("/products/")
async def update_product(product: Product):
    return crud_product.update_product(product)

# Endpoint para eliminar un producto por ID
@router.delete("/products/{id}")
async def delete_product(id: int):
    return crud_product.delete_product(id)
