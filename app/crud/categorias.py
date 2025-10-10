"""
Operaciones CRUD para Categorías con PostgreSQL.
Gestiona categorías personalizadas por usuario.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.categoria import Categoria, ProductoCategoria
from app.schemas.categorias import CategoriaCreate, CategoriaUpdate
from typing import List, Optional

def get_categoria(db: Session, categoria_id: int, usuario_id: int) -> Optional[Categoria]:
    """Obtener una categoría específica del usuario"""
    return db.query(Categoria).filter(
        Categoria.CategoriaID == categoria_id,
        Categoria.UsuarioID == usuario_id
    ).first()

def get_categorias(db: Session, usuario_id: int, skip: int = 0, limit: int = 100) -> List[Categoria]:
    """Obtener todas las categorías de un usuario"""
    return db.query(Categoria).filter(
        Categoria.UsuarioID == usuario_id
    ).offset(skip).limit(limit).all()

def get_categorias_with_product_count(db: Session, usuario_id: int) -> List[dict]:
    """Obtener categorías con conteo de productos"""
    results = db.query(
        Categoria,
        func.count(ProductoCategoria.ProductoID).label('total_productos')
    ).outerjoin(
        ProductoCategoria, Categoria.CategoriaID == ProductoCategoria.CategoriaID
    ).filter(
        Categoria.UsuarioID == usuario_id
    ).group_by(
        Categoria.CategoriaID
    ).all()
    
    return [
        {
            'CategoriaID': cat.CategoriaID,
            'NombreCategoria': cat.NombreCategoria,
            'Color': cat.Color,
            'UsuarioID': cat.UsuarioID,
            'FechaCreacion': cat.FechaCreacion,
            'TotalProductos': count
        }
        for cat, count in results
    ]

def create_categoria(db: Session, categoria: CategoriaCreate, usuario_id: int) -> Categoria:
    """Crear una nueva categoría"""
    db_categoria = Categoria(
        NombreCategoria=categoria.NombreCategoria,
        Color=categoria.Color,
        UsuarioID=usuario_id
    )
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def update_categoria(db: Session, categoria_id: int, categoria: CategoriaUpdate, usuario_id: int) -> Optional[Categoria]:
    """Actualizar una categoría existente"""
    db_categoria = get_categoria(db, categoria_id, usuario_id)
    if not db_categoria:
        return None
    
    # Actualizar solo los campos proporcionados
    update_data = categoria.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_categoria, field, value)
    
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int, usuario_id: int) -> bool:
    """Eliminar una categoría"""
    db_categoria = get_categoria(db, categoria_id, usuario_id)
    if not db_categoria:
        return False
    
    db.delete(db_categoria)
    db.commit()
    return True

def asignar_categoria_a_producto(db: Session, producto_id: int, categoria_id: int) -> ProductoCategoria:
    """Asignar una categoría a un producto"""
    # Verificar si ya existe la relación
    existing = db.query(ProductoCategoria).filter(
        ProductoCategoria.ProductoID == producto_id,
        ProductoCategoria.CategoriaID == categoria_id
    ).first()
    
    if existing:
        return existing
    
    # Crear nueva relación
    pc = ProductoCategoria(
        ProductoID=producto_id,
        CategoriaID=categoria_id
    )
    db.add(pc)
    db.commit()
    db.refresh(pc)
    return pc

def quitar_categoria_de_producto(db: Session, producto_id: int, categoria_id: int) -> bool:
    """Quitar una categoría de un producto"""
    pc = db.query(ProductoCategoria).filter(
        ProductoCategoria.ProductoID == producto_id,
        ProductoCategoria.CategoriaID == categoria_id
    ).first()
    
    if not pc:
        return False
    
    db.delete(pc)
    db.commit()
    return True