"""
Modelo SQLAlchemy para la tabla Productos.
Define productos con información de garantía y documentos
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Producto(Base):
    __tablename__ = "Productos"
    
    ProductoID = Column(Integer, primary_key=True, index=True)
    NombreProducto = Column(String(255), nullable=False)     
    FechaCompra = Column(Date)
    DuracionGarantia = Column(Integer)
    Marca = Column(String(100))                              
    Modelo = Column(String(100))                            
    Tienda = Column(String(255))                          
    Notas = Column(Text)                                    
    UsuarioID = Column(Integer, ForeignKey("Usuarios.UsuarioID"), nullable=False)
    
    # TEMPORALMENTE COMENTADAS - CONFLICTO CON STORED PROCEDURES
    # Relaciones
    # usuario = relationship("Usuario", back_populates="productos")
    # documentos = relationship("Documento", back_populates="producto")
    # categorias = relationship("Categoria", secondary="ProductoCategorias", back_populates="productos")