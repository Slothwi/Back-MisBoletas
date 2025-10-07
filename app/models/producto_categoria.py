from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.session import Base

# ==========================================
# Tabla de relación ProductoCategorias
# ==========================================
# Esta tabla es el eslabón intermedio (secondary) que permite que un Producto 
# esté en múltiples Categorías y viceversa.
# Nota: No requiere una clase modelo propia (no hereda de Base), 
# sino que se define como un objeto Table.
ProductoCategorias = Table(
    'ProductoCategorias',
    Base.metadata,
    # Clave Foránea a Productos
    Column('ProductoID', Integer, ForeignKey('Productos.ProductoID', ondelete='CASCADE'), primary_key=True),
    # Clave Foránea a Categorías
    Column('CategoriaID', Integer, ForeignKey('Categorias.CategoriaID', ondelete='CASCADE'), primary_key=True)
)
