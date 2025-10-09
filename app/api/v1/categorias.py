"""
API endpoints para gestión de categorías de productos
Incluye operaciones CRUD completas con     return crud_categori    return crud_categorias.delete_categoria(
        db=db,
        categoria_id=categoria_id,
        user_id=current_user.idUsuario
    )date_categoria(
        db=db,
        categoria_id=categoria_id,
        categoria_data=categoria_update,
        user_id=current_user.idUsuario
    )icación
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.api.dependencies import get_current_user, get_db
from app.crud import categorias as crud_categorias
from app.schemas.categorias import (
    CategoriaCreate, 
    CategoriaUpdate, 
    CategoriaRead, 
    CategoriaWithProducts
)
from app.schemas.user import UserRead

router = APIRouter()

# ===== ENDPOINTS PRINCIPALES =====

@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
async def create_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Crear una nueva categoría para el usuario autenticado
    
    - **nombrecategoria**: Nombre único de la categoría (máximo 50 caracteres)
    - **color**: Color en formato hexadecimal (ej: #FF5733) o color predefinido
    
    Retorna la categoría creada con su ID asignado
    """
    return crud_categorias.create_categoria(
        db=db, 
        categoria=categoria, 
        user_id=current_user.idUsuario
    )

@router.get("/", response_model=List[CategoriaWithProducts])
async def get_categorias(
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Obtener todas las categorías del usuario autenticado
    
    Incluye el conteo de productos asociados a cada categoría
    """
    return crud_categorias.get_categorias_by_user(
        db=db, 
        user_id=current_user.idUsuario
    )

@router.get("/{categoria_id}", response_model=CategoriaRead)
async def get_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Obtener una categoría específica por ID
    
    Solo se pueden consultar categorías propias del usuario
    """
    categoria = crud_categorias.get_categoria_by_id(
        db=db, 
        categoria_id=categoria_id, 
        user_id=current_user.idUsuario
    )
    
    if not categoria:
        raise HTTPException(
            status_code=404, 
            detail="Categoría no encontrada"
        )
    
    return categoria

@router.put("/{categoria_id}", response_model=CategoriaRead)
async def update_categoria(
    categoria_id: int,
    categoria_update: CategoriaUpdate,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Actualizar una categoría existente
    
    Se pueden actualizar de forma parcial los campos:
    - **nombrecategoria**: Nuevo nombre (debe ser único)
    - **color**: Nuevo color en formato hexadecimal
    
    Solo se pueden modificar categorías propias del usuario
    """
    return crud_categorias.update_categoria(
        db=db,
        categoria_id=categoria_id,
        categoria_update=categoria_update,
        user_id=current_user.idUsuario
    )

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Eliminar una categoría
    
    La categoría no puede tener productos asociados para poder ser eliminada
    Solo se pueden eliminar categorías propias del usuario
    """
    success = crud_categorias.delete_categoria(
        db=db,
        categoria_id=categoria_id,
        user_id=current_user.idUsuario
    )
    
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar la categoría"
        )

# ===== ENDPOINTS DE BÚSQUEDA Y ESTADÍSTICAS =====

@router.get("/buscar/nombre/{nombre}", response_model=CategoriaRead)
async def get_categoria_by_name(
    nombre: str,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Buscar una categoría por nombre exacto (no sensible a mayúsculas)
    
    - **nombre**: Nombre de la categoría a buscar
    """
    categoria = crud_categorias.get_categoria_by_name(
        db=db,
        nombre=nombre,
        user_id=current_user.idUsuario
    )
    
    if not categoria:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró una categoría con el nombre '{nombre}'"
        )
    
    return categoria

@router.get("/estadisticas/resumen", response_model=Dict[str, Any])
async def get_categorias_stats(
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Obtener estadísticas y resumen de las categorías del usuario
    
    Incluye:
    - Total de categorías
    - Categoría más usada (con más productos)
    - Categoría menos usada
    - Lista de colores utilizados
    """
    return crud_categorias.get_categorias_stats(
        db=db,
        user_id=current_user.idUsuario
    )

# ===== ENDPOINTS AUXILIARES =====

@router.get("/validar/nombre/{nombre}")
async def validate_categoria_name(
    nombre: str,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Validar si un nombre de categoría está disponible
    
    Útil para validación en tiempo real en el frontend
    """
    categoria_existente = crud_categorias.get_categoria_by_name(
        db=db,
        nombre=nombre,
        user_id=current_user.idUsuario
    )
    
    return {
        "nombre": nombre,
        "disponible": categoria_existente is None,
        "mensaje": "Nombre disponible" if categoria_existente is None else "El nombre ya está en uso"
    }

@router.get("/colores/predefinidos")
async def get_predefined_colors():
    """
    Obtener lista de colores predefinidos para las categorías
    
    Retorna colores recomendados con sus códigos hexadecimales
    """
    from app.schemas.categorias import PREDEFINED_COLORS
    
    return {
        "colores": [
            {"nombre": color, "valor": value} 
            for color, value in PREDEFINED_COLORS.items()
        ],
        "total": len(PREDEFINED_COLORS)
    }


# ===== ENDPOINT PARA PRODUCTOS POR CATEGORÍA =====

@router.get("/{categoria_id}/productos")
async def get_productos_by_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Obtener todos los productos asignados a una categoría específica
    
    Incluye información detallada de garantía y estado
    """
    try:
        from sqlalchemy import text
        result = db.execute(
            text("EXEC sp_GetProductosByCategoria @CategoriaID = :categoria_id, @UsuarioID = :user_id"),
            {
                "categoria_id": categoria_id,
                "user_id": current_user.idUsuario
            }
        )
        
        productos = result.fetchall()
        
        return [
            {
                "ProductoID": p.ProductoID,
                "NombreProducto": p.NombreProducto,
                "FechaCompra": p.FechaCompra,
                "DuracionGarantia": p.DuracionGarantia,
                "Marca": p.Marca,
                "Modelo": p.Modelo,
                "Tienda": p.Tienda,
                "Notas": p.Notas,
                "UsuarioID": p.UsuarioID,
                "DiasRestantesGarantia": p.DiasRestantesGarantia,
                "EstadoGarantia": p.EstadoGarantia
            }
            for p in productos
        ]
        
    except Exception as e:
        error_msg = str(e)
        if "no encontrada" in error_msg:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {error_msg}")



