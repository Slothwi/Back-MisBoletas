"""
Modelo SQLAlchemy para la tabla Categorias.

Define categorías para organizar productos

"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Categoria(Base):
    productos = relationship("Producto", secondary="ProductoCategorias", back_populates="categorias")
    __tablename__ = "Categorias"
    
    CategoriaID = Column(Integer, primary_key=True, index=True)
    NombreCategoria = Column(String(50), nullable=False)
    Color = Column(String(20))
    UsuarioID = Column(Integer, ForeignKey("Usuarios.UsuarioID"), nullable=False)
    
