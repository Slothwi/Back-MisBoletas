"""
Modelo SQLAlchemy para la tabla Documentos.
Define documentos adjuntos a productos (boletas, garantías, facturas)
Almacena URLs de Google Cloud Storage en lugar de rutas locales.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Documento(Base):
    __tablename__ = "documentos"
    
    # Clave Primaria Autoincremental
    documentoid = Column(Integer, primary_key=True, index=True)
    productoid = Column(Integer, ForeignKey("productos.productoid", ondelete='CASCADE'), nullable=False, index=True)
    
    # Información del archivo
    nombrearchivo = Column(String(255), nullable=False)        # Nombre original del archivo
    url_gcs = Column(String(500), nullable=False)              # URL completa de GCS (público o firmado)
    blob_name = Column(String(500), nullable=False, unique=True)  # Nombre del blob en GCS (para eliminación)
    
    # Metadatos del archivo
    content_type = Column(String(100))                         # Tipo MIME (application/pdf, image/jpeg, etc.)
    size_bytes = Column(BigInteger)                            # Tamaño en bytes
    
    # Timestamps
    fecha_subida = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relación con el producto
    producto = relationship("Producto", back_populates="documentos")
