"""
Modelo SQLAlchemy para la tabla Usuarios.

Define la estructura de usuarios del sistema MisBoletas:
- Información básica: nombre, email, contraseña
- Relaciones: categorías y productos pertenecientes al usuario
- Constraints: email único, campos requeridos

Tabla: Usuarios
Relaciones:
- 1:N con Categorias (un usuario tiene muchas categorías)
- 1:N con Productos (un usuario tiene muchos productos)

Autor: Configurado para proyecto MisBoletas
Fecha: 2025-09-11
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Usuario(Base):
    __tablename__ = "Usuarios"
    
    UsuarioID = Column(Integer, primary_key=True, index=True)
    NombreUsuario = Column(String(50), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    ContraseñaHash = Column(String(256), nullable=False)
    
    # Relaciones
    categorias = relationship("Categoria", back_populates="usuario")
    productos = relationship("Producto", back_populates="usuario")