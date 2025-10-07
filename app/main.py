from fastapi import FastAPI
from app.api.v1 import user, product
from app.core.middleware import setup_middleware
from app.core.error_handlers import setup_exception_handlers
from app.db.session import engine, Base

# Funcion Para Crear Tablas
def create_tables():
    """
    Función que crea todas las tablas de SQLAlchemy en la base de datos de PostgreSQL.
    Se ejecuta al iniciar el servidor (on_startup).
    """
    print("Intentando crear tablas en la base de datos...")
    # Base.metadata contiene la definición de todas tus clases modelo
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente o ya existentes.")

# Crear aplicación FastAPI
app = FastAPI(
    title="MisBoletas API",
    description="API optimizada para gestión de productos, garantías y boletas.",
    version="1.0.0",
    on_startup=[create_tables]  # Crear tablas al iniciar el servidor
)

# Configurar middleware (CORS, logging, etc.)
setup_middleware(app)

# Configurar manejadores de errores globales
setup_exception_handlers(app)

# Registrar routers de endpoints ESENCIALES
app.include_router(user.router, prefix="/api/v1", tags=["Usuarios"])
app.include_router(product.router, prefix="/api/v1", tags=["Productos"])

@app.get("/")

async def root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {
        "message": "MisBoletas API",
        "version": "1.0.0",
        "docs": "/docs"
    }