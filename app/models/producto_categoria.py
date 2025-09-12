"""
Tabla de asociación many-to-many entre Productos y Categorías.

Permite relaciones flexibles donde:
- Un producto puede pertenecer a múltiples categorías
- Una categoría puede contener múltiples productos

Ejemplos de uso:
- Producto "iPhone" en categorías: "Electrónicos", "Celulares", "Apple"  
- Producto "Cafetera" en categorías: "Electrodomésticos", "Cocina"

Esta tabla intermedia elimina la necesidad de duplicar productos
para diferentes categorizaciones.

"""

from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.session import Base

# Tabla de relación muchos a muchos entre Productos y Categorías
ProductoCategorias = Table(
    'ProductoCategorias',
    Base.metadata,
    Column('ProductoID', Integer, ForeignKey('Productos.ProductoID'), primary_key=True),
    Column('CategoriaID', Integer, ForeignKey('Categorias.CategoriaID'), primary_key=True)
)