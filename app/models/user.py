"""
Modelo SQLAlchemy para la tabla Usuarios.
Define la estructura de usuarios del sistema MisBoletas
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # Necesario para la función NOW() de la base de datos
from app.db.session import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    # Columnas principales
    usuarioid = Column(Integer, primary_key=True, index=True)
    nombreusuario = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    contrasenahash = Column(String, nullable=False)
    fecharegistro = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    productos = relationship(
        "Producto",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
