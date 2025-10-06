"""
Modelo SQLAlchemy para la tabla Usuarios.
Define la estructura de usuarios del sistema MisBoletas
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Usuario(Base):
    productos = relationship("Producto", back_populates="usuario")
    __tablename__ = "Usuarios"

    UsuarioID = Column(Integer, primary_key=True, index=True)
    NombreUsuario = Column(String(50), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    ContraseñaHash = Column(String(255), nullable=False)
    fechaRegistro = Column(String, nullable=True)  