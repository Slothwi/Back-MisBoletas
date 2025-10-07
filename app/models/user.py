"""
Modelo SQLAlchemy para la tabla Usuarios.
Define la estructura de usuarios del sistema MisBoletas
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # Necesario para la función NOW() de la base de datos
from app.db.session import Base

class Usuario(Base):
    # Relación con la tabla Productos (un usuario puede tener muchos productos)
    productos = relationship("Producto", back_populates="usuario")
    
    __tablename__ = "Usuarios"

    UsuarioID = Column(Integer, primary_key=True, index=True)
    NombreUsuario = Column(String(50), nullable=False)
    
    # Email debe ser único y con límite de 100 caracteres
    Email = Column(String(100), unique=True, nullable=False)
    
    # Contraseña en Hash (256 es estándar para SHA-256)
    ContraseñaHash = Column(String(256), nullable=False)
    
    # La columna ya no es nullable, ya que tendrá un valor por defecto.
    FechaRegistro = Column(
        DateTime(timezone=False), # Usamos DateTime
        default=func.now(),       # Función NOW() de PostgreSQL
        nullable=False
    )
