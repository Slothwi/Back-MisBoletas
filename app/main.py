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
    from app.services.gcs_service import get_gcs_service
    
    # Verificar GCS de forma segura
    gcs_status = "disabled"
    try:
        if settings.gcs_enabled:
            gcs_service = get_gcs_service()
            gcs_status = "connected" if gcs_service else "error"
    except Exception as e:
        gcs_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "environment": settings.ENV,
        "database": "connected",
        "gcs_enabled": settings.gcs_enabled,
        "gcs_status": gcs_status,
        "bucket": settings.gcs_bucket_name if settings.gcs_enabled else None
    }

@app.get("/test-gcs")
async def test_gcs():
    """Endpoint para verificar la configuración de Google Cloud Storage."""
    from app.services.gcs_service import get_gcs_service
    
    if not settings.gcs_enabled:
        return {
            "status": "disabled",
            "message": "Google Cloud Storage no está habilitado"
        }
    
    gcs_service = get_gcs_service()
    
    if not gcs_service:
        return {
            "status": "error",
            "message": "No se pudo inicializar el servicio GCS",
            "gcs_credentials_path": settings.gcs_credentials_path,
            "gcs_bucket_name": settings.gcs_bucket_name
        }
    
    # Intentar listar archivos del bucket (solo verifica conexión)
    try:
        bucket = gcs_service.client.bucket(settings.gcs_bucket_name)
        exists = bucket.exists()
        
        if not exists:
            return {
                "status": "error",
                "message": f"El bucket '{settings.gcs_bucket_name}' no existe o no tienes permisos"
            }
        
        # Contar archivos
        blobs = list(bucket.list_blobs(max_results=10))
        
        return {
            "status": "success",
            "message": "Google Cloud Storage funcionando correctamente",
            "bucket_name": settings.gcs_bucket_name,
            "bucket_exists": True,
            "files_count": len(blobs),
            "sample_files": [blob.name for blob in blobs[:5]]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al conectar con GCS: {str(e)}",
            "bucket_name": settings.gcs_bucket_name
        }


# Para ejecutar con uvicorn desde la terminal
# El puerto se toma de la variable de entorno PORT (Render) o usa 8000 por defecto
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", settings.PORT))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=settings.DEBUG)