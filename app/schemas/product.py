from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

# ===== SCHEMAS CORREGIDOS - CON CATEGORÍAS =====

# Schema simple para categoría en productos
class CategoriaSimple(BaseModel):
    CategoriaID: int
    NombreCategoria: str
    Color: Optional[str] = None

# Schema para LEER productos (respuestas de API)
class ProductRead(BaseModel):
    ProductoID: int
    NombreProducto: str
    FechaCompra: Optional[date] = None
    DuracionGarantia: Optional[int] = None
    Marca: Optional[str] = None
    Modelo: Optional[str] = None
    Tienda: Optional[str] = None
    Notas: Optional[str] = None
    UsuarioID: int
    # Nuevos campos para categorías
    categorias: Optional[List[CategoriaSimple]] = []
    
    class Config:
        from_attributes = True

# Schema para CREAR productos (sin ID, campos obligatorios)
class ProductCreate(BaseModel):
    NombreProducto: str = Field(..., min_length=1, max_length=255)
    FechaCompra: Optional[date] = None
    DuracionGarantia: Optional[int] = Field(None, ge=0, le=120)
    Marca: Optional[str] = Field(None, max_length=100)      
    Modelo: Optional[str] = Field(None, max_length=100)         
    Tienda: Optional[str] = Field(None, max_length=255)       
    Notas: Optional[str] = Field(None, max_length=5000)
    # Opcional: IDs de categorías a asignar
    categoria_ids: Optional[List[int]] = []                  
    # UsuarioID se asigna automáticamente desde el token

# Schema para ACTUALIZAR productos (todos los campos opcionales)
class ProductUpdate(BaseModel):
    NombreProducto: Optional[str] = Field(None, min_length=1, max_length=255)
    FechaCompra: Optional[date] = None
    DuracionGarantia: Optional[int] = Field(None, ge=0, le=120)
    Marca: Optional[str] = Field(None, max_length=100)                        
    Modelo: Optional[str] = Field(None, max_length=100)                       
    Tienda: Optional[str] = Field(None, max_length=255)                       
    Notas: Optional[str] = Field(None, max_length=5000)
    # Opcional: IDs de categorías a asignar (reemplaza las existentes)
    categoria_ids: Optional[List[int]] = None

# Schema específico para actualizar solo notas (simplificado)
class ProductNotesUpdate(BaseModel):
    Notas: str = Field(..., max_length=5000)

# ===== SCHEMAS ESPECÍFICOS PARA CATEGORÍAS =====

# Schema para asignar categoría a producto
class ProductCategoriaAsignacion(BaseModel):
    ProductoID: int
    CategoriaID: int
    
# Schema para respuesta de asignación
class ProductCategoriaResponse(BaseModel):
    ProductoID: int
    CategoriaID: int
    NombreProducto: str
    NombreCategoria: str
    Color: Optional[str] = None
    FechaAsignacion: Optional[date] = None

# Schema para productos con información de categorías extendida
class ProductWithCategorias(ProductRead):
    CategoriasNombres: Optional[str] = None  # "Electrónicos, Hogar"
    CategoriasColores: Optional[str] = None  # "#FF0000, #00FF00"
    CantidadCategorias: Optional[int] = 0
    DiasRestantesGarantia: Optional[int] = None
    EstadoGarantia: Optional[str] = None