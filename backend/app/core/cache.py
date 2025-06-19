"""
Sistema de cache para optimizar embeddings y consultas frecuentes
"""
import time
from typing import Dict, List, Optional, Any
from collections import OrderedDict

class EmbeddingCache:
    """Cache LRU para embeddings con expiración temporal"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, float] = {}
    
    def _generate_key(self, text: str) -> str:
        """Genera clave única para el texto"""
        return f"emb_{hash(text[:200])}"
    
    def _is_expired(self, key: str) -> bool:
        """Verifica si una entrada ha expirado"""
        if key not in self.timestamps:
            return True
        return time.time() - self.timestamps[key] > self.ttl_seconds
    
    def _cleanup_expired(self):
        """Limpia entradas expiradas"""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self.timestamps.items()
            if current_time - timestamp > self.ttl_seconds
        ]
        for key in expired_keys:
            self.cache.pop(key, None)
            self.timestamps.pop(key, None)
    
    def get(self, text: str) -> Optional[List[float]]:
        """Obtiene embedding del cache"""
        key = self._generate_key(text)
        
        if key in self.cache and not self._is_expired(key):
            # Mover al final (LRU)
            self.cache.move_to_end(key)
            return self.cache[key]
        
        return None
    
    def set(self, text: str, embedding: List[float]):
        """Guarda embedding en el cache"""
        key = self._generate_key(text)
        
        # Limpiar expirados ocasionalmente
        if len(self.cache) % 100 == 0:
            self._cleanup_expired()
        
        # Aplicar límite de tamaño
        while len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            self.cache.pop(oldest_key)
            self.timestamps.pop(oldest_key, None)
        
        self.cache[key] = embedding
        self.timestamps[key] = time.time()
    
    def clear(self):
        """Limpia todo el cache"""
        self.cache.clear()
        self.timestamps.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Estadísticas del cache"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl_seconds": self.ttl_seconds,
            "hit_ratio": getattr(self, '_hit_count', 0) / max(getattr(self, '_total_requests', 1), 1)
        }

class QueryCache:
    """Cache para consultas frecuentes y respuestas similares"""
    
    def __init__(self, max_size: int = 500, ttl_seconds: int = 1800):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, float] = {}
    
    def _generate_key(self, query: str, context_hash: str = "") -> str:
        """Genera clave única para la consulta"""
        return f"query_{hash(query.lower()[:100] + context_hash)}"
    
    def get(self, query: str, context_hash: str = "") -> Optional[str]:
        """Obtiene respuesta del cache"""
        key = self._generate_key(query, context_hash)
        
        if key in self.cache:
            if time.time() - self.timestamps[key] <= self.ttl_seconds:
                self.cache.move_to_end(key)
                return self.cache[key]
            else:
                # Remover entrada expirada
                self.cache.pop(key)
                self.timestamps.pop(key)
        
        return None
    
    def set(self, query: str, response: str, context_hash: str = ""):
        """Guarda respuesta en el cache"""
        key = self._generate_key(query, context_hash)
        
        # Aplicar límite de tamaño
        while len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            self.cache.pop(oldest_key)
            self.timestamps.pop(oldest_key, None)
        
        self.cache[key] = response
        self.timestamps[key] = time.time()

# Instancias globales
embedding_cache = EmbeddingCache()
query_cache = QueryCache()

def get_cached_embedding(text: str, embedding_function) -> List[float]:
    """Función helper para obtener embeddings con cache"""
    # Intentar obtener del cache
    cached = embedding_cache.get(text)
    if cached:
        return cached
    
    # Generar nuevo embedding
    embedding = embedding_function(text)
    
    # Guardar en cache
    embedding_cache.set(text, embedding)
    
    return embedding