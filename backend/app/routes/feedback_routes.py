"""
Rutas para sistema de feedback
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from ..services.feedback_service import feedback_service

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

# Modelos de datos
class FeedbackSubmission(BaseModel):
    session_id: str
    query: str = Field(..., max_length=500)
    response: str = Field(..., max_length=1000)
    rating: int = Field(..., ge=1, le=5)
    feedback_text: Optional[str] = Field(None, max_length=500)
    categories: Optional[List[str]] = None
    user_id: Optional[str] = None
    response_time: Optional[float] = None
    query_type: Optional[str] = None

class FeedbackResponse(BaseModel):
    success: bool
    message: str
    feedback_id: Optional[str] = None

@router.post("/submit", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackSubmission):
    """Enviar feedback sobre una respuesta"""
    try:
        result = feedback_service.submit_feedback(
            session_id=feedback.session_id,
            query=feedback.query,
            response=feedback.response,
            rating=feedback.rating,
            feedback_text=feedback.feedback_text,
            categories=feedback.categories or [],
            user_id=feedback.user_id,
            response_time=feedback.response_time,
            query_type=feedback.query_type
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return FeedbackResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando feedback: {str(e)}")

@router.get("/stats")
async def get_feedback_stats(days: int = Query(default=30, ge=1, le=365)):
    """Obtener estadísticas de feedback"""
    try:
        stats = feedback_service.get_feedback_stats(days)
        
        if "error" in stats:
            raise HTTPException(status_code=500, detail=stats["error"])
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

@router.get("/recent")
async def get_recent_feedback(
    limit: int = Query(default=10, ge=1, le=50),
    min_rating: Optional[int] = Query(default=None, ge=1, le=5)
):
    """Obtener feedback reciente"""
    try:
        feedback_list = feedback_service.get_recent_feedback(limit, min_rating)
        return {"feedback": feedback_list}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo feedback: {str(e)}")

@router.get("/improvement-report")
async def get_improvement_report(days: int = Query(default=30, ge=1, le=365)):
    """Obtener reporte de mejoras sugeridas"""
    try:
        report = feedback_service.generate_improvement_report(days)
        
        if "error" in report:
            raise HTTPException(status_code=500, detail=report["error"])
        
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")

@router.post("/export")
async def export_feedback_data(
    format: str = Query(default="json", regex="^(json|csv)$"),
    days: Optional[int] = Query(default=None, ge=1, le=365)
):
    """Exportar datos de feedback"""
    try:
        result = feedback_service.export_feedback_data(format, days)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exportando datos: {str(e)}")

@router.get("/categories")
async def get_feedback_categories():
    """Obtener categorías disponibles para feedback"""
    return {
        "categories": [
            "respuesta_incorrecta",
            "respuesta_incompleta", 
            "no_entiende_pregunta",
            "respuesta_muy_lenta",
            "formato_confuso",
            "falta_contexto",
            "error_tecnico",
            "sugerencia_mejora"
        ],
        "descriptions": {
            "respuesta_incorrecta": "La respuesta contiene información errónea",
            "respuesta_incompleta": "La respuesta no cubre todos los aspectos de la pregunta",
            "no_entiende_pregunta": "El sistema no comprendió la consulta correctamente",
            "respuesta_muy_lenta": "El tiempo de respuesta fue excesivo",
            "formato_confuso": "La respuesta está mal estructurada o es difícil de leer",
            "falta_contexto": "La respuesta necesita más contexto o explicación",
            "error_tecnico": "Error técnico en el sistema",
            "sugerencia_mejora": "Sugerencia para mejorar el sistema"
        }
    }

@router.get("/metrics/satisfaction")
async def get_satisfaction_metrics(days: int = Query(default=7, ge=1, le=365)):
    """Obtener métricas de satisfacción"""
    try:
        stats = feedback_service.get_feedback_stats(days)
        
        if "error" in stats:
            raise HTTPException(status_code=500, detail=stats["error"])
        
        # Extraer métricas específicas de satisfacción
        if "message" in stats:
            return {"message": stats["message"], "satisfaction_data": None}
        
        satisfaction_data = {
            "period_days": days,
            "average_rating": stats.get("average_rating", 0),
            "satisfaction_rate": stats.get("satisfaction_rate", 0),
            "total_responses": stats.get("total_feedback", 0),
            "rating_breakdown": stats.get("rating_distribution", {}),
            "trend": "stable"  # Sería calculado con datos históricos
        }
        
        # Determinar tendencia basada en rating promedio
        avg_rating = satisfaction_data["average_rating"]
        if avg_rating >= 4.0:
            satisfaction_data["status"] = "excellent"
        elif avg_rating >= 3.5:
            satisfaction_data["status"] = "good" 
        elif avg_rating >= 3.0:
            satisfaction_data["status"] = "fair"
        else:
            satisfaction_data["status"] = "needs_improvement"
        
        return {"satisfaction_data": satisfaction_data}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas: {str(e)}")

@router.get("/metrics/performance")
async def get_performance_metrics(days: int = Query(default=7, ge=1, le=365)):
    """Obtener métricas de rendimiento"""
    try:
        stats = feedback_service.get_feedback_stats(days)
        
        if "error" in stats:
            raise HTTPException(status_code=500, detail=stats["error"])
        
        if "message" in stats:
            return {"message": stats["message"], "performance_data": None}
        
        # Calcular métricas de rendimiento
        performance_data = {
            "period_days": days,
            "query_types": stats.get("query_types", {}),
            "problem_categories": stats.get("problem_categories", {}),
            "negative_feedback_rate": round(
                (stats.get("negative_feedback_count", 0) / max(stats.get("total_feedback", 1), 1)) * 100, 1
            ),
            "improvement_areas": []
        }
        
        # Identificar áreas de mejora
        problem_categories = performance_data["problem_categories"]
        total_feedback = stats.get("total_feedback", 1)
        
        for category, count in problem_categories.items():
            if count / total_feedback > 0.1:  # Más del 10% del feedback
                performance_data["improvement_areas"].append({
                    "category": category,
                    "frequency": count,
                    "percentage": round((count / total_feedback) * 100, 1)
                })
        
        return {"performance_data": performance_data}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas de rendimiento: {str(e)}")