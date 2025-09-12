"""
Paquete de modelos SQLAlchemy para MisBoletas.

Exporta todos los modelos de la aplicación:
- Usuario: Gestión de usuarios del sistema
- Categoria: Organización de productos por categorías  
- Producto: Productos con garantías y documentación
- Documento: Archivos adjuntos (boletas, garantías, etc.)
- ProductoCategorias: Tabla de relación many-to-many

"""

from .user import Usuario
from .categoria import Categoria
from .producto import Producto
from .documento import Documento
from .producto_categoria import ProductoCategorias

__all__ = ["Usuario", "Categoria", "Producto", "Documento", "ProductoCategorias"]