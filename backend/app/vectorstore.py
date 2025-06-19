"""
Sistema de vectorstore usando FAISS para búsqueda semántica
"""
import os
import json
import faiss
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Any
import openai
from .config import VECTOR_INDEX_PATH, EMBED_DIM, VECTORSTORE_METADATA_PATH, OPENAI_API_KEY, EMBEDDING_MODEL

# Configurar OpenAI
openai.api_key = OPENAI_API_KEY

class VectorStore:
    """Clase para manejo del vectorstore FAISS"""
    
    def __init__(self):
        self.index_path = Path(VECTOR_INDEX_PATH)
        self.metadata_path = Path(VECTORSTORE_METADATA_PATH)
        self.embed_dim = EMBED_DIM
        self.index = None
        self.metadata = []
        
        # Crear directorio si no existe
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Cargar índice existente o crear nuevo
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """Carga índice existente o crea uno nuevo"""
        try:
            if self.index_path.with_suffix('.index').exists():
                # Cargar índice existente
                self.index = faiss.read_index(str(self.index_path.with_suffix('.index')))
                
                # Cargar metadata
                if self.metadata_path.exists():
                    with open(self.metadata_path, 'r', encoding='utf-8') as f:
                        self.metadata = json.load(f)
                
                print(f"✅ Vectorstore cargado: {self.index.ntotal} documentos")
            else:
                # Crear nuevo índice
                self.index = faiss.IndexFlatIP(self.embed_dim)  # Inner Product para cosine similarity
                self.metadata = []
                print("🆕 Nuevo vectorstore creado")
                
        except Exception as e:
            print(f"❌ Error cargando vectorstore: {e}")
            # Crear nuevo índice en caso de error
            self.index = faiss.IndexFlatIP(self.embed_dim)
            self.metadata = []
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """Obtiene embedding de OpenAI para un texto"""
        try:
            response = openai.embeddings.create(
                model=EMBEDDING_MODEL,
                input=text
            )
            embedding = np.array(response.data[0].embedding, dtype=np.float32)
            
            # Normalizar para cosine similarity
            embedding = embedding / np.linalg.norm(embedding)
            
            return embedding
            
        except Exception as e:
            print(f"❌ Error obteniendo embedding: {e}")
            raise
    
    def agregar_documento(self, texto: str, metadata: Dict = None) -> int:
        """Agrega un documento al vectorstore"""
        try:
            # Obtener embedding
            embedding = self._get_embedding(texto)
            
            # Agregar al índice
            self.index.add(embedding.reshape(1, -1))
            
            # Agregar metadata
            doc_metadata = {
                "texto": texto,
                "id": len(self.metadata),
                **(metadata or {})
            }
            self.metadata.append(doc_metadata)
            
            # Guardar cambios
            self._save_index()
            
            return doc_metadata["id"]
            
        except Exception as e:
            print(f"❌ Error agregando documento: {e}")
            raise
    
    def buscar_documentos(self, query: str, top_k: int = 5) -> List[Dict]:
        """Busca documentos similares a la consulta"""
        try:
            if self.index.ntotal == 0:
                return []
            
            # Obtener embedding de la consulta
            query_embedding = self._get_embedding(query)
            
            # Buscar en el índice
            scores, indices = self.index.search(query_embedding.reshape(1, -1), top_k)
            
            # Preparar resultados
            resultados = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx != -1 and idx < len(self.metadata):  # Verificar índice válido
                    resultado = {
                        **self.metadata[idx],
                        "score": float(score),
                        "rank": i + 1
                    }
                    resultados.append(resultado)
            
            return resultados
            
        except Exception as e:
            print(f"❌ Error buscando documentos: {e}")
            return []
    
    def _save_index(self):
        """Guarda el índice y metadata en disco"""
        try:
            # Guardar índice FAISS
            faiss.write_index(self.index, str(self.index_path.with_suffix('.index')))
            
            # Guardar metadata
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Error guardando índice: {e}")
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del vectorstore"""
        return {
            "total_documents": self.index.ntotal if self.index else 0,
            "embedding_dimension": self.embed_dim,
            "index_type": type(self.index).__name__ if self.index else "None",
            "metadata_count": len(self.metadata)
        }

# Instancia global del vectorstore
_vectorstore = None

def get_vectorstore() -> VectorStore:
    """Obtiene la instancia global del vectorstore"""
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = VectorStore()
    return _vectorstore

# Funciones de compatibilidad con el código existente
async def initialize_vectorstore():
    """Inicializa el vectorstore"""
    get_vectorstore()
    print("✅ Vectorstore inicializado")

async def agregar_documento(texto: str, metadata: Dict = None) -> int:
    """Agrega un documento al vectorstore"""
    vectorstore = get_vectorstore()
    return vectorstore.agregar_documento(texto, metadata)

def obtener_chunks(query: str, top_k: int = 5) -> List[Dict]:
    """Busca chunks relevantes para una consulta"""
    vectorstore = get_vectorstore()
    return vectorstore.buscar_documentos(query, top_k)

def get_vectorstore_stats() -> Dict:
    """Obtiene estadísticas del vectorstore"""
    vectorstore = get_vectorstore()
    return vectorstore.get_stats()