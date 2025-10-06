"""
Modelo SQLAlchemy para la tabla Documentos.
Define documentos adjuntos a productos
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Documento(Base):
    __tablename__ = "Documentos"
    
    DocumentoID = Column(Integer, primary_key=True, index=True)
    RutaArchivo = Column(String(255), nullable=False)
    TipoArchivo = Column(String(10))
    ProductoID = Column(Integer, ForeignKey("Productos.ProductoID"), nullable=False)
    
    # Relaciones
    producto = relationship("Producto", back_populates="documentos")