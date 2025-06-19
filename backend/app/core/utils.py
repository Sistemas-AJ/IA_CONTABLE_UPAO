"""
Utilidades generales del sistema
"""
import re
import time
import logging
from typing import List, Dict, Any, Optional
from functools import wraps

# Logger para timing
timing_logger = logging.getLogger("timing")

def timing_decorator(func):
    """Decorador para medir tiempo de ejecución"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Logging más detallado
        timing_logger.info(f"⏱️ INICIO - {func.__name__}")
        
        try:
            result = await func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            
            # Log con más detalles
            timing_logger.info(f"✅ COMPLETADO - {func.__name__} ejecutado en {duration:.3f} segundos")
            
            # Agregar tiempo al resultado si es un dict
            if isinstance(result, dict):
                result["processing_time"] = duration
            
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            timing_logger.error(f"❌ ERROR - {func.__name__} falló después de {duration:.3f} segundos: {str(e)}")
            raise
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        timing_logger.info(f"⏱️ INICIO - {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            timing_logger.info(f"✅ COMPLETADO - {func.__name__} ejecutado en {duration:.3f} segundos")
            return result
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            timing_logger.error(f"❌ ERROR - {func.__name__} falló después de {duration:.3f} segundos: {str(e)}")
            raise
    
    if hasattr(func, '__code__') and func.__code__.co_flags & 0x80:  # CO_COROUTINE
        return async_wrapper
    else:
        return sync_wrapper

def format_currency(amount: float, currency: str = "S/") -> str:
    """Formatea montos como moneda"""
    return f"{currency} {amount:,.2f}"

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calcula variación porcentual"""
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100

def generate_table_markdown(data: List[Dict], headers: List[str]) -> str:
    """Genera tabla en formato Markdown"""
    if not data or not headers:
        return ""
    
    # Encabezados
    table = "| " + " | ".join(headers) + " |\n"
    table += "|" + "|".join(["--------"] * len(headers)) + "|\n"
    
    # Filas
    for row in data:
        row_data = []
        for header in headers:
            value = row.get(header, "")
            row_data.append(str(value))
        table += "| " + " | ".join(row_data) + " |\n"
    
    return table

def sanitize_filename(filename: str) -> str:
    """Sanitiza nombre de archivo"""
    # Remover caracteres peligrosos
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limitar longitud
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')
    return filename

def chunk_text(text: str, max_length: int = 1000, overlap: int = 100) -> List[str]:
    """Divide texto en chunks con superposición"""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + max_length
        
        # Buscar punto de corte natural (espacio, punto, etc.)
        if end < len(text):
            # Buscar hacia atrás hasta encontrar un separador
            for i in range(end, start, -1):
                if text[i] in [' ', '.', '!', '?', '\n']:
                    end = i + 1
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Calcular siguiente inicio con superposición
        start = max(end - overlap, start + 1)
    
    return chunks