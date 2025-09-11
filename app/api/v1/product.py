from fastapi import APIRouter
from app.schemas.product import Product
from app.crud import product as crud_product

router = APIRouter()

@router.get("/products")
async def get_products():
    return crud_product.products_list

@router.get("/product/{id}")
async def get_product(id: int):
    product = crud_product.search_product(id)
    if not product:
        return {"error": "Producto no encontrado"}
    return product

@router.post("/product/", status_code=201)
async def create_product(product: Product):
    return crud_product.create_product(product)

@router.put("/product/")
async def update_product(product: Product):
    return crud_product.update_product(product)

@router.delete("/product/{id}")
async def delete_product(id: int):
    return crud_product.delete_product(id)
