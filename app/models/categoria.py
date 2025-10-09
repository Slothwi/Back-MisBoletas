"""
Modelo SQLAlchemy para la tabla Categorías.
Define categorías de productos con colores y validaciones
Compatible con estructura de BD existente
"""

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base

class Categoria(Base):
    __tablename__ = "Categorias"  # Nombre de tabla en mayúscula como en BD
    
    # Clave Primaria
    CategoriaID = Column(Integer, primary_key=True, index=True)
    
    # Campos principales (nombres como en BD existente)
    NombreCategoria = Column(String(50), nullable=False)
    Color = Column(String(20), nullable=True)  # Permitir null como en BD original
    
    # Clave Foránea al Usuario
    UsuarioID = Column(Integer, ForeignKey("Usuarios.UsuarioID", ondelete="CASCADE"), nullable=False)
    
    # TEMPORALMENTE COMENTADAS - USANDO STORED PROCEDURES
    # Relaciones
    # usuario = relationship("Usuario", back_populates="categorias")
    
    # Relación muchos-a-muchos con productos a través de tabla intermedia
    # productos = relationship(
    #     "Producto", 
    #     secondary="ProductoCategorias", 
    #     back_populates="categorias"
    # )
    
    # Constraint para evitar categorías duplicadas por usuario
    __table_args__ = (
        UniqueConstraint('UsuarioID', 'NombreCategoria', name='uq_usuario_categoria'),
    )
    
