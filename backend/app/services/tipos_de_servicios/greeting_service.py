"""
Servicio para manejo de saludos y conversación general
"""
import random
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class GreetingService:
    """Servicio especializado en saludos y conversación general"""
    
    async def generate_response(self, query: str, context: Dict, metadata: Dict) -> str:
        """Genera respuesta de saludo o conversación general"""
        query_lower = query.lower().strip()
        
        # 🔧 MEJORAR DETECCIÓN DE DESPEDIDAS - Más específico
        despedidas = [
            "adiós", "adios", "hasta luego", "nos vemos", "chau", "chao", 
            "hasta pronto", "cuídate", "cuídate mucho", "hasta la próxima", 
            "hasta la vista", "bye", "goodbye", "take care", "me voy", 
            "hasta mañana", "buenas noches"
        ]
        
        # ✅ DETECTAR DESPEDIDAS EXACTAS
        if query_lower in despedidas or any(despedida in query_lower for despedida in despedidas):
            return self._generate_farewell_response()
        
        # Detectar saludos casuales
        elif any(greeting in query_lower for greeting in ["como estas", "cómo estas", "como está", "cómo está", "que tal", "qué tal"]):
            return self._generate_casual_response()
        
        # Detectar saludos formales
        elif any(greeting in query_lower for greeting in ["hola", "hello", "hi", "buenos días", "buenas tardes", "saludos", "buen día"]):
            return self._generate_greeting()
        
        # Por defecto, conversación general
        else:
            return self._generate_general_conversation()
    
    def _generate_farewell_response(self) -> str:
        """Genera respuesta de despedida"""
        farewell_responses = [
            "¡Hasta luego! 👋 Fue un gusto ayudarte con tus consultas contables.",
            "¡Nos vemos pronto! 😊 Recuerda que siempre estaré aquí para tus dudas contables.",
            "¡Adiós! 🌟 Que tengas un excelente día y éxito en tus labores contables.",
            "¡Hasta la próxima! 💼 Espero haberte ayudado con tus temas contables.",
            "¡Cuídate mucho! 😄 Vuelve cuando necesites ayuda con contabilidad.",
            "¡Chau! 👍 Ha sido genial resolver tus consultas contables contigo.",
            "¡Hasta pronto! 📊 Que tengas mucho éxito en tus actividades contables.",
            "¡Bye! 🎯 Siempre a tu disposición para cualquier tema contable.",
            "¡Nos vemos! 💡 Recuerda aplicar lo que hemos conversado en contabilidad.",
            "¡Hasta luego! 🚀 Que tengas un día productivo y lleno de logros contables."
        ]
        
        return random.choice(farewell_responses)
    
    def _generate_casual_response(self) -> str:
        """Genera respuesta casual para preguntas como 'como estas'"""
        casual_responses = [
            "¡Todo bien! 😊 Aquí andamos ayudando con temas contables. ¿En qué puedo ayudarte hoy?",
            "¡Excelente! 👍 Listo para resolver cualquier consulta contable que tengas.",
            "¡Muy bien, gracias! 😄 ¿Tienes alguna pregunta sobre contabilidad?",
            "¡De maravilla! 🌟 ¿Qué tema contable te interesa?",
            "¡Todo perfecto! 💯 ¿En qué aspecto contable necesitas ayuda?"
        ]
        
        return random.choice(casual_responses)
    
    def _generate_greeting(self) -> str:
        """Genera saludo personalizado completo"""
        greetings = [
            "¡Hola! 👋 Soy tu **Asistente Contable UPAO**.",
            "¡Buenos días! 🌅 Bienvenido al **Sistema Contable UPAO**.",
            "¡Hola! 😊 ¿En qué puedo ayudarte hoy?"
        ]
        
        greeting = random.choice(greetings)
        
        return f"""{greeting}

## **📊 Mis especialidades contables:**

### **🎯 Asientos Contables**
- Préstamos bancarios y financiamiento
- Compras y ventas con IGV
- Operaciones con personal (planillas, CTS)
- Depreciación de activos fijos

### **📈 Análisis Financiero**
- **Ratios de Liquidez:** Current Ratio, Quick Ratio
- **Ratios de Rentabilidad:** ROA, ROE, Márgenes
- **Ratios de Actividad:** Rotación de inventarios/cuentas
- **Ratios de Endeudamiento:** Debt Ratio, Leverage

### **📋 Estados Financieros**
- Análisis vertical y horizontal
- Tendencias y variaciones
- Interpretación de resultados
- Identificación de fortalezas/debilidades

### **🧮 Cálculos Especializados**
- **Laborales:** CTS, vacaciones, gratificaciones
- **Tributarios:** IGV, Impuesto a la Renta
- **Financieros:** Intereses, valor presente, préstamos
- **Depreciación:** Línea recta, saldos decrecientes

## **💡 Ejemplos rápidos:**

**Para asientos:** *"Registra un préstamo de S/ 50,000"*  
**Para ratios:** *"Calcula ROE con utilidad S/ 15,000 y patrimonio S/ 100,000"*  
**Para análisis:** *"Analiza mi balance general vs año anterior"*  
**Para cálculos:** *"Calcula CTS de trabajador que gana S/ 3,000"*  

**¿En qué tema contable te puedo ayudar?** 🤔"""

    def _generate_general_conversation(self) -> str:
        """Genera respuesta para conversación general"""
        return """## **🤖 Asistente Contable UPAO**

Soy un especialista en contabilidad diseñado para ayudarte con:

### **📚 Mis capacidades principales:**

**🎯 Contabilidad Práctica:**
- Asientos contables del PCGE 2019
- Registro de operaciones comerciales
- Cálculos laborales y tributarios

**📊 Análisis Financiero:**
- Ratios de liquidez, rentabilidad y endeudamiento
- Análisis de estados financieros
- Interpretación de indicadores

**🧮 Cálculos Especializados:**
- CTS, vacaciones, gratificaciones
- Depreciación de activos fijos
- IGV e Impuesto a la Renta

**🎓 Educación Contable:**
- Explicación de conceptos
- Diferencias entre términos contables
- Ejemplos prácticos y casos

### **💬 Formas de consultarme:**

- **Directa:** *"Calcula el IGV de S/ 1,000"*
- **Educativa:** *"¿Qué es el ROE?"*
- **Práctica:** *"Asiento contable de compra a crédito"*
- **Analítica:** *"Interpreta un ratio de liquidez de 1.8"*

**¿Qué tema contable específico te interesa?**"""

# Instancia global
greeting_service = GreetingService()