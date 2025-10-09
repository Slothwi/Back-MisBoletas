from fastapi import FastAPI
from app.api.v1 import user, product, categorias
from app.core.middleware import setup_middleware
from app.core.error_handlers import setup_exception_handlers

# Crear aplicación FastAPI
app = FastAPI(
    title="MisBoletas API",
    description="API optimizada para gestión de productos, garantías y boletas.",
    version="1.0.0"
)

# Configurar middleware (CORS, logging, etc.)
setup_middleware(app)

# Configurar manejadores de errores globales
setup_exception_handlers(app)

# Registrar routers de endpoints ESENCIALES
app.include_router(user.router, prefix="/api/v1/users", tags=["Usuarios"])
app.include_router(product.router, prefix="/api/v1/products", tags=["Productos"])
app.include_router(categorias.router, prefix="/api/v1/categorias", tags=["Categorías"])

@app.get("/")

async def root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {
        "message": "MisBoletas API",
        "version": "1.0.0",
        "docs": "/docs"
    }