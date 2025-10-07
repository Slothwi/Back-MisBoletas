"""
Modelo SQLAlchemy para la tabla Categorias.
Permite a los usuarios organizar sus productos.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Categoria(Base):
    # Relación muchos-a-muchos con Producto, utilizando la tabla intermedia
    productos = relationship("Producto", secondary="ProductoCategorias", back_populates="categorias")
    __tablename__ = "Categorias"
    
    # Clave Primaria Autoincremental
    CategoriaID = Column(Integer, primary_key=True, index=True)
    
    # Campos de datos
    NombreCategoria = Column(String(50), nullable=False)
    Color = Column(String(20)) # Para la interfaz de usuario
    
    # Clave Foránea al Usuario
    # Se añade ON DELETE CASCADE para eliminar las categorías del usuario si este se elimina.
    UsuarioID = Column(Integer, ForeignKey("Usuarios.UsuarioID", ondelete='CASCADE'), nullable=False)
