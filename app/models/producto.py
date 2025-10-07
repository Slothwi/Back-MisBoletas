"""
Modelo SQLAlchemy para la tabla Productos.
Define productos con información de garantía y documentos
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Producto(Base):
    __tablename__ = "Productos"
    
    # Clave Primaria Autoincremental
    ProductoID = Column(Integer, primary_key=True, index=True)
    
    # Campos de datos
    NombreProducto = Column(String(255), nullable=False)     
    FechaCompra = Column(Date)
    DuracionGarantia = Column(Integer)
    Marca = Column(String(100))                              
    Modelo = Column(String(100))                            
    Tienda = Column(String(255))                          
    Notas = Column(Text)                                    
    
    # Clave Foránea al Usuario
    UsuarioID = Column(Integer, ForeignKey("Usuarios.UsuarioID"), nullable=False)
    
    # Relaciones (Relationships)
    # Relación uno-a-muchos: El producto pertenece a un solo usuario
    usuario = relationship("Usuario", back_populates="productos")
    
    # Relación uno-a-muchos: Un producto tiene múltiples documentos (boletas, garantías)
    documentos = relationship("Documento", back_populates="producto")
    
    # Relación muchos-a-muchos: Un producto puede tener múltiples categorías
    categorias = relationship("Categoria", secondary="ProductoCategorias", back_populates="productos")
