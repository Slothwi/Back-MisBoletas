from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

# ===== SCHEMAS CORREGIDOS - SIN CONFUSIÓN =====

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
    categoria_id: Optional[int] = None  # NUEVO: Categoría del producto
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

# Schema específico para actualizar solo notas (simplificado)
class ProductNotesUpdate(BaseModel):
    Notas: str = Field(..., max_length=5000)

# ===== MANTENER Product PARA COMPATIBILIDAD (DEPRECATED) =====
# TODO: Eliminar cuando se actualicen todos los imports
class Product(ProductRead):
    """DEPRECATED: Usar ProductRead en su lugar"""
    pass