"""
Endpoints API para Documentos (Boletas, Garantías, Facturas).
- Upload y Delete usan Stored Procedures
- Listado y lectura usan SQLAlchemy directo
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from app.schemas.documento import (
    DocumentoRead,
    DocumentoUploadResponse,
    DocumentoDelete,
    DocumentoListItem
)
from app.schemas.user import UserRead
from app.crud import documento as crud_documento
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.services.gcs_service import get_gcs_service, GCSService
from app.core.config import settings

# Router para endpoints de documentos
router = APIRouter()

# ===== UPLOAD DE DOCUMENTO =====
@router.post("/productos/{producto_id}/documentos", response_model=DocumentoUploadResponse, status_code=201)
async def upload_documento(
    producto_id: int,
    file: UploadFile = File(..., description="Archivo a subir (PDF, JPG, PNG)"),
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Sube un documento (boleta, garantía, factura) a un producto.
    
    **Flujo:**
    1. Valida que el archivo sea válido (tipo y tamaño)
    2. Sube el archivo a Google Cloud Storage
    3. Guarda la referencia en la base de datos usando Stored Procedure
    4. Retorna la información del documento creado
    
    **Tipos de archivo permitidos:**
    - PDF (.pdf)
    - Imágenes (.jpg, .jpeg, .png, .gif, .webp)
    
    **Tamaño máximo:** Configurado en GCS_MAX_FILE_SIZE_MB (default: 10MB)
    """
    # Verificar que GCS esté habilitado
    if not settings.gcs_enabled:
        raise HTTPException(
            status_code=503,
            detail="Google Cloud Storage no está configurado. Contacta al administrador."
        )
    
    # Obtener servicio de GCS
    gcs_service = get_gcs_service()
    if not gcs_service:
        raise HTTPException(status_code=503, detail="Servicio de GCS no disponible")
    
    try:
        # 1. Subir archivo a GCS
        upload_result = await gcs_service.upload_file(
            file=file,
            user_id=current_user.idUsuario,
            product_id=producto_id
        )
        
        # 2. Guardar referencia en base de datos usando SP
        documento = crud_documento.create_documento_sp(
            db=db,
            producto_id=producto_id,
            user_id=current_user.idUsuario,
            nombre_archivo=upload_result["filename"],
            url_gcs=upload_result["public_url"],
            blob_name=upload_result["blob_name"],
            content_type=upload_result["content_type"],
            size_bytes=upload_result["size_bytes"]
        )
        
        return DocumentoUploadResponse(
            message="Documento subido exitosamente",
            documento=documento
        )
    
    except HTTPException:
        raise
    except Exception as e:
        # Si falla la DB, intentar limpiar el archivo de GCS
        if 'upload_result' in locals():
            try:
                gcs_service.delete_file(upload_result["blob_name"])
            except:
                pass
        
        raise HTTPException(
            status_code=500,
            detail=f"Error al subir documento: {str(e)}"
        )

# ===== OBTENER DOCUMENTOS DE UN PRODUCTO =====
@router.get("/productos/{producto_id}/documentos", response_model=List[DocumentoListItem])
async def get_documentos_by_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Obtiene todos los documentos asociados a un producto.
    
    Solo retorna documentos de productos que pertenecen al usuario autenticado.
    **Lectura directa con SQLAlchemy (sin Stored Procedure).**
    """
    return crud_documento.get_documentos_by_producto(
        db=db,
        producto_id=producto_id,
        user_id=current_user.idUsuario
    )

# ===== OBTENER UN DOCUMENTO ESPECÍFICO =====
@router.get("/documentos/{documento_id}", response_model=DocumentoRead)
async def get_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Obtiene la información de un documento específico por ID.
    
    Solo retorna el documento si pertenece a un producto del usuario autenticado.
    **Lectura directa con SQLAlchemy (sin Stored Procedure).**
    """
    return crud_documento.get_documento_by_id(
        db=db,
        documento_id=documento_id,
        user_id=current_user.idUsuario
    )

# ===== ELIMINAR DOCUMENTO =====
@router.delete("/documentos/{documento_id}", response_model=DocumentoDelete)
async def delete_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Elimina un documento (tanto de la base de datos como de Google Cloud Storage).
    
    **Flujo:**
    1. Verifica que el documento pertenezca al usuario
    2. Elimina el archivo de Google Cloud Storage
    3. Elimina el registro de la base de datos usando Stored Procedure
    
    Solo puede eliminar documentos de productos que pertenecen al usuario autenticado.
    """
    # Verificar que GCS esté habilitado
    if not settings.gcs_enabled:
        raise HTTPException(
            status_code=503,
            detail="Google Cloud Storage no está configurado"
        )
    
    # Obtener servicio de GCS
    gcs_service = get_gcs_service()
    if not gcs_service:
        raise HTTPException(status_code=503, detail="Servicio de GCS no disponible")
    
    try:
        # 1. Eliminar de la base de datos (también obtiene blob_name)
        delete_result = crud_documento.delete_documento_sp(
            db=db,
            documento_id=documento_id,
            user_id=current_user.idUsuario
        )
        
        # 2. Eliminar archivo de GCS
        try:
            gcs_service.delete_file(delete_result["blob_name"])
        except Exception as e:
            # Log warning pero no fallar la operación
            print(f"Advertencia: No se pudo eliminar archivo de GCS: {str(e)}")
        
        return DocumentoDelete(
            message="Documento eliminado exitosamente",
            documentoid=documento_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar documento: {str(e)}"
        )

# ===== OBTENER URL FIRMADA (OPCIONAL) =====
@router.get("/documentos/{documento_id}/signed-url")
async def get_signed_url(
    documento_id: int,
    expiration_seconds: int = 3600,  # 1 hora por defecto
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Genera una URL firmada temporal para acceder a un documento privado.
    
    **Útil si los archivos en GCS son privados en lugar de públicos.**
    **Lectura directa con SQLAlchemy (sin Stored Procedure).**
    
    Args:
        documento_id: ID del documento
        expiration_seconds: Segundos de validez de la URL (default: 3600 = 1 hora)
    
    Returns:
        URL firmada válida temporalmente
    """
    # Verificar que GCS esté habilitado
    if not settings.gcs_enabled:
        raise HTTPException(status_code=503, detail="GCS no configurado")
    
    gcs_service = get_gcs_service()
    if not gcs_service:
        raise HTTPException(status_code=503, detail="Servicio de GCS no disponible")
    
    # Obtener documento (verifica ownership)
    documento = crud_documento.get_documento_by_id(
        db=db,
        documento_id=documento_id,
        user_id=current_user.idUsuario
    )
    
    # Generar URL firmada
    signed_url = gcs_service.get_signed_url(
        blob_name=documento.blob_name,
        expiration_seconds=expiration_seconds
    )
    
    return {
        "documento_id": documento_id,
        "signed_url": signed_url,
        "expires_in_seconds": expiration_seconds
    }
