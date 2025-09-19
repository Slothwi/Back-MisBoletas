"""
Modelo SQLAlchemy para la tabla Productos.

Define productos con información de garantía y documentos:
- Información básica: nombre, marca, modelo, tienda
- Garantía: fecha de compra, duración de garantía
- Organización: notas adicionales, categorías asociadas
- Documentos: boletas, garantías, manuales adjuntos

"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Producto(Base):
    __tablename__ = "Productos"
    
    ProductoID = Column(Integer, primary_key=True, index=True)
    NombreProducto = Column(String(100), nullable=False)
    FechaCompra = Column(Date)
    DuracionGarantia = Column(Integer)
    Marca = Column(String(50))
    Modelo = Column(String(50))
    Tienda = Column(String(50))
    Notas = Column(Text)
    UsuarioID = Column(Integer, ForeignKey("Usuarios.idUsuario"), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="productos")
    documentos = relationship("Documento", back_populates="producto")
    categorias = relationship("Categoria", secondary="ProductoCategorias", back_populates="productos")