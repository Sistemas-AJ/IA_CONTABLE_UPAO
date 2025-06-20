"""
Rutas para el sistema de chat
"""
import uuid
import time
from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from pydantic import BaseModel
from ..services.chat_service import chat_service

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Modelos de datos
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_context: Optional[Dict] = None
    history: Optional[List[Dict]] = None  # <-- Agrega esto

class ChatResponse(BaseModel):
    response: str
    session_id: str
    query_type: str
    confidence: float
    metadata: Optional[Dict] = None
    processing_time: Optional[float] = None

class SessionInfo(BaseModel):
    session_id: str
    created_at: str
    message_count: int
    last_activity: str

# Almacenamiento temporal de sesiones (en producción usar Redis/DB)
active_sessions = {}

def get_or_create_session(session_id: Optional[str] = None) -> str:
    """Obtiene o crea una sesión de chat"""
    if session_id and session_id in active_sessions:
        # Actualizar última actividad
        active_sessions[session_id]["last_activity"] = datetime.now().isoformat()
        return session_id
    
    # Crear nueva sesión
    new_session_id = str(uuid.uuid4())
    active_sessions[new_session_id] = {
        "created_at": datetime.now().isoformat(),
        "last_activity": datetime.now().isoformat(),
        "message_count": 0,
        "messages": []
    }
    return new_session_id

@router.post("/message", response_model=ChatResponse)
async def send_message(chat_message: ChatMessage):
    """Envía un mensaje al chatbot"""
    try:
        start_time = time.time()
        
        # Validaciones
        if not chat_message.message.strip():
            raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
        
        if len(chat_message.message) > 2000:
            raise HTTPException(status_code=400, detail="El mensaje es muy largo (máximo 2000 caracteres)")
        
        # Obtener o crear sesión
        session_id = get_or_create_session(chat_message.session_id)
        
        # Procesar mensaje
        result = await chat_service.process_query(
            query=chat_message.message,
            session_id=session_id,
            user_context=chat_message.user_context,
            history=chat_message.history   # <-- AGREGAR ESTA LÍNEA
        )
        
        # Calcular tiempo de procesamiento
        processing_time = time.time() - start_time
        
        # Actualizar sesión
        if session_id in active_sessions:
            active_sessions[session_id]["message_count"] += 1
            active_sessions[session_id]["messages"].append({
                "timestamp": datetime.now().isoformat(),
                "user_message": chat_message.message,
                "bot_response": result["response"],
                "query_type": result.get("query_type", "unknown")
            })
        
        # Preparar respuesta
        return ChatResponse(
            response=result["response"],
            session_id=session_id,
            query_type=result.get("query_type", "unknown"),
            confidence=result.get("confidence", 0.0),
            metadata=result.get("metadata", {}),
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando mensaje: {str(e)}")

@router.get("/sessions", response_model=List[SessionInfo])
async def get_active_sessions():
    """Obtiene lista de sesiones activas"""
    try:
        sessions = []
        for session_id, session_data in active_sessions.items():
            sessions.append(SessionInfo(
                session_id=session_id,
                created_at=session_data["created_at"],
                message_count=session_data["message_count"],
                last_activity=session_data["last_activity"]
            ))
        
        # Ordenar por última actividad
        sessions.sort(key=lambda x: x.last_activity, reverse=True)
        return sessions
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo sesiones: {str(e)}")

@router.get("/health")
async def chat_health():
    """Verifica el estado del servicio de chat"""
    return {
        "status": "healthy",
        "service": "chat",
        "timestamp": time.time(),
        "active_sessions": len(active_sessions)
    }

@router.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """Obtiene información de una sesión"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    return {
        "session_id": session_id,
        "status": "active",
        "timestamp": time.time(),
        "session_data": active_sessions[session_id]
    }

@router.get("/capabilities")
async def get_chat_capabilities():
    """Obtiene las capacidades del chatbot"""
    return {
        "system_name": "IA Contable UPAO",
        "version": "1.0.0",
        "capabilities": {
            "accounting_entries": {
                "description": "Generación de asientos contables según PCGE 2019",
                "examples": [
                    "Registra un préstamo bancario de S/ 50,000",
                    "Asiento contable para compra de mercaderías con IGV"
                ]
            },
            "financial_analysis": {
                "description": "Análisis de ratios y estados financieros",
                "examples": [
                    "Calcula ROE con utilidad S/ 15,000 y patrimonio S/ 100,000",
                    "Analiza ratio de liquidez corriente"
                ]
            },
            "calculations": {
                "description": "Cálculos laborales, tributarios y financieros",
                "examples": [
                    "Calcula CTS de trabajador que gana S/ 3,000",
                    "Depreciación de maquinaria por S/ 30,000"
                ]
            },
            "education": {
                "description": "Explicación de conceptos contables",
                "examples": [
                    "¿Qué es el activo corriente?",
                    "Diferencia entre gasto y costo"
                ]
            }
        }
    }