"""
Modelo SQLAlchemy para la tabla Documentos.
Define documentos adjuntos a productos
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Documento(Base):
    __tablename__ = "Documentos"
    
    # Clave Primaria Autoincremental
    DocumentoID = Column(Integer, primary_key=True, index=True)
    
    # Campos de datos
    RutaArchivo = Column(String(255), nullable=False)
    TipoArchivo = Column(String(10))
    
    # Clave Foránea a Producto
    # Se añade ON DELETE CASCADE para asegurar que los documentos se eliminen 
    # si el producto padre es eliminado.
    ProductoID = Column(Integer, ForeignKey("Productos.ProductoID", ondelete='CASCADE'), nullable=False)
    
    # Relaciones
    # Relación uno-a-uno (o uno-a-muchos si se permite compartir)
    producto = relationship("Producto", back_populates="documentos")
