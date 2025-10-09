from app.schemas.product import ProductRead
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException

# ===== FUNCIÓN HELPER PARA ELIMINAR REPETICIÓN =====
def _convert_to_product_schema(row) -> ProductRead:
    """Convierte una fila de BD a ProductRead schema."""
    return ProductRead(
        ProductoID=row.ProductoID,
        NombreProducto=row.NombreProducto,
        FechaCompra=row.FechaCompra,
        DuracionGarantia=row.DuracionGarantia,
        Marca=row.Marca,
        Modelo=row.Modelo,
        Tienda=row.Tienda,
        Notas=row.Notas,
        UsuarioID=row.UsuarioID
    )

def check_product_ownership(product: ProductRead, user_id: int):
    """Verifica que el producto pertenezca al usuario"""
    if product.UsuarioID != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este producto")

# ===== FUNCIONES USADAS EN LA API =====

# Buscar producto por ID usando SP con verificación de ownership
def search_product_wrapper(db: Session, product_id: int, user_id: int):
    try:
        result = db.execute(text("EXEC sp_GetProductById @ProductoID = :product_id"), 
                            {"product_id": product_id})
        product = result.fetchone()
        
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
            
        product_obj = _convert_to_product_schema(product)
        check_product_ownership(product_obj, user_id)
        return product_obj
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar producto: {str(e)}")

# Obtener productos de un usuario específico usando SP
def get_products_by_user(db: Session, user_id: int):
    try:
        result = db.execute(text("EXEC sp_GetProductsByUser @UsuarioID = :user_id"), 
                                {"user_id": user_id})
        products = result.fetchall()
        
        return [_convert_to_product_schema(p) for p in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos del usuario: {str(e)}")

# Crear producto usando SP
def create_product_wrapper(db: Session, product: ProductRead):
    try:
        result = db.execute(
            text("""
                EXEC sp_CreateProduct 
                @NombreProducto = :nombre,
                @FechaCompra = :fecha_compra,
                @DuracionGarantia = :duracion_garantia,
                @Marca = :marca,
                @Modelo = :modelo,
                @Tienda = :tienda,
                @Notas = :notas,
                @UsuarioID = :usuario_id
            """),
            {
                "nombre": product.NombreProducto,
                "fecha_compra": product.FechaCompra,
                "duracion_garantia": product.DuracionGarantia,
                "marca": product.Marca,
                "modelo": product.Modelo,
                "tienda": product.Tienda,
                "notas": product.Notas,
                "usuario_id": product.UsuarioID
            }
        )
        
        created_product = result.fetchone()
        db.commit()
        
        if not created_product:
            raise HTTPException(status_code=400, detail="Error al crear producto")
            
        return _convert_to_product_schema(created_product)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear producto: {str(e)}")

# Actualizar producto usando SP (verificación de ownership en SP)
def update_product(db: Session, product: ProductRead):
    try:
        result = db.execute(
            text("""
                EXEC sp_UpdateProduct 
                @ProductoID = :product_id,
                @NombreProducto = :nombre,
                @FechaCompra = :fecha_compra,
                @DuracionGarantia = :duracion_garantia,
                @Marca = :marca,
                @Modelo = :modelo,
                @Tienda = :tienda,
                @Notas = :notas,
                @UsuarioID = :usuario_id
            """),
            {
                "product_id": product.ProductoID,
                "nombre": product.NombreProducto,
                "fecha_compra": product.FechaCompra,
                "duracion_garantia": product.DuracionGarantia,
                "marca": product.Marca,
                "modelo": product.Modelo,
                "tienda": product.Tienda,
                "notas": product.Notas,
                "usuario_id": product.UsuarioID
            }
        )
        
        updated_product = result.fetchone()
        db.commit()
        
        if not updated_product:
            raise HTTPException(status_code=404, detail="Producto no encontrado o sin permisos")
            
        return _convert_to_product_schema(updated_product)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {str(e)}")

# Eliminar producto usando SP (verificación de ownership en SP)
def delete_product(db: Session, product_id: int, user_id: int):
    try:
        result = db.execute(
            text("""
                EXEC sp_DeleteProduct 
                @ProductoID = :product_id,
                @UsuarioID = :usuario_id
            """),
            {
                "product_id": product_id,
                "usuario_id": user_id
            }
        )
        
        message = result.fetchone()
        db.commit()
        
        if not message:
            raise HTTPException(status_code=404, detail="Producto no encontrado o sin permisos")
            
        return {"message": message[0]}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {str(e)}")