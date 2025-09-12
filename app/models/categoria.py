"""
Modelo SQLAlchemy para la tabla Categorias.

Define categorías para organizar productos:
- Información: nombre, color para identificación visual
- Pertenencia: cada categoría pertenece a un usuario específico
- Relaciones: con usuario propietario y productos asociados

"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Categoria(Base):
    __tablename__ = "Categorias"
    
    CategoriaID = Column(Integer, primary_key=True, index=True)
    NombreCategoria = Column(String(50), nullable=False)
    Color = Column(String(20))
    UsuarioID = Column(Integer, ForeignKey("Usuarios.UsuarioID"), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="categorias")
    productos = relationship("Producto", secondary="ProductoCategorias", back_populates="categorias")