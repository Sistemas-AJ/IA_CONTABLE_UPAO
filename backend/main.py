import os
import sys
import logging
import asyncio
import time
from contextlib import asynccontextmanager
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Importar configuración y rutas
from app.config import (
    API_HOST, API_PORT, API_RELOAD, CORS_ORIGINS, 
    SYSTEM_NAME, SYSTEM_VERSION, SYSTEM_DESCRIPTION,
    validate_config, get_config, OPENAI_API_KEY
)
from app.routes import chat_router, upload_router, feedback_router, system_router
from app.routes.user_routes import router as user_router
from app.vectorstore import initialize_vectorstore

# Configura el logger raíz para solo mostrar WARNING y ERROR de librerías externas
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

# Configura tu logger principal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger(__name__)

# Variables globales para métricas
startup_time = None
request_count = 0
error_count = 0

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación"""
    global startup_time
    startup_time = time.time()
    
    try:
        # Inicialización
        logger.info(f"Iniciando {SYSTEM_NAME} v{SYSTEM_VERSION}")
        
        # Validar configuración
        validation = validate_config()
        if not validation["is_valid"]:
            for issue in validation["issues"]:
                logger.error(f"Configuración: {issue}")
            raise Exception("Configuración inválida")
        
        logger.info("Configuración validada correctamente")
        
        # Inicializar componentes
        await initialize_components()
        
        logger.info("Sistema iniciado correctamente")
        logger.info(f"API disponible en: http://{API_HOST}:{API_PORT}")
        logger.info(f"Documentación en: http://{API_HOST}:{API_PORT}/docs")
        
        yield
        
    except Exception as e:
        logger.error(f"Error durante inicialización: {e}")
        raise
    finally:
        # Limpieza
        logger.info("Cerrando sistema...")
        await cleanup_components()
        logger.info("Sistema cerrado correctamente")

async def initialize_components():
    """Inicializa todos los componentes del sistema"""
    try:
        # Crear directorios necesarios
        os.makedirs("data/logs", exist_ok=True)
        os.makedirs("data/feedback", exist_ok=True)
        os.makedirs("data/uploads", exist_ok=True)
        os.makedirs("data/vectorstore", exist_ok=True)
        
        logger.info("Inicializando vectorstore...")
        await initialize_vectorstore()
        
        logger.info("Servicios cargados correctamente...")
        
        logger.info("Cargando datos iniciales...")
        await load_initial_data()
        
        logger.info("Inicializando cache...")
        await initialize_cache()
        
        logger.info("Componentes inicializados")
        
    except Exception as e:
        logger.error(f"Error inicializando componentes: {e}")
        raise

async def cleanup_components():
    """Limpia recursos al cerrar"""
    try:
        logger.info("Limpiando servicios...")
        
    except Exception as e:
        logger.error(f"Error durante limpieza: {e}")

async def load_initial_data():
    """Carga datos iniciales si es necesario"""
    try:
        pass
    except Exception as e:
        logger.error(f"Error cargando datos iniciales: {e}")

async def initialize_cache():
    """Inicializa el sistema de cache"""
    try:
        pass
    except Exception as e:
        logger.error(f"Error inicializando cache: {e}")

# Crear aplicación FastAPI
app = FastAPI(
    title=SYSTEM_NAME,
    version=SYSTEM_VERSION,
    description=
        f"""
{SYSTEM_DESCRIPTION}

---

<p align="center">
  <b>👨‍💻 Desarrollador principal</b>
</p>

<ul>
  <li><b>Nombre:</b> Adrian Alejandro Ruiz Carreño</li>
  <li><b>Edad:</b> 19</li>
  <li><b>CEO y dueño:</b> <b>SCORPIONS</b></li>
  <li><b>Desarrollador de la Empresa:</b> Adolfo Jurado</li>
  <li><b>Estudios:</b> UNIVERSIDAD TECNOLOGICA DEL PERÚ (UTP)</li>
</ul>

<p align="center">
  <a href="https://upao.edu.pe">🌐 Sitio web</a> |
  <a href="mailto:adrianalejandroruiz19@gmail.com">✉️ Email</a> |
  <a href="https://github.com/AdrianRuizC">💻 GitHub</a> |
  <a href="https://github.com/SCORPIONS-DEV-INC">💻 GitHub Scorpions</a>
</p>

---

### 🎓 Universidad

- <b>Universidad Privada Antenor Orrego (UPAO)</b>
- Proyecto de patente desarrollado como parte de la formación profesional de sus alumnos de Contabilidad.
- [Sitio web UPAO](https://upao.edu.pe)

---
""",
    contact={
        "name": "Adrian Alejandro Ruiz Carreño",
        "email": "adrianalejandroruiz19@gmail.com",
        "url": "https://upao.edu.pe",
        "x-github": "https://github.com/AdrianRuizCar"
    },
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Middleware de métricas
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Manejador de solicitudes"""
    global request_count, error_count
    
    start_time = time.time()
    request_count += 1
    
    try:
        response = await call_next(request)
        
        if response.status_code >= 400:
            error_count += 1
            
        process_time = time.time() - start_time
        
        # Log de request (sin emojis)
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )
        
        return response
        
    except Exception as e:
        error_count += 1
        logger.error(f"Error procesando request {request.url.path}: {e}")
        raise

# Rutas principales
@app.get("/", response_class=HTMLResponse)
async def root():
    """Página principal"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{SYSTEM_NAME}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Agrega Font Awesome para iconos -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px; 
                margin: 0 auto; 
                padding: 2rem;
                line-height: 1.6;
                color: #333;
            }}
            /* --------- ESTILOS DESARROLLADOR --------- */
            .dev-card {{
                background: #fff;
                margin: 0 auto 2rem auto;
                padding: 2rem 1.5rem 1.5rem 1.5rem;
                border-radius: 18px;
                box-shadow: 0 8px 32px #007acc33;
                max-width: 410px;
                text-align: center;
                position: relative;
                top: 0;
                transition: box-shadow 0.2s, top 0.2s;
            }}
            .dev-card:hover {{
                box-shadow: 0 12px 40px #007acc55;
                top: -4px;
            }}
            .dev-img-rect {{
                width: 100%;
                max-width: 350px;
                height: 220px;
                object-fit: cover;
                border-radius: 16px;
                border: 4px solid #007acc;
                box-shadow: 0 2px 12px #007acc33;
                background: #eaf6fb;
                margin-bottom: 1rem;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }}
            .dev-card h3 {{
                margin-bottom: 0.3rem;
                font-size: 1.25rem;
                color: #007acc;
            }}
            .dev-card p {{
                font-size: 1.18rem;
                font-weight: 600;
                margin: 0;
            }}
            .dev-card .extra-info {{
                font-size: 1.02rem;
                color: #444;
                margin: 0.7rem 0 0.2rem 0;
            }}
            .dev-card .extra-info span {{
                display: inline-block;
                margin: 0 0.7rem 0.5rem 0;
            }}
            .dev-card .empresa {{
                font-size: 1.02rem;
                color: #444;
                margin-top: 0.2rem;
            }}
            /* --------- FIN ESTILOS DESARROLLADOR --------- */

            .header {{ 
                text-align: center; 
                margin-bottom: 2.2rem;
                padding-bottom: 1.2rem;
                border-bottom: 2px solid #007acc;
            }}
            .feature {{ 
                background: #f8f9fa; 
                padding: 1.5rem; 
                margin: 1rem 0; 
                border-radius: 8px;
                border-left: 4px solid #007acc;
            }}
            .links {{ 
                display: flex; 
                gap: 1rem; 
                justify-content: center; 
                margin: 2rem 0;
                flex-wrap: wrap;
            }}
            .btn {{ 
                background: #007acc; 
                color: white; 
                padding: 0.75rem 1.5rem; 
                text-decoration: none; 
                border-radius: 5px;
                font-weight: 500;
                transition: background 0.3s;
            }}
            .btn:hover {{ background: #005fa3; }}
            .version {{ 
                text-align: center; 
                color: #666; 
                font-size: 0.9rem;
                margin-top: 2rem;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 {SYSTEM_NAME}</h1>
            <p>Sistema de Asistente Inteligente para Contabilidad</p>
            <p>Versión {SYSTEM_VERSION}</p>
        </div>
        <div class="dev-card" style="max-width:820px;width:100%;margin:0 auto 2rem auto;display:flex;align-items:center;gap:2.5rem;box-sizing:border-box;box-shadow:0 8px 32px #00ff0033;background:#111;border-radius:22px;padding:2.2rem 2.2rem 2rem 2.2rem;color:#fff;">
            <!-- Información en dos columnas -->
            <div style="flex:2;display:grid;grid-template-columns:1fr 1fr;gap:1.2rem 2.2rem;text-align:left;">
                <div>
                    <h3 style="margin-bottom:0.5rem;color:#00ff00;">👨‍💻 Desarrollador</h3>
                    <b style="color:#00ff00;">Nombre:</b> Adrian Alejandro Ruiz Carreño<br>
                    <b style="color:#00ff00;">Edad:</b> 19<br>
                    <b style="color:#00ff00;">CEO y dueño:</b> <a href="https://green-fox-331799.hostingersite.com/" style="color:#00ff00;text-decoration:none;">SCORPIONS</a><br>
                    <b style="color:#00ff00;">Desarrollador de la empresa:</b> <b>Adolfo Jurado</b><br>
                    <b style="color:#00ff00;">Estudios:</b> UNIVERSIDAD TECNOLÓGICA DEL PERÚ (UTP)
                </div>
                <div>
                    <b style="color:#00ff00;">Tecnologías:</b><br>
                    <span title="Python" style="font-size:2rem;color:#00ff00;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fab fa-python"></i></span>
                    <span title="JavaScript" style="font-size:2rem;color:#fff;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fab fa-js"></i></span>
                    <span title="React" style="font-size:2rem;color:#00ff00;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fab fa-react"></i></span>
                    <span title="Node.js" style="font-size:2rem;color:#fff;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fab fa-node-js"></i></span>
                    <span title="Java" style="font-size:2rem;color:#00ff00;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fab fa-java"></i></span>
                    <span title="FastAPI" style="font-size:2rem;color:#fff;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fas fa-bolt"></i></span>
                    <span title="TailwindCSS" style="font-size:2rem;color:#00ff00;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fas fa-wind"></i></span>
                    <span title="SQLite" style="font-size:2rem;color:#fff;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fas fa-database"></i></span>
                    <span title="PostgreSQL" style="font-size:2rem;color:#00ff00;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fas fa-database"></i></span>
                    <span title="Docker" style="font-size:2rem;color:#fff;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fab fa-docker"></i></span>
                    <span title="Linux" style="font-size:2rem;color:#00ff00;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fab fa-linux"></i></span>
                    <span title="Ethical Hacking" style="font-size:2rem;color:#fff;background:#222;padding:0.3rem 0.5rem;border-radius:8px;margin:0 0.2rem;"><i class="fas fa-user-secret"></i></span>
                </div>
                <div style="grid-column:1/3;margin-top:1.2rem;">
                    <span style="font-weight:600;color:#00ff00;">Contacto:</span>
                    <div style="margin-top:0.3rem;display:flex;flex-wrap:wrap;gap:1.2rem;">
                        <a href="https://green-fox-331799.hostingersite.com/" style="color:#00ff00;text-decoration:none;font-weight:500;">💼 Portafolio</a>
                        <a href="https://green-fox-331799.hostingersite.com/" style="color:#00ff00;text-decoration:none;font-weight:500;">🌐 Sitio web Scorpions</a>
                        <a href="mailto:adrianalejandroruiz19@gmail.com" style="color:#00ff00;text-decoration:none;font-weight:500;">✉️ Email</a>
                        <a href="https://github.com/AdrianRuizC" style="color:#00ff00;text-decoration:none;font-weight:500;">💻 GitHub Personal</a>
                        <a href="https://github.com/SCORPIONS-DEV-INC" style="color:#00ff00;text-decoration:none;font-weight:500;">💻 GitHub Scorpions</a>
                    </div>
                </div>
            </div>
            <!-- Imagen a la derecha -->
            <div style="flex:1;display:flex;justify-content:center;align-items:center;">
                <img class="dev-img-rect" src="/static/ADRIAN_ALEJANDRO_RUIZ_CARREÑO.jpeg" alt="Adrian Alejandro Ruiz Carreño" style="margin:0;max-width:210px;min-width:150px;aspect-ratio:1/1;object-fit:cover;border-radius:18px;border:3px solid #00ff00;box-shadow:0 0 18px #00ff0055;">
            </div>
        </div>

        <div class="feature">
            <h3>📊 Asientos Contables</h3>
            <p>Generación automática de asientos contables según PCGE 2019</p>
        </div>
        
        <div class="feature">
            <h3>📈 Análisis Financiero</h3>
            <p>Cálculo e interpretación de ratios financieros y análisis de estados financieros</p>
        </div>
        
        <div class="feature">
            <h3>🧮 Cálculos Especializados</h3>
            <p>CTS, vacaciones, gratificaciones, depreciación e impuestos</p>
        </div>
        
        <div class="feature">
            <h3>🎓 Contenido Educativo</h3>
            <p>Explicaciones de conceptos contables y normativa tributaria peruana</p>
        </div>
        
        <div class="links">
            <a href="/docs" class="btn">📖 Documentación API</a>
            <a href="/health" class="btn">🏥 Estado del Sistema</a>
            <a href="/api/config" class="btn">ℹ️ Configuración</a>
        </div>
        
        <div class="version">
            Versión {SYSTEM_VERSION} | Universidad Privada Antenor Orrego
        </div>
    </body>
    </html>
    """

@app.get("/api")
async def api_info():
    """Información de la API"""
    return {
        "name": SYSTEM_NAME,
        "version": SYSTEM_VERSION,
        "description": SYSTEM_DESCRIPTION,
        "endpoints": {
            "chat": "/api/chat",
            "upload": "/api/upload", 
            "feedback": "/api/feedback",
            "system": "/api/system"
        },
        "documentation": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Verificación de salud del sistema"""
    global startup_time, request_count, error_count
    
    uptime = time.time() - startup_time if startup_time else 0
    
    return {
        "status": "healthy",
        "uptime": uptime,
        "uptime_human": f"{uptime:.2f} seconds",
        "requests_total": request_count,
        "errors_total": error_count,
        "error_rate": error_count / max(request_count, 1) * 100,
        "timestamp": time.time(),
        "version": SYSTEM_VERSION
    }

@app.get("/api/config")
async def get_app_config():
    """Obtiene configuración de la aplicación"""
    config = get_config()
    
    # Ocultar información sensible
    if "openai" in config:
        config["openai"].pop("api_key", None)
    
    return {
        "config": config,
        "validation": validate_config(),
        "timestamp": time.time()
    }

@app.get("/api/metrics")
async def get_metrics():
    """Obtiene métricas del sistema"""
    global startup_time, request_count, error_count
    
    uptime = time.time() - startup_time if startup_time else 0
    
    return {
        "uptime": uptime,
        "requests": {
            "total": request_count,
            "rate": request_count / max(uptime, 1) * 60,  # requests per minute
        },
        "errors": {
            "total": error_count,
            "rate": error_count / max(request_count, 1) * 100,  # error percentage
        },
        "memory": await get_memory_info(),
        "timestamp": time.time()
    }

async def get_memory_info():
    """Obtiene información de memoria"""
    try:
        import psutil
        process = psutil.Process()
        return {
            "rss": process.memory_info().rss,
            "vms": process.memory_info().vms,
            "percent": process.memory_percent(),
            "available": psutil.virtual_memory().available
        }
    except ImportError:
        return {"error": "psutil no disponible"}

# Incluir routers
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(feedback_router)
app.include_router(system_router)
app.include_router(user_router) 
# Servir archivos estáticos si existen
try:
    if os.path.exists("static"):
        app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    logger.warning(f"No se pudo montar directorio static: {e}")

# Ruta para verificar el estado del sistema
@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": SYSTEM_VERSION,
        "api_key_configured": OPENAI_API_KEY != "dummy-key"
    }

# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no manejado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor", "message": str(exc)}
    )

# Función principal
def main():
    """Función principal para ejecutar el servidor"""
    try:
        logger.info(f"Iniciando servidor en {API_HOST}:{API_PORT}")
        
        uvicorn.run(
            "main:app",
            host=API_HOST,
            port=API_PORT,
            reload=API_RELOAD,
            log_level="info",
            access_log=True,
            use_colors=True  # Desactivar colores para evitar problemas de codificación
        )
        
    except KeyboardInterrupt:
        logger.info("Servidor detenido por usuario")
    except Exception as e:
        logger.error(f"Error ejecutando servidor: {e}")
        raise

if __name__ == "__main__":
    main()