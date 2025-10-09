"""
CRUD para Documentos.
- Stored Procedures para operaciones críticas: CREAR y ELIMINAR
- SQLAlchemy directo para operaciones de LECTURA
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from typing import List, Optional
from app.schemas.documento import DocumentoRead
from app.models.documento import Documento
from app.models.producto import Producto
from datetime import datetime

# ===== FUNCIÓN HELPER PARA CONVERTIR MODELO A SCHEMA =====
def _convert_to_documento_schema(doc: Documento) -> DocumentoRead:
    """Convierte un modelo Documento a DocumentoRead schema."""
    return DocumentoRead(
        DocumentoID=doc.documentoid,
        ProductoID=doc.productoid,
        NombreArchivo=doc.nombrearchivo,
        UrlGCS=doc.url_gcs,
        BlobName=doc.blob_name,
        ContentType=doc.content_type,
        SizeBytes=doc.size_bytes,
        FechaSubida=doc.fecha_subida
    )

def _convert_row_to_schema(row) -> DocumentoRead:
    """Convierte una fila de resultado SQL a DocumentoRead schema."""
    return DocumentoRead(
        DocumentoID=row.documentoid,
        ProductoID=row.productoid,
        NombreArchivo=row.nombrearchivo,
        UrlGCS=row.url_gcs,
        BlobName=row.blob_name,
        ContentType=row.content_type,
        SizeBytes=row.size_bytes,
        FechaSubida=row.fecha_subida
    )

# ===== CREAR DOCUMENTO (Stored Procedure) =====
def create_documento_sp(
    db: Session,
    producto_id: int,
    user_id: int,
    nombre_archivo: str,
    url_gcs: str,
    blob_name: str,
    content_type: Optional[str],
    size_bytes: Optional[int]
) -> DocumentoRead:
    """
    Crea un nuevo documento usando Stored Procedure.
    
    Args:
        db: Sesión de base de datos
        producto_id: ID del producto
        user_id: ID del usuario (para verificación de ownership)
        nombre_archivo: Nombre original del archivo
        url_gcs: URL pública de GCS
        blob_name: Nombre del blob en GCS
        content_type: Tipo MIME del archivo
        size_bytes: Tamaño en bytes
        
    Returns:
        DocumentoRead con la información del documento creado
        
    Raises:
        HTTPException: Si el producto no existe o no pertenece al usuario
    """
    try:
        result = db.execute(
            text("""
                SELECT * FROM sp_CreateDocumento(
                    :producto_id,
                    :user_id,
                    :nombre_archivo,
                    :url_gcs,
                    :blob_name,
                    :content_type,
                    :size_bytes
                )
            """),
            {
                "producto_id": producto_id,
                "user_id": user_id,
                "nombre_archivo": nombre_archivo,
                "url_gcs": url_gcs,
                "blob_name": blob_name,
                "content_type": content_type,
                "size_bytes": size_bytes
            }
        )
        
        created_doc = result.fetchone()
        db.commit()
        
        if not created_doc:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado o no tienes permisos para agregar documentos"
            )
        
        return _convert_row_to_schema(created_doc)
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear documento: {str(e)}"
        )

# ===== OBTENER DOCUMENTOS DE UN PRODUCTO (SQLAlchemy) =====
def get_documentos_by_producto(
    db: Session,
    producto_id: int,
    user_id: int
) -> List[DocumentoRead]:
    """
    Obtiene todos los documentos de un producto usando SQLAlchemy.
    
    Args:
        db: Sesión de base de datos
        producto_id: ID del producto
        user_id: ID del usuario (para verificación de ownership)
        
    Returns:
        Lista de DocumentoRead
        
    Raises:
        HTTPException: Si el producto no pertenece al usuario
    """
    try:
        # Verificar que el producto pertenece al usuario
        producto = db.query(Producto).filter(
            Producto.productoid == producto_id,
            Producto.usuarioid == user_id
        ).first()
        
        if not producto:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado o no tienes permisos"
            )
        
        # Obtener documentos del producto
        documentos = db.query(Documento).filter(
            Documento.productoid == producto_id
        ).order_by(Documento.fecha_subida.desc()).all()
        
        return [_convert_to_documento_schema(doc) for doc in documentos]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener documentos: {str(e)}"
        )

# ===== OBTENER UN DOCUMENTO POR ID (SQLAlchemy) =====
def get_documento_by_id(
    db: Session,
    documento_id: int,
    user_id: int
) -> DocumentoRead:
    """
    Obtiene un documento específico por ID usando SQLAlchemy.
    
    Args:
        db: Sesión de base de datos
        documento_id: ID del documento
        user_id: ID del usuario (para verificación de ownership)
        
    Returns:
        DocumentoRead
        
    Raises:
        HTTPException: Si el documento no existe o no pertenece al usuario
    """
    try:
        # Obtener documento con join a producto para verificar ownership
        documento = db.query(Documento).join(Producto).filter(
            Documento.documentoid == documento_id,
            Producto.usuarioid == user_id
        ).first()
        
        if not documento:
            raise HTTPException(
                status_code=404,
                detail="Documento no encontrado o no tienes permisos"
            )
        
        return _convert_to_documento_schema(documento)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener documento: {str(e)}"
        )

# ===== ELIMINAR DOCUMENTO (Stored Procedure) =====
def delete_documento_sp(
    db: Session,
    documento_id: int,
    user_id: int
) -> dict:
    """
    Elimina un documento usando SP.
    
    Args:
        db: Sesión de base de datos
        documento_id: ID del documento a eliminar
        user_id: ID del usuario (para verificación de ownership)
        
    Returns:
        Dict con información del blob_name (para eliminación de GCS)
        
    Raises:
        HTTPException: Si el documento no existe o no pertenece al usuario
    """
    try:
        # Primero obtener el blob_name para eliminarlo de GCS
        doc = get_documento_by_id(db, documento_id, user_id)
        blob_name = doc.blob_name
        
        # Ejecutar SP de eliminación
        result = db.execute(
            text("SELECT * FROM sp_DeleteDocumento(:documento_id, :user_id)"),
            {"documento_id": documento_id, "user_id": user_id}
        )
        
        db.commit()
        
        return {
            "message": "Documento eliminado exitosamente",
            "blob_name": blob_name
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar documento: {str(e)}"
        )
