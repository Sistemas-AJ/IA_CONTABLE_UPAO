"""
Configuración centralizada del sistema
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Cargar variables de entorno desde .env si existe
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))
    logger.info(f"Variables de entorno cargadas desde {env_path}")
else:
    logger.warning(f"Archivo .env no encontrado en {env_path}")

# Configuración del servidor
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "8000"))

# Configuración de OpenAI - Ahora con valor por defecto "dummy-key"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "dummy-key")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Configuración de directorios
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"
LOGS_DIR = DATA_DIR / "logs"

# Crear directorios si no existen
for directory in [DATA_DIR, UPLOAD_DIR, VECTORSTORE_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configuración de vectorstore (NUEVAS CONSTANTES)
VECTOR_INDEX_PATH = VECTORSTORE_DIR / "faiss_index"
EMBED_DIM = 1536  # Dimensión para text-embedding-3-small
VECTORSTORE_METADATA_PATH = VECTORSTORE_DIR / "metadata.json"

# Configuración de archivos
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.xlsx', '.xls', '.csv', '.txt'}

# Configuración de vectorstore
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
EMBEDDING_MODEL = "text-embedding-3-small"

# Configuración de cache
CACHE_TTL = 3600  # 1 hora
CACHE_MAX_SIZE = 1000

# Configuración de API
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "true").lower() == "true"

# Configuración de CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080"
]

# Configuración de logging (SIN EMOJIS para Windows)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuración específica para Windows
WINDOWS_ENCODING = "utf-8"
USE_COLORS = False  # Desactivar colores en Windows

# Configuración de sistema
SYSTEM_NAME = "IA CONTABLE UPAO"
SYSTEM_VERSION = "1.0.0"
SYSTEM_DESCRIPTION = "Asistente inteligente para contabilidad"

# Configuración de modelos
MODEL_SETTINGS: Dict[str, Any] = {
    "temperature": 0.1,
    "max_tokens": 2000,
    "top_p": 0.9,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}

# Configuración de web search
WEB_SEARCH_ENABLED = os.getenv("WEB_SEARCH_ENABLED", "false").lower() == "true"
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID", "")

# Configuración de base de datos (para futuro)
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/app.db")

# Configuración de sesiones
SESSION_TIMEOUT = 3600  # 1 hora
MAX_SESSIONS_PER_USER = 5

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "")

# Configuración de monitoreo
METRICS_ENABLED = os.getenv("METRICS_ENABLED", "true").lower() == "true"
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "")

# Configuración de límites de rate limiting
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "3600"))  # 1 hora

def get_config() -> Dict[str, Any]:
    """Retorna configuración completa del sistema"""
    return {
        "system": {
            "name": SYSTEM_NAME,
            "version": SYSTEM_VERSION,
            "description": SYSTEM_DESCRIPTION
        },
        "api": {
            "host": API_HOST,
            "port": API_PORT,
            "reload": API_RELOAD
        },
        "openai": {
            "model": OPENAI_MODEL,
            "settings": MODEL_SETTINGS
        },
        "storage": {
            "data_dir": str(DATA_DIR),
            "upload_dir": str(UPLOAD_DIR),
            "max_file_size": MAX_FILE_SIZE
        },
        "features": {
            "web_search": WEB_SEARCH_ENABLED,
            "metrics": METRICS_ENABLED
        }
    }

def validate_config() -> Dict[str, Any]:
    """Valida configuración del sistema"""
    issues = []
    
    # Validar OpenAI API Key
    if OPENAI_API_KEY == "dummy-key":
        issues.append("OPENAI_API_KEY está usando valor por defecto. Algunas funciones estarán limitadas.")
    
    # Validar directorios
    for name, path in [
        ("DATA_DIR", DATA_DIR),
        ("UPLOAD_DIR", UPLOAD_DIR),
        ("VECTORSTORE_DIR", VECTORSTORE_DIR)
    ]:
        if not path.exists():
            issues.append(f"Directorio {name} no existe: {path}")
        elif not os.access(path, os.W_OK):
            issues.append(f"No hay permisos de escritura en {name}: {path}")
    
    # Validar configuración de web search
    if WEB_SEARCH_ENABLED and not SEARCH_API_KEY:
        issues.append("Web search habilitado pero SEARCH_API_KEY no configurado")
    
    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "config_summary": get_config()
    }