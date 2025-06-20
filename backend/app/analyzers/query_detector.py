"""
Detector de tipos de consulta mejorado y modularizado
"""
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class QueryPattern:
    """Patrón de consulta con metadatos"""
    keywords: List[str]
    strong_indicators: List[str]
    category: str
    priority: int
    min_keyword_count: int = 1

class QueryDetector:
    """Detector inteligente de tipos de consulta contable"""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, QueryPattern]:
        """Inicializa patrones de detección"""
        return {
            "saludo": QueryPattern(
                keywords=["hola", "hello", "hi", "buenos días", "buenas tardes", "buenas noches", 
                        "saludos", "que tal", "qué tal", "como estas", "cómo estás", "como está", "cómo está",
                        "buen día", "buena tarde", "buena noche", "hey", "oye", "como andas", "cómo andas"],
                strong_indicators=["hola", "hello", "hi", "buenos días", "buenas tardes", "como estas", "cómo estás"],
                category="conversational",
                priority=10
            ),
            "despedida": QueryPattern(
            keywords=["adiós", "adios", "hasta luego", "nos vemos", "chau", "chao", "hasta pronto",
             "cuídate", "cuídate mucho", "hasta la próxima", "hasta la vista", "bye", "take care",
             "me voy", "hasta mañana", "buenas noches", "goodbye"],
            strong_indicators=["adiós", "adios", "hasta luego", "chau", "chao", "hasta pronto", "bye"],
            category="conversational",  
            priority=10  
            ),      
            "conversacion_general": QueryPattern(
                keywords=["como funciona", "que puedes hacer", "qué puedes hacer", "ayuda", "help",
                         "quien eres", "quién eres", "que eres", "qué eres", "para que sirves",
                         "como te llamas", "cómo te llamas", "cual es tu nombre", "cuál es tu nombre"],
                strong_indicators=["que puedes hacer", "quien eres", "ayuda", "como funciona"],
                category="conversational",
                priority=9
            ),
            
            "educativo": QueryPattern(
                keywords=[
                    "qué es", "que es", "explicar", "explica", "definir", "define", 
                    "diferencia entre", "tipos de", "características", "definición", 
                    "concepto", "principio contable", "norma contable", "ejemplo de",
                    "que significa", "qué significa", "significado de"
                ],
                strong_indicators=[
                    "qué es", "que es", "explicar", "definir", "ejemplo de", "definición de", "que significa", "qué significa"
                ],
                category="educational",
                priority=11,  # Más alta prioridad para preguntas educativas
                min_keyword_count=1
            ),
            
            "asiento_contable": QueryPattern(
                keywords=[
                    "asiento", "contabilizar", "registrar", "préstamo", "prestamo", "debe", "haber",
                    "cuenta", "pcge", "contable", "registro", "cuota", "pago", "interés", "financiero",
                    "libro diario", "partida doble", "débito", "crédito",
                    "ingreso de mercadería", "ingreso de mercaderías", "ingreso de inventario", "entrada de mercadería", "entrada de mercaderías",
                    "compra", "venta", "factura", "nota de crédito", "nota de débito", "recibo", "boleta",
                    "gasto", "ingreso", "servicio", "servicios", "honorario", "honorarios", "proveedor", "cliente",
                    "banco", "transferencia", "depósito", "retiro", "cheque", "letra", "pagaré", "pagare",
                    "activo fijo", "depreciación", "provisión", "provisiones", "amortización", "capital", "aporte", "retiro de socios",
                    "planilla", "remuneración", "sueldo", "salario", "cts", "gratificación", "vacaciones", "essalud", "afp", "onp",
                    "impuesto", "igv", "renta", "detracción", "percepción", "retención", "tributo", "sunat",
                    "dividendos", "utilidad", "pérdida", "resultado", "ajuste", "reclasificación", "saldo inicial", "saldo final"
                ],
                strong_indicators=[
                    "asiento contable", "préstamo", "registra", "debe y haber", "cuota",
                    "ingreso de mercadería", "ingreso de mercaderías", "asiento de compra", "asiento de venta",
                    "asiento de pago", "asiento de cobro", "asiento de honorarios", "asiento de servicios",
                    "asiento de depreciación", "asiento de provisión", "asiento de planilla", "asiento de impuesto",
                    "asiento de transferencia", "asiento bancario", "asiento de ajuste", "asiento de apertura", "asiento de cierre"
                ],
                category="accounting",
                priority=8,
                min_keyword_count=1
            ),
            
            "ratios_financieros": QueryPattern(
                keywords=["ratio", "índice", "indicador", "análisis financiero", "liquidez", "solvencia",
                         "rentabilidad", "actividad", "apalancamiento", "endeudamiento", "rotación",
                         "margen", "roa", "roe", "current ratio", "quick ratio", "debt ratio",
                         "profit margin", "asset turnover", "equity ratio", "dupont"],
                strong_indicators=["ratio", "roa", "roe", "current ratio", "quick ratio"],
                category="financial_analysis",
                priority=7
            ),
            
            "calculos_contables": QueryPattern(
                keywords=["calcular", "cálculo", "determinar", "cuánto", "valor", "importe",
                         "depreciación", "amortización", "provisión", "reserva", "utilidad",
                         "pérdida", "costo de ventas", "inventario", "cts", "vacaciones",
                         "gratificación", "impuesto a la renta", "participaciones"],
                strong_indicators=["calcular", "depreciación", "cts", "gratificación", "cuánto"],
                category="calculations",
                priority=7
            ),
            "consulta_general": QueryPattern(
                keywords=["por qué", "porqué", "porque", "cómo", "cuando", "cuándo", "dónde", 
                         "donde", "quién", "quien", "qué", "que", "cuál", "cual", "cuanto", 
                         "cuánto", "cuántos", "cuantos"],
                strong_indicators=["por qué", "cómo", "cuándo", "dónde", "quién"],
                category="general_knowledge",
                priority=5,  # BAJA PRIORIDAD
                min_keyword_count=1
            ),
            "regulatory": QueryPattern(
                keywords=["pcge", "plan contable", "niif", "nic", "norma", "resolución", "elementos del pcge", "estructura del pcge", "principio de materialidad", "principio de importancia relativa"],
                strong_indicators=["pcge", "plan contable", "niif", "nic", "principio de materialidad"],
                category="regulatory",
                priority=12,
                min_keyword_count=1
            )
        }

    def _preprocess_query(self, query: str) -> str:
        # Elimina artículos y preposiciones comunes para mejorar la detección
        return re.sub(r"\b(el|la|los|las|de|del|un|una|en|por|para|a|y|o|es|son|lo|al|su|sus|con|sin)\b", "", query.lower()).strip()

    def detect_query_type(self, query: str) -> Tuple[str, float, Dict]:
        """
        Detecta el tipo de consulta con nivel de confianza
        
        Returns:
            Tuple[tipo, confianza, metadatos]
        """
        query_lower = query.lower().strip()
        query_clean = self._preprocess_query(query_lower)
        results = []

        # Prioridad: Si la consulta inicia con "qué es", "que es", "definición de", etc., es educativo
        if re.match(r"^(qué|que)\s+es\b", query_lower) or re.match(r"^definición de\b", query_lower) or re.match(r"^que significa\b", query_lower) or re.match(r"^qué significa\b", query_lower):
            return "educativo", 1.0, {"category": "educational", "reason": "pattern_start"}

        # Casos especiales primero
        if self._is_simple_math_question(query_lower):
            return "general", 0.9, {"category": "general", "reason": "math_question"}
        
        if self._is_example_request(query_lower):
            return "educativo", 0.9, {"category": "educational", "reason": "example_request"}
        
        # Procesar cada patrón
        for query_type, pattern in self.patterns.items():
            score = self._calculate_pattern_score(query_clean, pattern)
            if score > 0:
                results.append((query_type, score))
        
        # Detectar préstamos específicamente
        if self._is_loan_query(query_lower):
            results.append(("asiento_contable", 0.9))
        
        # Ordenar por score y prioridad
        if results:
            results.sort(key=lambda x: (x[1], self.patterns[x[0]].priority), reverse=True)
            best_match = results[0]
            
            # Verificar confianza mínima
            if best_match[1] >= 0.3:
                return best_match[0], best_match[1], {"category": self.patterns[best_match[0]].category}
        
        # Detectar operaciones específicas como fallback
        if self._contains_financial_operations(query_lower):
            return "asiento_contable", 0.7, {"category": "accounting", "fallback": True}
        
        return "ai", 0.5, {}  # <-- Fallback a IA general
    
    def _is_simple_math_question(self, query: str) -> bool:
        """Detecta preguntas de matemática simple"""
        math_patterns = [
            r'\d+\s*[\+\-\*\/]\s*\d+',
            r'cuanto es \d+',
            r'suma de \d+',
            r'\d+ mas \d+',
            r'\d+ menos \d+',
            r'\d+ por \d+',
            r'\d+ entre \d+'
        ]
        
        for pattern in math_patterns:
            if re.search(pattern, query):
                return True
        return False
    
    def _is_example_request(self, query: str) -> bool:
        """Detecta solicitudes de ejemplo"""
        example_indicators = [
            "dame un ejemplo",
            "ejemplo de",
            "ejemplos de", 
            "muestra un ejemplo",
            "pon un ejemplo",
            "como ejemplo"
        ]
        
        return any(indicator in query for indicator in example_indicators)
    
    def _is_loan_query(self, query: str) -> bool:
        """Detecta específicamente consultas sobre préstamos"""
        loan_indicators = [
            r'préstamo\s+(?:de\s+)?(?:s/|soles?)\s*\d+',
            r'prestamo\s+(?:de\s+)?(?:s/|soles?)\s*\d+',
            r'\d+\s*(?:soles?|s/)\s+(?:préstamo|prestamo)',
            r'asiento.*préstamo',
            r'préstamo.*asiento',
            r'cuota.*préstamo',
            r'interés.*\d+%'
        ]
        
        for pattern in loan_indicators:
            if re.search(pattern, query):
                return True
        
        return False
    
    def _calculate_pattern_score(self, query: str, pattern: QueryPattern) -> float:
        """Calcula score para un patrón específico"""
        score = 0.0
        keyword_matches = 0
        strong_indicator_matches = 0
        
        # Contar coincidencias de keywords
        for keyword in pattern.keywords:
            if keyword in query:
                keyword_matches += 1
                score += 0.1
        
        # Contar indicadores fuertes
        for indicator in pattern.strong_indicators:
            if indicator in query:
                strong_indicator_matches += 1
                score += 0.5  # Aumentar peso de indicadores fuertes
        
        # Aplicar bonus por indicadores fuertes
        if strong_indicator_matches > 0:
            score *= 2.0  # Mayor multiplicador
        
        # Verificar mínimo de keywords
        if keyword_matches < pattern.min_keyword_count:
            score *= 0.3
        
        # Bonus por densidad de keywords
        query_words = len(query.split())
        if query_words > 0:
            density = keyword_matches / query_words
            if density > 0.3:
                score += 0.3
        
        return min(score, 1.0)  # Máximo 1.0
    
    def _contains_financial_operations(self, query: str) -> bool:
        """Detecta operaciones financieras como fallback"""
        operation_keywords = [
            "préstamo", "prestamo", "compra", "venta", "pago", "cobro", 
            "inversión", "dividendos", "aportes", "retiros", "transferencia", 
            "depósito", "intereses", "amortización"
        ]
        return any(keyword in query for keyword in operation_keywords)

# Instancia global del detector
query_detector = QueryDetector()

def detect_query_type(query: str) -> str:
    """Función wrapper para compatibilidad"""
    query_type, confidence, metadata = query_detector.detect_query_type(query)
    return query_type