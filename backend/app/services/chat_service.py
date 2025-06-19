"""
Servicio principal del chatbot contable - Coordinador
"""
import logging
from typing import Dict
from ..analyzers.query_detector import query_detector
from ..core.utils import timing_decorator
from .tipos_de_servicios.greeting_service import greeting_service
from .tipos_de_servicios.calculation_service import calculation_service
from .tipos_de_servicios.financial_service import financial_service
from .tipos_de_servicios.educational_service import educational_service
from .tipos_de_servicios.ai_service import ai_service
from .business_service import business_service
from .regulatory_service import regulatory_service
from ..vectorstore import obtener_chunks
from .tipos_de_servicios.asientos_contables import asientos_contables

logger = logging.getLogger(__name__)

class ChatService:
    """Servicio coordinador principal para manejo de conversaciones"""
    
    def __init__(self):
        self.service_map = {
            "saludo": greeting_service,
            "despedida": greeting_service,
            "conversacion_general": greeting_service,
            "ratios_financieros": financial_service,
            "analisis_estados_financieros": financial_service,
            "calculos_contables": calculation_service,
            "educativo": educational_service,
            "constitucion": business_service,
            "normativa": regulatory_service,
            "general": educational_service,
            "asiento_contable": asientos_contables
        }
    
    @timing_decorator
    async def process_query(self, query: str, session_id: str, user_context: Dict = None) -> Dict:
        """Procesa una consulta del usuario"""
        try:

            logger.info(f"🔍 Consulta recibida | Session: {session_id} | Mensaje: {query}")
            
            # Detectar tipo de consulta
            query_type, confidence, metadata = query_detector.detect_query_type(query)
            service = self.service_map.get(query_type, educational_service)  # <-- Mover aquí
            
            # Ahora sí puedes loguear:
            logger.info(f"✅ Tipo detectado: {query_type} | Confianza: {confidence:.2f} | Servicio: {service.__class__.__name__}")
            
            # Recopilar contexto
            context = await self._gather_context(query, user_context)
            
            # Obtener servicio especializado
            service = self.service_map.get(query_type, educational_service)
            
            try:
                # Intentar con servicio especializado
                response = await service.generate_response(query, context, metadata)
                
                # 🆕 NUEVO: Si el servicio educativo retorna None, usar IA directamente
                if response is None:
                    logger.info(f"🤖 Servicio retornó None - Usando IA para: '{query}'")
                    response = await ai_service.generate_ai_response(query, query_type, context)
                
                # Si respuesta incompleta, usar IA como fallback
                elif self._is_incomplete_response(response):
                    logger.warning(f"⚠️ Respuesta incompleta, usando IA como fallback")
                    response = await ai_service.generate_ai_response(query, query_type, context)
                    
            except Exception as e:
                logger.error(f"❌ Error en servicio {query_type}: {str(e)}")
                response = await ai_service.generate_ai_response(query, query_type, context)
            
            return {
                "response": response,
                "query_type": query_type,
                "confidence": confidence,
                "metadata": metadata,
                "processing_time": 0.0
            }
            
        except Exception as e:
            logger.error(f"❌ Error procesando consulta: {str(e)}", exc_info=True)
            return ai_service.generate_error_response(str(e))

    async def _gather_context(self, query: str, user_context: Dict = None) -> Dict:
        """Recopila contexto relevante para la consulta"""
        context = {
            "local_documents": "",
            "user_data": user_context or {},
            "extracted_entities": {}
        }
        
        try:
            chunks = obtener_chunks(query, top_k=3)
            if chunks:
                context["local_documents"] = "\n\n".join([chunk["texto"] for chunk in chunks])
        except Exception as e:
            logger.error(f"❌ Error recopilando contexto: {e}")
        
        return context
    
    def _is_incomplete_response(self, response: str) -> bool:
        """Verifica si la respuesta está incompleta"""
        return (response is None or 
                len(response.strip()) < 50 or 
                "en desarrollo" in response.lower())

# Instancia global
chat_service = ChatService()