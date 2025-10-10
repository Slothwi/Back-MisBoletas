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
    ID = Column("id", Integer, primary_key=True)
    ProductoID = Column("productoid", Integer, ForeignKey('productos.productoid', ondelete='CASCADE'))
    Categoria = Column("categoria", String(100))
    
    # Relación con el producto
    producto = relationship("Producto", back_populates="categorias")
