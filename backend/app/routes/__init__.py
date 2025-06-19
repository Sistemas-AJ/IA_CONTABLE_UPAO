"""
Rutas del sistema IA Contable
"""
from .chat_routes import router as chat_router
from .upload_routes import router as upload_router
from .feedback_routes import router as feedback_router
from .system_routes import router as system_router
from .user_routes import router as user_router

__all__ = ["chat_router", "upload_router", "feedback_router", "system_router", "user_router"]