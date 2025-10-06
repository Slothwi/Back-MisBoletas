from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.product import ProductRead, ProductCreate, ProductUpdate
from app.schemas.user import UserRead
from app.crud import product as crud_product
from app.db.session import get_db
from app.api.dependencies import get_current_user

# Router para endpoints de productos
router = APIRouter()

# ===== ENDPOINTS SIMPLIFICADOS =====

@router.get("/products", response_model=List[ProductRead])
async def get_products(
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Obtiene todos los productos del usuario autenticado."""
    return crud_product.get_products_by_user(db, current_user.idUsuario)

@router.get("/products/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Obtiene un producto específico por ID."""
    return crud_product.search_product_wrapper(db, product_id, current_user.idUsuario)

@router.post("/products", response_model=ProductRead, status_code=201)
async def create_product(
    product_data: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Crea un nuevo producto asociado al usuario autenticado."""
    from app.schemas.product import Product
    product = Product(
        ProductoID=0,
        NombreProducto=product_data.NombreProducto,
        FechaCompra=product_data.FechaCompra,
        DuracionGarantia=product_data.DuracionGarantia,
        Marca=product_data.Marca or "",
        Modelo=product_data.Modelo or "",
        Tienda=product_data.Tienda or "",
        Notas=product_data.Notas or "",
        UsuarioID=current_user.idUsuario
    )
    return crud_product.create_product_wrapper(db, product)

@router.put("/products/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int, 
    product_data: ProductUpdate, 
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Actualiza un producto existente del usuario autenticado."""
    # Obtener producto existente (con verificación de ownership)
    existing_product = crud_product.search_product_wrapper(db, product_id, current_user.idUsuario)
    
    # Crear producto actualizado
    from app.schemas.product import Product
    updated_product = Product(
        ProductoID=product_id,
        NombreProducto=product_data.NombreProducto or existing_product.NombreProducto,
        FechaCompra=product_data.FechaCompra or existing_product.FechaCompra,
        DuracionGarantia=product_data.DuracionGarantia or existing_product.DuracionGarantia,
        Marca=product_data.Marca or existing_product.Marca,
        Modelo=product_data.Modelo or existing_product.Modelo,
        Tienda=product_data.Tienda or existing_product.Tienda,
        Notas=product_data.Notas or existing_product.Notas,
        UsuarioID=current_user.idUsuario
    )
    return crud_product.update_product(db, updated_product)

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Elimina un producto del usuario autenticado."""
    return crud_product.delete_product(db, product_id, current_user.idUsuario)