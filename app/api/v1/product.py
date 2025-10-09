from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.product import (
    ProductRead, ProductCreate, ProductUpdate, 
    CategoriaSimple
)
from app.schemas.user import UserRead
from app.crud import product as crud_product
from app.db.session import get_db
from app.api.dependencies import get_current_user

# Router para endpoints de productos
router = APIRouter()

# ===== ENDPOINTS SIMPLIFICADOS =====

@router.get("/", response_model=List[ProductRead])
async def get_products(
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Obtiene todos los productos del usuario autenticado."""
    return crud_product.get_products_by_user(db, current_user.idUsuario)

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Obtiene un producto específico por ID."""
    return crud_product.search_product_wrapper(db, product_id, current_user.idUsuario)

@router.post("/", response_model=ProductRead, status_code=201)
async def create_product(
    product_data: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Crea un nuevo producto asociado al usuario autenticado."""
    from app.schemas.product import ProductRead
    product = ProductRead(
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

@router.put("/{product_id}", response_model=ProductRead)
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
    from app.schemas.product import ProductRead
    updated_product = ProductRead(
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

@router.delete("/{product_id}")
async def delete_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Elimina un producto del usuario autenticado."""
    return crud_product.delete_product(db, product_id, current_user.idUsuario)


# ===== ENDPOINTS ESENCIALES PARA PRODUCTOS EN CATEGORÍAS =====

@router.post("/{product_id}/categorias/{categoria_id}")
async def agregar_producto_a_categoria(
    product_id: int,
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Agrega un producto a una categoría."""
    try:
        from sqlalchemy import text
        result = db.execute(
            text("EXEC sp_AgregarProductoACategoria @ProductoID = :product_id, @CategoriaID = :categoria_id, @UsuarioID = :user_id"),
            {
                "product_id": product_id,
                "categoria_id": categoria_id, 
                "user_id": current_user.idUsuario
            }
        )
        
        mensaje = result.fetchone()
        db.commit()
        
        return {"mensaje": mensaje.Mensaje if mensaje else "Producto agregado a la categoría"}
        
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        if "ya está en esta categoría" in error_msg:
            raise HTTPException(status_code=400, detail="El producto ya está en esta categoría")
        elif "no encontrado" in error_msg:
            raise HTTPException(status_code=404, detail="Producto o categoría no encontrado")
        raise HTTPException(status_code=500, detail=f"Error: {error_msg}")


@router.delete("/{product_id}/categorias/{categoria_id}")
async def quitar_producto_de_categoria(
    product_id: int,
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Quita un producto de una categoría."""
    try:
        from sqlalchemy import text
        result = db.execute(
            text("EXEC sp_QuitarProductoDeCategoria @ProductoID = :product_id, @CategoriaID = :categoria_id, @UsuarioID = :user_id"),
            {
                "product_id": product_id,
                "categoria_id": categoria_id,
                "user_id": current_user.idUsuario
            }
        )
        
        mensaje = result.fetchone()
        db.commit()
        
        return {"mensaje": mensaje.Mensaje if mensaje else "Producto removido de la categoría"}
        
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        if "no está en esta categoría" in error_msg:
            raise HTTPException(status_code=400, detail="El producto no está en esta categoría")
        elif "no encontrado" in error_msg:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        raise HTTPException(status_code=500, detail=f"Error: {error_msg}")


@router.get("/{product_id}/categorias", response_model=List[CategoriaSimple])
async def obtener_categorias_del_producto(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """Obtiene las categorías donde está un producto."""
    try:
        from sqlalchemy import text
        result = db.execute(
            text("EXEC sp_GetCategoriasDelProducto @ProductoID = :product_id, @UsuarioID = :user_id"),
            {
                "product_id": product_id,
                "user_id": current_user.idUsuario
            }
        )
        
        categorias = result.fetchall()
        
        return [
            CategoriaSimple(
                CategoriaID=cat.CategoriaID,
                NombreCategoria=cat.NombreCategoria,
                Color=cat.Color
            )
            for cat in categorias
        ]
        
    except Exception as e:
        error_msg = str(e)
        if "no encontrado" in error_msg:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        raise HTTPException(status_code=500, detail=f"Error: {error_msg}")