"""
Modelo SQLAlchemy para la tabla Documentos.
Define documentos adjuntos a productos
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Documento(Base):
    __tablename__ = "documentos"
    
    # Clave Primaria Autoincremental
    documentoid = Column(Integer, primary_key=True, index=True)
    productoid = Column(Integer, ForeignKey("productos.productoid", ondelete='CASCADE'))
    nombrearchivo = Column(String(255))
    rutaarchivo = Column(String)
    
    # Relación con el producto
    producto = relationship("Producto", back_populates="documentos")
