"""
Servicio de IA para respuestas avanzadas usando OpenAI
"""
import openai
import logging
from typing import Dict
from ...config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)

class AIService:
    """Servicio de IA para respuestas complejas"""
    
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
    
    async def generate_ai_response(self, query: str, query_type: str, context: Dict) -> str:
        """Genera respuesta usando OpenAI"""
        try:
            if OPENAI_API_KEY == "dummy-key":
                return self._generate_fallback_response(query, query_type)
            
            system_prompt = self._get_system_prompt(query_type)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
            
            if context.get("local_documents"):
                messages.insert(1, {
                    "role": "system", 
                    "content": f"Contexto relevante: {context['local_documents'][:2000]}"
                })
            
            response = openai.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.2,
                max_tokens=3000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"❌ Error en IA: {str(e)}")
            return self._generate_error_response()
    
    def _get_system_prompt(self, query_type: str) -> str:
        """Sistema prompt según tipo de consulta"""
        prompts = {
            "calculos_contables": """Eres un contador experto en cálculos contables peruanos. 
Resuelve el cálculo mostrando fórmulas, pasos y resultado final con formato Markdown.""",
            
            "asiento_contable": """Eres un contador certificado en Perú. 
Genera asientos contables con códigos PCGE 2019, tablas formateadas y explicaciones.""",
            
            "ratios_financieros": """Eres un analista financiero experto. 
Explica ratios con fórmulas, interpretación y valores de referencia.""",
            
            "general": """Eres un asistente contable especializado en contabilidad peruana. 
Responde con precisión usando normativa local y formato Markdown."""
        }
        
        return prompts.get(query_type, prompts["general"])
    
    def _generate_fallback_response(self, query: str, query_type: str) -> str:
        """Respuesta cuando no hay API key válida"""
        return f"""## **⚠️**

Tu consulta: *"{query}"*

**Manejo de ERRORES.**"""
    
    def generate_error_response(self, error: str = None) -> Dict:
        """Genera respuesta de error"""
        return {
            "response": f"""## **❌ Error**

Ocurrió un problema: {error or "Error inesperado"}

**Por favor:**
- Verifica tu consulta
- Intenta de nuevo
- Contacta soporte si persiste""",
            "query_type": "error",
            "confidence": 0.0,
            "metadata": {"error": error},
            "processing_time": 0.0
        }

# Instancia global
ai_service = AIService()