"""
CRUD simplificado para Documentos usando SQLAlchemy.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional
from app.models.documento import Documento
from app.models.producto import Producto

# ===== CREAR DOCUMENTO =====
def create_documento(
    db: Session,
    producto_id: int,
    user_id: int,
    nombre_archivo: str,
    url_gcs: str,
    blob_name: str,
    content_type: Optional[str],
    size_bytes: Optional[int]
) -> Documento:
    """Crea un nuevo documento."""
    # Verificar ownership del producto
    producto = db.query(Producto).filter(
        Producto.productoid == producto_id,
        Producto.usuarioid == user_id
    ).first()
    
    if not producto:
        raise HTTPException(404, "Producto no encontrado o sin permisos")
    
    # Crear documento
    documento = Documento(
        productoid=producto_id,
        nombrearchivo=nombre_archivo,
        url_gcs=url_gcs,
        blob_name=blob_name,
        content_type=content_type,
        size_bytes=size_bytes
    )
    db.add(documento)
    db.commit()
    db.refresh(documento)
    return documento

# ===== OBTENER DOCUMENTOS DE UN PRODUCTO =====
def get_documentos_by_producto(
    db: Session,
    producto_id: int,
    user_id: int
) -> List[Documento]:
    """Obtiene todos los documentos de un producto."""
    # Verificar ownership
    producto = db.query(Producto).filter(
        Producto.productoid == producto_id,
        Producto.usuarioid == user_id
    ).first()
    
    if not producto:
        raise HTTPException(404, "Producto no encontrado o sin permisos")
    
    return db.query(Documento).filter(
        Documento.productoid == producto_id
    ).order_by(Documento.fecha_subida.desc()).all()

# ===== OBTENER UN DOCUMENTO POR ID =====
def get_documento_by_id(
    db: Session,
    documento_id: int,
    user_id: int
) -> Documento:
    """Obtiene un documento específico por ID."""
    documento = db.query(Documento).join(Producto).filter(
        Documento.documentoid == documento_id,
        Producto.usuarioid == user_id
    ).first()
    
    if not documento:
        raise HTTPException(404, "Documento no encontrado o sin permisos")
    
    return documento

# ===== ELIMINAR DOCUMENTO =====
def delete_documento(
    db: Session,
    documento_id: int,
    user_id: int
) -> dict:
    """Elimina un documento."""
    documento = db.query(Documento).join(Producto).filter(
        Documento.documentoid == documento_id,
        Producto.usuarioid == user_id
    ).first()
    
    if not documento:
        raise HTTPException(404, "Documento no encontrado o sin permisos")
    
    blob_name = documento.blob_name
    db.delete(documento)
    db.commit()
    
    return {
        "message": "Documento eliminado exitosamente",
        "blob_name": blob_name
    }
