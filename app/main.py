from fastapi import FastAPI
from app.api.v1 import user, product, documento
from app.core.middleware import setup_middleware
from app.core.error_handlers import setup_exception_handlers
from app.db.session import engine, Base
from app.core.config import settings
import os

# Funcion Para Crear Tablas
def create_tables():
    """
    Función que crea todas las tablas de SQLAlchemy en la base de datos de PostgreSQL.
    Se ejecuta al iniciar el servidor (on_startup).
    """
    print("Intentando crear tablas en la base de datos...")

    """Importar Modelos para que Base.metadata los conozca"""
    from app.models import user, categoria, producto, documento, producto_categoria
    # Base.metadata contiene la definición de todas tus clases modelo
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente o ya existentes.")

# Crear aplicación FastAPI
app = FastAPI(
    title="MisBoletas API",
    description="API optimizada para gestión de productos, garantías y boletas con Google Cloud Storage.",
    version="2.0.0",
    on_startup=[create_tables]  # Crear tablas al iniciar el servidor
)

# Configurar middleware (CORS, logging, etc.)
setup_middleware(app)

# Configurar manejadores de errores globales
setup_exception_handlers(app)

# Registrar routers de endpoints
app.include_router(user.router, prefix="/api/v1", tags=["Usuarios"])
app.include_router(product.router, prefix="/api/v1", tags=["Productos"])
app.include_router(documento.router, prefix="/api/v1", tags=["Documentos"])

@app.get("/")
async def root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {
        "message": "MisBoletas API",
        "version": "2.0.0",
        "docs": "/docs",
        "environment": settings.ENV,
        "gcs_enabled": settings.gcs_enabled
    }

@app.get("/health")
async def health_check():
    """Endpoint de health check para Render."""
    return {
        "status": "healthy",
        "environment": settings.ENV,
        "database": "connected"
    }

# Para ejecutar con uvicorn desde la terminal
# El puerto se toma de la variable de entorno PORT (Render) o usa 8000 por defecto
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", settings.PORT))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=settings.DEBUG)