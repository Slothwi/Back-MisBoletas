"""
Schemas Pydantic para validación de datos de categorías
Compatible con estructura de BD existente
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
import re

# === COLORES PREDEFINIDOS ===
PREDEFINED_COLORS = {
    "azul": "#007BFF",
    "verde": "#28A745", 
    "rojo": "#DC3545",
    "amarillo": "#FFC107",
    "naranja": "#FD7E14",
    "morado": "#6F42C1",
    "rosa": "#E83E8C",
    "gris": "#6C757D",
    "negro": "#000000",
    "blanco": "#FFFFFF",
    "celeste": "#17A2B8",
    "lima": "#20C997"
}

# === SCHEMAS DE ENTRADA ===

class CategoriaCreate(BaseModel):
    """Schema para crear una nueva categoría"""
    NombreCategoria: str = Field(..., min_length=1, max_length=50, description="Nombre de la categoría")
    Color: str = Field(..., description="Color en formato hexadecimal (#RRGGBB)")
    
    @validator('NombreCategoria')
    def validar_nombre(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('El nombre de la categoría no puede estar vacío')
        if len(v) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v.title()  # Primera letra mayúscula
    
    @validator('Color')
    def validar_color(cls, v):
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('El color debe estar en formato hexadecimal (#RRGGBB)')
        return v.upper()
    
    class Config:
        json_schema_extra = {
            "example": {
                "NombreCategoria": "Electrónicos",
                "Color": "#007BFF"
            }
        }

class CategoriaUpdate(BaseModel):
    """Schema para actualizar una categoría existente"""
    NombreCategoria: Optional[str] = Field(None, min_length=1, max_length=50)
    Color: Optional[str] = Field(None, description="Color en formato hexadecimal")
    
    @validator('NombreCategoria')
    def validar_nombre(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('El nombre de la categoría no puede estar vacío')
            if len(v) < 2:
                raise ValueError('El nombre debe tener al menos 2 caracteres')
            return v.title()
        return v
    
    @validator('Color')
    def validar_color(cls, v):
        if v is not None and not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('El color debe estar en formato hexadecimal (#RRGGBB)')
        return v.upper() if v else v

# === SCHEMAS DE SALIDA ===

class CategoriaRead(BaseModel):
    """Schema para leer datos de categoría"""
    CategoriaID: int
    NombreCategoria: str
    Color: str
    UsuarioID: int
    
    class Config:
        from_attributes = True

class CategoriaWithProducts(CategoriaRead):
    """Schema de categoría con productos asociados"""
    TotalProductos: int = 0
    
class CategoriaStats(BaseModel):
    """Schema para estadísticas de categorías"""
    TotalCategorias: int
    CategoriaMasUsada: Optional[str] = None
    CategoriaMenosUsada: Optional[str] = None
    ColoresDisponibles: List[str] = []
