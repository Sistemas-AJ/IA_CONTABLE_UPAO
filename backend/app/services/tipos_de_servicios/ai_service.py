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
            
            # Asegurar que local_documents es string antes de hacer slice
            local_docs = context.get("local_documents")
            if local_docs is not None:
                if not isinstance(local_docs, str):
                    local_docs = str(local_docs)
                messages.insert(1, {
                    "role": "system",
                    "content": f"Contexto relevante de documentos entrenados:\n{local_docs[:2000]}"
                })

            if context.get("user_data"):
                user_ctx = "\n".join(f"{k}: {v}" for k, v in context["user_data"].items())
                messages.insert(1, {
                    "role": "system",
                    "content": f"Contexto del usuario para esta sesión:\n{user_ctx}"
                })
            
            if context.get("history"):
                history_text = "\n".join(
                    f"{msg['role']}: {msg['content']}" for msg in context["history"]
                )
                messages.insert(1, {
                    "role": "system",
                    "content": f"Historial reciente de la conversación:\n{history_text}"
                })

            response = openai.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.2,
                max_tokens=3000
            )
            
            # DEBUG: Asegurarse de que el contenido es string
            content = response.choices[0].message.content
            logger.info(f"Respuesta OpenAI content type: {type(content)} | value: {content}")
            if not isinstance(content, str):
                content = str(content)
            return content
            
        except Exception as e:
            logger.error(f"❌ Error en IA: {str(e)}")
            return self.generate_error_response(str(e))
    
    def _get_system_prompt(self, query_type: str) -> str:
        """Sistema prompt según tipo de consulta"""
        prompts = {
            "calculos_contables": """Eres un contador experto en cálculos contables peruanos. 
Resuelve el cálculo mostrando fórmulas, pasos y resultado final con formato Markdown.""",
            
            "asiento_contable": """Eres un contador certificado en Perú. 
Genera asientos contables con códigos PCGE 2019, tablas formateadas y explicaciones.""",
            
            "ratios_financieros": """Eres un analista financiero experto. 
Explica ratios con fórmulas, interpretación y valores de referencia.""",
            
            "ai": "Eres un asistente inteligente capaz de responder cualquier tipo de pregunta, no solo contabilidad. Responde de forma clara, útil y profesional.",
            "general": "Eres un asistente inteligente capaz de responder cualquier tipo de pregunta, no solo contabilidad. Responde de forma clara, útil y profesional."
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