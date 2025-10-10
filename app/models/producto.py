"""
Modelo SQLAlchemy para la tabla Productos.
Define productos con información de garantía y documentos
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Producto(Base):
    __tablename__ = "productos"
    
    # Clave Primaria Autoincremental  
    ProductoID = Column("productoid", Integer, primary_key=True, index=True)
    
    # Campos de datos
    NombreProducto = Column("nombreproducto", String(150), nullable=False)     
    FechaCompra = Column("fechacompra", Date)
    DuracionGarantia = Column("duraciongarantia", Integer)
    Marca = Column("marca", String(100))                              
    Modelo = Column("modelo", String(100))                            
    Tienda = Column("tienda", String(100))                          
    Notas = Column("notas", Text)                                    
    
    # Clave Foránea al Usuario
    UsuarioID = Column("usuarioid", Integer, ForeignKey("usuarios.usuarioid", ondelete="CASCADE"), nullable=False)
    
    # Relaciones (Relationships)
    # Relación uno-a-muchos: El producto pertenece a un solo usuario
    usuario = relationship("Usuario", back_populates="productos")
    
    # Relación uno-a-muchos: Un producto tiene múltiples documentos (boletas, garantías)
    documentos = relationship(
        "Documento",
        back_populates="producto",
        cascade="all, delete-orphan"
    )
    
    # Relación uno-a-muchos: Un producto puede tener múltiples categorías
    categorias = relationship(
        "Categoria",
        back_populates="producto",
        cascade="all, delete-orphan"
    )
