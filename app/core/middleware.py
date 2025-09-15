"""
Middleware personalizado para la aplicación MisBoletas.

Incluye:
- CORS para el frontend React Native
- Logging de requests
- Manejo global de errores
- Métricas de rendimiento

"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
from typing import Callable

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_cors_middleware(app: FastAPI):
    """
    Agrega middleware CORS para permitir conexiones desde React Native.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En producción, especificar orígenes exactos
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def add_trusted_host_middleware(app: FastAPI):
    """
    Agrega middleware para validar hosts confiables.
    """
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["localhost", "127.0.0.1"]
    )

async def log_requests_middleware(request: Request, call_next: Callable):
    """
    Middleware para logging de todas las requests.
    """
    start_time = time.time()
    
    # Log de request entrante
    logger.info(f"{request.method} {request.url.path} - Cliente: {request.client.host}")
    
    # Procesar request
    try:
        response = await call_next(request)
        
        # Calcular tiempo de procesamiento
        process_time = time.time() - start_time
        
        # Log de response
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Tiempo: {process_time:.3f}s"
        )
        
        # Agregar header con tiempo de procesamiento
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"{request.method} {request.url.path} - "
            f"Error: {str(e)} - "
            f"Tiempo: {process_time:.3f}s"
        )
        raise

def setup_middleware(app: FastAPI):
    """
    Configura todos los middlewares de la aplicación.
    """
    # Orden importante: el primero en agregarse es el último en ejecutarse
    
    # 1. Logging (se ejecuta último)
    app.middleware("http")(log_requests_middleware)
    
    # 2. CORS (se ejecuta penúltimo) 
    add_cors_middleware(app)
    
    # 3. Trusted hosts (se ejecuta primero)
    add_trusted_host_middleware(app)
    
    logger.info("Middleware configurado exitosamente")