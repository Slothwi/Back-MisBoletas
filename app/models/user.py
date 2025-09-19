"""
Modelo SQLAlchemy para la tabla Usuarios.

Define la estructura de usuarios del sistema MisBoletas

Tabla: Usuarios
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Usuario(Base):
    productos = relationship("Producto", back_populates="usuario")
    __tablename__ = "Usuarios"

    idUsuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    fechaRegistro = Column(String, nullable=True)  