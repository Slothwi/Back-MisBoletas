"""
Modelo SQLAlchemy para la tabla Productos.
Define productos con información de garantía y documentos
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Producto(Base):
    __tablename__ = "productos"
    
    # Clave Primaria Autoincremental
    productoid = Column(Integer, primary_key=True, index=True)
    
    # Campos de datos
    nombreproducto = Column(String(150), nullable=False)     
    fechacompra = Column(Date)
    duraciongarantia = Column(Integer)
    marca = Column(String(100))                              
    modelo = Column(String(100))                            
    tienda = Column(String(100))                          
    notas = Column(Text)                                    
    
    # Clave Foránea al Usuario
    usuarioid = Column(Integer, ForeignKey("usuarios.usuarioid", ondelete="CASCADE"), nullable=False)
    
    # Relaciones (Relationships)
    # Relación uno-a-muchos: El producto pertenece a un solo usuario
    usuario = relationship("Usuario", back_populates="productos")
    
    # Relación uno-a-muchos: Un producto tiene múltiples documentos (boletas, garantías)
    documentos = relationship(
        "Documento",
        back_populates="producto",
        cascade="all, delete-orphan"
    )
    
    # Relación uno-a-muchos: Un producto puede tener múltiples categorías
    categorias = relationship(
        "Categoria",
        back_populates="producto",
        cascade="all, delete-orphan"
    )
