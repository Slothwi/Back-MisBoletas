from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.product import Product
from app.crud import product as crud_product
from app.db.session import get_db

# Router para endpoints de productos
router = APIRouter()

# Endpoint para obtener todos los productos
@router.get("/products/", response_model=List[Product])
async def get_products(db: Session = Depends(get_db)):
    """Obtiene todos los productos desde la base de datos."""
    return crud_product.get_products_list(db)

# Endpoint para obtener un producto específico por ID
@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Obtiene un producto específico por su ID."""
    return crud_product.search_product_wrapper(db, product_id)

# Endpoint para obtener todos los productos de un usuario específico
@router.get("/products/user/{user_id}", response_model=List[Product])
async def get_products_by_user(user_id: int, db: Session = Depends(get_db)):
    """Obtiene todos los productos de un usuario específico."""
    db_products = crud_product.get_products_by_user(db, user_id)
    return [
        Product(
            ProductoID=p.ProductoID,
            NombreProducto=p.NombreProducto,
            FechaCompra=p.FechaCompra,
            DuracionGarantia=p.DuracionGarantia,
            Marca=p.Marca,
            Modelo=p.Modelo,
            Tienda=p.Tienda,
            Notas=p.Notas,
            UsuarioID=p.UsuarioID
        )
        for p in db_products
    ]

# Endpoint para crear un nuevo producto
@router.post("/products/", response_model=Product, status_code=201)
async def create_product(product: Product, db: Session = Depends(get_db)):
    """Crea un nuevo producto en la base de datos."""
    return crud_product.create_product_wrapper(db, product)

# Endpoint para actualizar un producto existente
@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    """Actualiza un producto existente."""
    # Asegurar que el ID coincida
    product.ProductoID = product_id
    db_product = crud_product.update_product(db, product)
    return Product(
        ProductoID=db_product.ProductoID,
        NombreProducto=db_product.NombreProducto,
        FechaCompra=db_product.FechaCompra,
        DuracionGarantia=db_product.DuracionGarantia,
        Marca=db_product.Marca,
        Modelo=db_product.Modelo,
        Tienda=db_product.Tienda,
        Notas=db_product.Notas,
        UsuarioID=db_product.UsuarioID
    )

# Endpoint para eliminar un producto por ID
@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Elimina un producto de la base de datos."""
    return crud_product.delete_product(db, product_id)
