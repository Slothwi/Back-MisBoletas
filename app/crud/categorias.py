"""
CRUD operations para categorías usando Stored Procedures
Compatible con estructura de BD existente
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from fastapi import HTTPException
from typing import List, Optional

from app.schemas.categorias import CategoriaCreate, CategoriaUpdate, CategoriaRead, CategoriaWithProducts

# ===== OPERACIONES CRUD CON STORED PROCEDURES =====

def create_categoria(db: Session, categoria: CategoriaCreate, user_id: int) -> CategoriaRead:
    """
    Crear una nueva categoría usando stored procedure
    """
    try:
        # Ejecutar stored procedure
        result = db.execute(
            text("EXEC sp_CreateCategoria :NombreCategoria, :Color, :UsuarioID"),
            {
                "NombreCategoria": categoria.NombreCategoria,
                "Color": categoria.Color,
                "UsuarioID": user_id
            }
        )
        
        # Obtener resultado
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=500, detail="Error al crear categoría")
        
        db.commit()
        
        return CategoriaRead(
            CategoriaID=row[0],
            NombreCategoria=row[1],
            Color=row[2],
            UsuarioID=row[3]
        )
        
    except Exception as e:
        db.rollback()
        if "Ya existe una categoría con ese nombre" in str(e):
            raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")
        elif "Usuario no encontrado" in str(e):
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        else:
            raise HTTPException(status_code=500, detail=f"Error al crear categoría: {str(e)}")

def get_categorias_by_user(db: Session, user_id: int) -> List[CategoriaWithProducts]:
    """
    Obtener todas las categorías de un usuario usando stored procedure
    """
    try:
        result = db.execute(
            text("EXEC sp_GetCategoriasByUser :UsuarioID"),
            {"UsuarioID": user_id}
        )
        
        categorias = []
        for row in result.fetchall():
            categorias.append(CategoriaWithProducts(
                CategoriaID=row[0],
                NombreCategoria=row[1],
                Color=row[2],
                UsuarioID=row[3],
                TotalProductos=row[4] or 0
            ))
        
        return categorias
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener categorías: {str(e)}")

def get_categoria_by_id(db: Session, categoria_id: int, user_id: int) -> Optional[CategoriaRead]:
    """
    Obtener una categoría específica por ID usando stored procedure
    """
    try:
        result = db.execute(
            text("EXEC sp_GetCategoriaById :CategoriaID, :UsuarioID"),
            {"CategoriaID": categoria_id, "UsuarioID": user_id}
        )
        
        row = result.fetchone()
        if not row:
            return None
            
        return CategoriaRead(
            CategoriaID=row[0],
            NombreCategoria=row[1],
            Color=row[2],
            UsuarioID=row[3]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar categoría: {str(e)}")

def update_categoria(db: Session, categoria_id: int, categoria_update: CategoriaUpdate, user_id: int) -> CategoriaRead:
    """
    Actualizar una categoría usando stored procedure
    """
    try:
        # Si no se proporciona nombre o color, obtener los valores actuales
        if not categoria_update.NombreCategoria or not categoria_update.Color:
            current = get_categoria_by_id(db, categoria_id, user_id)
            if not current:
                raise HTTPException(status_code=404, detail="Categoría no encontrada")
            
            nombre = categoria_update.NombreCategoria or current.NombreCategoria
            color = categoria_update.Color or current.Color
        else:
            nombre = categoria_update.NombreCategoria
            color = categoria_update.Color
        
        result = db.execute(
            text("EXEC sp_UpdateCategoria :CategoriaID, :NombreCategoria, :Color, :UsuarioID"),
            {
                "CategoriaID": categoria_id,
                "NombreCategoria": nombre,
                "Color": color,
                "UsuarioID": user_id
            }
        )
        
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        
        db.commit()
        
        return CategoriaRead(
            CategoriaID=row[0],
            NombreCategoria=row[1],
            Color=row[2],
            UsuarioID=row[3]
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        if "Ya existe otra categoría con ese nombre" in str(e):
            raise HTTPException(status_code=400, detail="Ya existe otra categoría con ese nombre")
        elif "no encontrada" in str(e):
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        else:
            raise HTTPException(status_code=500, detail=f"Error al actualizar categoría: {str(e)}")

def delete_categoria(db: Session, categoria_id: int, user_id: int) -> bool:
    """
    Eliminar una categoría usando stored procedure
    """
    try:
        result = db.execute(
            text("EXEC sp_DeleteCategoria :CategoriaID, :UsuarioID"),
            {"CategoriaID": categoria_id, "UsuarioID": user_id}
        )
        
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        
        db.commit()
        return True
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        if "tiene productos asociados" in str(e):
            raise HTTPException(status_code=400, detail="No se puede eliminar la categoría porque tiene productos asociados")
        elif "no encontrada" in str(e):
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        else:
            raise HTTPException(status_code=500, detail=f"Error al eliminar categoría: {str(e)}")

def get_categoria_by_name(db: Session, nombre: str, user_id: int) -> Optional[CategoriaRead]:
    """
    Buscar categoría por nombre usando stored procedure
    """
    try:
        result = db.execute(
            text("EXEC sp_GetCategoriaByName :NombreCategoria, :UsuarioID"),
            {"NombreCategoria": nombre, "UsuarioID": user_id}
        )
        
        row = result.fetchone()
        if not row:
            return None
            
        return CategoriaRead(
            CategoriaID=row[0],
            NombreCategoria=row[1],
            Color=row[2],
            UsuarioID=row[3]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar categoría por nombre: {str(e)}")

def get_categorias_stats(db: Session, user_id: int) -> dict:
    """
    Obtener estadísticas de categorías usando stored procedure
    """
    try:
        result = db.execute(
            text("EXEC sp_GetCategoriasStats :UsuarioID"),
            {"UsuarioID": user_id}
        )
        
        row = result.fetchone()
        if not row:
            return {
                "TotalCategorias": 0,
                "CategoriaMasUsada": None,
                "CategoriaMenosUsada": None,
                "ColoresDisponibles": []
            }
        
        # Procesar colores (viene como JSON o string)
        colores = []
        if row[3]:  # ColoresDisponibles
            try:
                import json
                colores_json = json.loads(row[3])
                colores = [item["Color"] for item in colores_json]
            except:
                colores = []
        
        return {
            "TotalCategorias": row[0] or 0,
            "CategoriaMasUsada": row[1],
            "CategoriaMenosUsada": row[2],
            "ColoresDisponibles": colores
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")