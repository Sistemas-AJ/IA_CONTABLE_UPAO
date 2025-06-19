"""
Rutas para manejo de archivos
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List, Optional
from pydantic import BaseModel
from ..services.upload_service import upload_service
from ..core.utils import timing_decorator

router = APIRouter(prefix="/api/upload", tags=["upload"])

# Modelos de respuesta
class FileInfo(BaseModel):
    id: str
    name: str
    size: int
    type: str
    upload_time: str
    status: str
    chunks_created: int

class UploadResponse(BaseModel):
    success: bool
    message: str
    file_info: Optional[dict] = None
    processing_stats: Optional[dict] = None
    is_duplicate: bool = False

@router.post("/file", response_model=UploadResponse)
@timing_decorator
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Form(default="anonymous")
):
    """Subir un archivo para procesamiento"""
    try:
        # Validaciones iniciales
        if not file.filename:
            raise HTTPException(status_code=400, detail="No se proporcionó nombre de archivo")
        
        # Leer contenido del archivo
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="El archivo está vacío")
        
        # Procesar archivo
        result = await upload_service.process_file_upload(
            file_content=file_content,
            filename=file.filename,
            user_id=user_id
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return UploadResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando archivo: {str(e)}")

@router.get("/files", response_model=List[FileInfo])
async def get_uploaded_files(user_id: Optional[str] = None):
    """Obtener lista de archivos subidos"""
    try:
        files = upload_service.get_uploaded_files(user_id)
        return [FileInfo(**file_data) for file_data in files]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo archivos: {str(e)}")

@router.delete("/files/{file_hash}")
async def delete_file(file_hash: str, user_id: Optional[str] = None):
    """Eliminar un archivo subido"""
    try:
        result = upload_service.delete_file(file_hash, user_id)
        
        if not result["success"]:
            if "no encontrado" in result["error"].lower():
                raise HTTPException(status_code=404, detail=result["error"])
            elif "permisos" in result["error"].lower():
                raise HTTPException(status_code=403, detail=result["error"])
            else:
                raise HTTPException(status_code=400, detail=result["error"])
        
        return {"message": result["message"]}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando archivo: {str(e)}")

@router.get("/stats")
async def get_upload_stats():
    """Obtener estadísticas de archivos subidos"""
    try:
        stats = upload_service.get_file_stats()
        
        if "error" in stats:
            raise HTTPException(status_code=500, detail=stats["error"])
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

@router.get("/supported-formats")
async def get_supported_formats():
    """Obtener formatos de archivo soportados"""
    return {
        "supported_extensions": [".pdf", ".docx", ".xlsx", ".xls", ".csv", ".txt"],
        "max_file_size_mb": 50,
        "descriptions": {
            ".pdf": "Documentos PDF - Se extrae el texto completo",
            ".docx": "Documentos Word - Se extrae texto y tablas",
            ".xlsx": "Hojas de cálculo Excel - Se procesan todas las hojas",
            ".xls": "Hojas de cálculo Excel (formato antiguo)",
            ".csv": "Archivos CSV - Datos tabulares",
            ".txt": "Archivos de texto plano"
        },
        "processing_info": {
            "text_extraction": "Se extrae y vectoriza el contenido para búsqueda",
            "chunking": "Los documentos se dividen en fragmentos de 1000 caracteres",
            "indexing": "Se crean embeddings para búsqueda semántica",
            "retention": "Los archivos se almacenan localmente para referencia"
        }
    }

@router.post("/batch")
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    user_id: str = Form(default="anonymous")
):
    """Subir múltiples archivos"""
    try:
        if len(files) > 10:
            raise HTTPException(status_code=400, detail="Máximo 10 archivos por lote")
        
        results = []
        
        for file in files:
            try:
                if not file.filename:
                    results.append({
                        "filename": "unknown",
                        "success": False,
                        "error": "Nombre de archivo no válido"
                    })
                    continue
                
                file_content = await file.read()
                
                result = await upload_service.process_file_upload(
                    file_content=file_content,
                    filename=file.filename,
                    user_id=user_id
                )
                
                results.append({
                    "filename": file.filename,
                    **result
                })
                
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": str(e)
                })
        
        # Estadísticas del lote
        successful = len([r for r in results if r["success"]])
        failed = len(results) - successful
        
        return {
            "batch_summary": {
                "total_files": len(results),
                "successful": successful,
                "failed": failed,
                "success_rate": round((successful / len(results)) * 100, 1) if results else 0
            },
            "results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando lote: {str(e)}")

@router.get("/files/{file_hash}/info")
async def get_file_info(file_hash: str):
    """Obtener información detallada de un archivo"""
    try:
        files = upload_service.get_uploaded_files()
        file_info = next((f for f in files if f["id"] == file_hash), None)
        
        if not file_info:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        
        return file_info
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo información: {str(e)}")

@router.post("/validate")
async def validate_file(file: UploadFile = File(...)):
    """Validar un archivo antes de subirlo"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No se proporcionó nombre de archivo")
        
        # Leer solo una pequeña parte para validación
        file_content = await file.read(1024)  # Primeros 1KB
        await file.seek(0)  # Resetear posición
        
        # Validar extensión
        from pathlib import Path
        file_ext = Path(file.filename).suffix.lower()
        supported_extensions = {'.pdf', '.docx', '.xlsx', '.xls', '.csv', '.txt'}
        
        if file_ext not in supported_extensions:
            return {
                "valid": False,
                "error": f"Extensión no soportada: {file_ext}",
                "supported_extensions": list(supported_extensions)
            }
        
        # Validar tamaño (obtener tamaño completo)
        content_length = 0
        chunk_size = 8192
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            content_length += len(chunk)
        
        max_size = 50 * 1024 * 1024  # 50MB
        if content_length > max_size:
            return {
                "valid": False,
                "error": f"Archivo muy grande: {content_length / 1024 / 1024:.1f}MB (máximo: 50MB)"
            }
        
        return {
            "valid": True,
            "file_info": {
                "name": file.filename,
                "size_bytes": content_length,
                "size_mb": round(content_length / 1024 / 1024, 2),
                "extension": file_ext,
                "content_type": file.content_type
            }
        }
        
    except Exception as e:
        return {
            "valid": False,
            "error": f"Error validando archivo: {str(e)}"
        }