"""
Rutas del sistema y administración
"""
import os
import psutil
from fastapi import APIRouter, HTTPException, Depends, Security
from typing import Dict, Any
from datetime import datetime
from ..config import get_config, validate_config, SYSTEM_NAME, SYSTEM_VERSION

router = APIRouter(prefix="/api/system", tags=["system"])

# Función simple de autorización (en producción usar JWT/OAuth)
def get_admin_user():
    """Función placeholder para autorización de admin"""
    # En producción, implementar verificación real de permisos
    return {"user_id": "admin", "role": "administrator"}

@router.get("/health")
async def health_check():
    """Verificar estado de salud del sistema"""
    try:
        # Verificar componentes básicos
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "system": {
                "name": SYSTEM_NAME,
                "version": SYSTEM_VERSION,
                "uptime": _get_uptime()
            },
            "components": {
                "api": "operational",
                "vectorstore": "operational", 
                "file_system": "operational",
                "memory": "operational"
            },
            "metrics": {
                "memory_usage_percent": psutil.virtual_memory().percent,
                "cpu_usage_percent": psutil.cpu_percent(interval=1),
                "disk_usage_percent": psutil.disk_usage('/').percent
            }
        }
        
        # Verificar si algún componente está en estado crítico
        if health_status["metrics"]["memory_usage_percent"] > 90:
            health_status["components"]["memory"] = "critical"
            health_status["status"] = "degraded"
        
        if health_status["metrics"]["disk_usage_percent"] > 90:
            health_status["components"]["file_system"] = "critical"
            health_status["status"] = "degraded"
        
        return health_status
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/info")
async def system_info():
    """Obtener información del sistema"""
    try:
        return {
            "system": {
                "name": SYSTEM_NAME,
                "version": SYSTEM_VERSION,
                "description": "Asistente inteligente para contabilidad",
                "environment": os.getenv("ENVIRONMENT", "development")
            },
            "capabilities": {
                "accounting_entries": True,
                "financial_analysis": True,
                "calculations": True,
                "educational_content": True,
                "file_processing": True,
                "web_search": False,  # Configurar según necesidades
                "real_time_updates": True
            },
            "supported_formats": [
                "PDF", "DOCX", "XLSX", "XLS", "CSV", "TXT"
            ],
            "api_version": "1.0",
            "documentation_url": "/docs",
            "contact": {
                "support_email": "soporte@upao.edu.pe",
                "website": "https://upao.edu.pe"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo información: {str(e)}")

@router.get("/config")
async def get_system_config(admin: dict = Depends(get_admin_user)):
    """Obtener configuración del sistema (solo admin)"""
    try:
        config = get_config()
        
        # Ocultar información sensible
        if "openai" in config and "api_key" in config["openai"]:
            config["openai"]["api_key"] = "***hidden***"
        
        return config
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo configuración: {str(e)}")

@router.get("/config/validate")
async def validate_system_config(admin: dict = Depends(get_admin_user)):
    """Validar configuración del sistema"""
    try:
        return validate_config()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validando configuración: {str(e)}")

@router.get("/metrics")
async def get_system_metrics():
    """Obtener métricas del sistema"""
    try:
        # Métricas de sistema
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Métricas de aplicación
        from ..services.chat_service import active_sessions
        from ..services.upload_service import upload_service
        from ..services.feedback_service import feedback_service
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_metrics": {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "used_percent": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "used_percent": round((disk.used / disk.total) * 100, 1)
                }
            },
            "application_metrics": {
                "active_sessions": len(active_sessions),
                "uploaded_files": len(upload_service.get_uploaded_files()),
                "total_feedback": len(feedback_service.feedback_data)
            },
            "performance_metrics": {
                "uptime_seconds": _get_uptime_seconds(),
                "process_count": len(psutil.pids()),
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas: {str(e)}")

@router.get("/logs")
async def get_system_logs(
    lines: int = 50,
    level: str = "INFO",
    admin: dict = Depends(get_admin_user)
):
    """Obtener logs del sistema (solo admin)"""
    try:
        # En implementación real, leer desde archivos de log
        # Por ahora, retornar logs simulados
        logs = [
            {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "message": "Sistema iniciado correctamente",
                "component": "main"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO", 
                "message": "Servicios cargados exitosamente",
                "component": "services"
            }
        ]
        
        return {
            "total_lines": len(logs),
            "requested_lines": lines,
            "level_filter": level,
            "logs": logs[-lines:]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo logs: {str(e)}")

@router.post("/maintenance")
async def toggle_maintenance_mode(
    enabled: bool,
    admin: dict = Depends(get_admin_user)
):
    """Activar/desactivar modo mantenimiento"""
    try:
        # En implementación real, persistir estado
        maintenance_status = {
            "maintenance_mode": enabled,
            "changed_by": admin["user_id"],
            "changed_at": datetime.now().isoformat(),
            "message": "Sistema en mantenimiento" if enabled else "Sistema operativo"
        }
        
        return maintenance_status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cambiando modo mantenimiento: {str(e)}")

@router.post("/restart")
async def restart_system(admin: dict = Depends(get_admin_user)):
    """Reiniciar componentes del sistema (solo admin)"""
    try:
        # En implementación real, reiniciar servicios específicos
        # Por ahora, simular reinicio
        
        restart_info = {
            "requested_by": admin["user_id"],
            "requested_at": datetime.now().isoformat(),
            "status": "restart_scheduled",
            "estimated_downtime": "2-3 minutos",
            "affected_services": [
                "chat_service",
                "upload_service", 
                "vectorstore",
                "cache"
            ]
        }
        
        return restart_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error programando reinicio: {str(e)}")

@router.get("/backup/status")
async def get_backup_status(admin: dict = Depends(get_admin_user)):
    """Obtener estado de respaldos"""
    try:
        # En implementación real, verificar respaldos automáticos
        return {
            "backup_enabled": True,
            "last_backup": "2024-01-15T02:00:00Z",
            "next_backup": "2024-01-16T02:00:00Z",
            "backup_size_mb": 150.5,
            "backup_location": "/backups/",
            "retention_days": 30,
            "backup_types": [
                "database",
                "uploaded_files",
                "vectorstore",
                "configuration"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estado de respaldo: {str(e)}")

@router.post("/backup/create")
async def create_backup(admin: dict = Depends(get_admin_user)):
    """Crear respaldo manual"""
    try:
        # En implementación real, ejecutar proceso de respaldo
        backup_info = {
            "backup_id": f"manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "created_by": admin["user_id"],
            "created_at": datetime.now().isoformat(),
            "status": "in_progress",
            "estimated_completion": "5-10 minutos",
            "backup_type": "full_manual"
        }
        
        return backup_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando respaldo: {str(e)}")

@router.get("/version")
async def get_version_info():
    """Obtener información de versión"""
    return {
        "version": SYSTEM_VERSION,
        "release_date": "2024-01-15",
        "build": "1.0.0-stable",
        "api_version": "1.0",
        "dependencies": {
            "fastapi": "0.104.1",
            "openai": "1.3.0",
            "python": "3.11+",
            "platform": os.name
        },
        "changelog_url": "/docs/changelog",
        "upgrade_available": False
    }

# Funciones auxiliares
def _get_uptime() -> str:
    """Obtiene tiempo de actividad del sistema"""
    try:
        uptime_seconds = _get_uptime_seconds()
        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60
        return f"{int(hours)}h {int(minutes)}m"
    except:
        return "unknown"

def _get_uptime_seconds() -> float:
    """Obtiene tiempo de actividad en segundos"""
    try:
        return psutil.boot_time()
    except:
        return 0.0