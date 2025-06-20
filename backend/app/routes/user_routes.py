"""
Rutas para manejo de contexto de usuario
"""
import time
from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["user"])

# Almacén temporal de contextos (en producción usar base de datos)
user-contexts = {}

class UserContextUpdate(BaseModel):
    context: Dict[str, Any]

@router.get("/user-context/{session_id}")
async def get_user_context(session_id: str):
    """Obtiene el contexto del usuario"""
    try:
        context = user_contexts.get(session_id, {})
        return {
            "session_id": session_id,
            "context": context,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo contexto: {str(e)}"
        )

@router.post("/user-context/{session_id}")
async def update_user_context(session_id: str, update: UserContextUpdate):
    """Actualiza el contexto del usuario"""
    try:
        user_contexts[session_id] = update.context
        return {
            "session_id": session_id,
            "status": "updated",
            "context": update.context,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error actualizando contexto: {str(e)}"
        )

@router.delete("/user-context/{session_id}")
async def clear_user_context(session_id: str):
    """Limpia el contexto del usuario"""
    try:
        if session_id in user_contexts:
            del user_contexts[session_id]
            return {
                "session_id": session_id,
                "status": "cleared",
                "timestamp": time.time()
            }
        else:
            raise HTTPException(status_code=404, detail="Contexto no encontrado")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error limpiando contexto: {str(e)}"
        )

@router.get("/user-contexts")
async def get_all_contexts():
    """Obtiene todos los contextos (solo para desarrollo)"""
    return {
        "total_sessions": len(user_contexts),
        "contexts": {
            session_id: {
                "context": context,
                "keys": list(context.keys()) if context else []
            }
            for session_id, context in user_contexts.items()
        },
        "timestamp": time.time()
    }
