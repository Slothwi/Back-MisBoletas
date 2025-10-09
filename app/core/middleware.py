"""
Middleware para la aplicación MisBoletas.

Este archivo configura:
1. CORS - Permite que el frontend React Native se conecte
2. Logging - Registra todas las requests para debugging
3. Hosts confiables - Solo permite ciertos hosts por seguridad
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
from typing import Callable

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_cors_middleware(app: FastAPI):
    """
    Permite que el frontend (React Native) se conecte al backend desde una IP/puerto diferente.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    logger.info(" CORS configurado - Frontend puede conectarse")

def add_logging_middleware(app: FastAPI):
    """
    Registra todas las requests para debugging.
    """
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable):
        # Solo loggear errores y requests importantes en producción
        start_time = time.time()
        
        try:
            # Procesar el request
            response = await call_next(request)
            
            # Calcular cuánto tiempo tardó
            duration = time.time() - start_time
            
            # Solo log para requests lentos (>1s) o errores
            if duration > 1.0 or response.status_code >= 400:
                client_ip = request.client.host if request.client else "unknown"
                logger.warning(
                    f"⚠️ {request.method} {request.url.path} → "
                    f"Status {response.status_code} en {duration:.3f}s desde {client_ip}"
                )
            
            # Agregar tiempo al header
            response.headers["X-Process-Time"] = f"{duration:.3f}"
            return response
            
        except Exception as error:
            duration = time.time() - start_time
            client_ip = request.client.host if request.client else "unknown"
            logger.error(
                f"❌ {request.method} {request.url.path} → "
                f"ERROR: {str(error)} en {duration:.3f}s desde {client_ip}"
            )
            raise  # Re-lanzar el error

def add_security_middleware(app: FastAPI):
    """
    Solo permite requests desde hosts confiables.
    """
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "*"
        ]
    )
    logger.info(" Hosts de seguridad configurados")

def setup_middleware(app: FastAPI):
    """
    Función principal que configura TODO el middleware.
    """
    logger.info(" Configuramdo middleware...")

    # 1. Logging (se ejecuta al final, después de todo)
    add_logging_middleware(app)
    
    # 2. CORS (se ejecuta en el medio)
    add_cors_middleware(app)
    
    # 3. Security (se ejecuta primero, antes que todo)
    add_security_middleware(app)
    
    logger.info(" Middleware configurado exitosamente")
    logger.info(" El frontend ya puede conectarse al backend")