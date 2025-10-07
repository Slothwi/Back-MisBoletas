"""
Modelo SQLAlchemy para la tabla Categorias.
Permite a los usuarios organizar sus productos.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Categoria(Base):
    __tablename__ = "productocategorias"
    
    # Campos exactamente como en el esquema PostgreSQL
    id = Column(Integer, primary_key=True)
    productoid = Column(Integer, ForeignKey('productos.productoid', ondelete='CASCADE'))
    categoria = Column(String(100))
    
    # Relación con el producto
    producto = relationship("Producto", back_populates="categorias")
