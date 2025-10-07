from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.session import Base

# Tabla de relación muchos a muchos entre Productos y Categorías
ProductoCategorias = Table(
    'ProductoCategorias',
    Base.metadata,
    Column('ProductoID', Integer, ForeignKey('Productos.ProductoID'), primary_key=True),
    Column('CategoriaID', Integer, ForeignKey('Categorias.CategoriaID'), primary_key=True)
)