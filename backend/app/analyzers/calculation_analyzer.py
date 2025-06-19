"""
Analizador especializado en cálculos contables y laborales
"""
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

@dataclass
class CalculationResult:
    """Resultado de un cálculo contable"""
    calculation_type: str
    result: float
    breakdown: Dict[str, float]
    formula_used: str
    legal_basis: List[str]
    recommendations: List[str]
    period: str

class CalculationAnalyzer:
    """Analizador especializado en cálculos contables"""
    
    def __init__(self):
        self.calculation_methods = self._initialize_calculation_methods()
        self.legal_rates = self._load_legal_rates()
        self.formulas = self._load_formulas()
    
    def _initialize_calculation_methods(self) -> Dict:
        """Inicializa métodos de cálculo disponibles"""
        return {
            "cts": self._calculate_cts,
            "vacation": self._calculate_vacation,
            "gratification": self._calculate_gratification,
            "depreciation": self._calculate_depreciation,
            "igv": self._calculate_igv
        }
    
    def _load_legal_rates(self) -> Dict:
        """Carga tasas legales vigentes en Perú"""
        return {
            "igv_rate": 0.18,
            "cts_rate": 1/12,
            "vacation_rate": 1/12,
            "gratification_rate": 2/12,
            "essalud_rate": 0.09,
            "uit_2024": 5150.00,
            "rmv_2024": 1025.00,
            "depreciation_rates": {
                "buildings": 0.03,
                "machinery": 0.10,
                "equipment": 0.10,
                "vehicles": 0.20,
                "furniture": 0.10,
                "computers": 0.25
            }
        }
    
    def _load_formulas(self) -> Dict:
        """Carga fórmulas de cálculo en formato LaTeX para MathJax"""
        return {
            "cts": r"$$\text{CTS} = \frac{\text{Sueldo} + \text{Gratificaciones} + \text{Horas Extras} + \text{Comisiones}}{12} \times \text{Meses trabajados}$$",
            "vacation": r"$$\text{Vacaciones} = (\text{Sueldo} + \text{Promedio de remuneraciones variables}) \times \frac{30}{360}$$",
            "gratification": r"$$\text{Gratificación} = (\text{Sueldo} + \text{Promedio de remuneraciones variables}) \times \frac{\text{Meses trabajados}}{6}$$",
            "depreciation": r"$$\text{Depreciación anual} = \frac{\text{Costo del Activo}}{\text{Vida Útil}}$$",
            "igv": r"$$\text{IGV} = \text{Base Imponible} \times 0.18$$"
        }
    
    def analyze_calculation_query(self, query: str) -> Dict:
        """Analiza una consulta de cálculo y determina el tipo"""
        query_lower = query.lower()
        
        # Detectar tipo de cálculo
        calc_type = self._detect_calculation_type(query_lower)
        
        # Extraer parámetros numéricos
        parameters = self._extract_calculation_parameters(query)
        
        return {
            "calculation_type": calc_type,
            "parameters": parameters,
            "confidence": self._calculate_detection_confidence(query_lower, calc_type)
        }
    
    def _detect_calculation_type(self, query: str) -> str:
        """Detecta el tipo de cálculo solicitado"""
        calculation_keywords = {
            "cts": ["cts", "compensación por tiempo de servicios", "compensacion"],
            "vacation": ["vacaciones", "descanso vacacional"],
            "gratification": ["gratificación", "aguinaldo", "sueldo extra"],
            "igv": ["igv", "impuesto general a las ventas"],
            "depreciation": ["depreciación", "desgaste", "vida útil", "activo fijo"]
        }
        
        for calc_type, keywords in calculation_keywords.items():
            if any(keyword in query for keyword in keywords):
                return calc_type
        
        return "general"
    
    def _extract_calculation_parameters(self, query: str) -> Dict:
        """Extrae parámetros numéricos de la consulta"""
        parameters = {}
        
        # Extraer montos monetarios
        money_patterns = [
            r'(?:s/|soles?)\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:soles?|s/)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        amounts = []
        for pattern in money_patterns:
            matches = re.findall(pattern, query)
            for match in matches:
                try:
                    amount = float(match.replace(',', ''))
                    amounts.append(amount)
                except ValueError:
                    continue
        
        if amounts:
            parameters["amount"] = amounts[0]
        
        return parameters
    
    def _calculate_detection_confidence(self, query: str, calc_type: str) -> float:
        """Calcula la confianza en la detección"""
        if calc_type == "general":
            return 0.3
        return 0.8
    
    def _calculate_cts(self, params: Dict) -> CalculationResult:
        """Calcula CTS"""
        sueldo = params.get("amount", 3000)
        meses = params.get("months", 6)
        
        cts_mensual = sueldo / 12
        cts_total = cts_mensual * meses
        
        return CalculationResult(
            calculation_type="cts",
            result=cts_total,
            breakdown={
                "sueldo_base": sueldo,
                "cts_mensual": cts_mensual,
                "meses_trabajados": meses,
                "cts_total": cts_total
            },
            formula_used=self.formulas["cts"],
            legal_basis=["D.S. 001-97-TR"],
            recommendations=["Depositar antes del 15 de mayo y 15 de noviembre"],
            period=f"{meses} meses"
        )
    
    def _calculate_vacation(self, params: Dict) -> CalculationResult:
        """Calcula vacaciones"""
        sueldo = params.get("amount", 3000)
        dias = params.get("days", 30)
        
        vacacion_diaria = sueldo / 30
        vacacion_total = vacacion_diaria * dias
        
        return CalculationResult(
            calculation_type="vacation",
            result=vacacion_total,
            breakdown={
                "sueldo_base": sueldo,
                "vacacion_diaria": vacacion_diaria,
                "dias_vacaciones": dias,
                "vacacion_total": vacacion_total
            },
            formula_used=self.formulas["vacation"],
            legal_basis=["D.S. 003-97-TR"],
            recommendations=["Goce físico o compensación económica"],
            period=f"{dias} días"
        )
    
    def _calculate_gratification(self, params: Dict) -> CalculationResult:
        """Calcula gratificación"""
        sueldo = params.get("amount", 3000)
        meses = params.get("months", 6)
        
        gratificacion = (sueldo * meses) / 6
        
        return CalculationResult(
            calculation_type="gratification",
            result=gratificacion,
            breakdown={
                "sueldo_base": sueldo,
                "meses_trabajados": meses,
                "gratificacion": gratificacion
            },
            formula_used=self.formulas["gratification"],
            legal_basis=["Ley 27735"],
            recommendations=["Pagar en julio y diciembre"],
            period=f"{meses} meses"
        )
    
    def _calculate_depreciation(self, params: Dict) -> CalculationResult:
        """Calcula depreciación"""
        valor = params.get("amount", 30000)
        tasa = self.legal_rates["depreciation_rates"]["machinery"]
        
        depreciacion_anual = valor * tasa
        depreciacion_mensual = depreciacion_anual / 12
        
        return CalculationResult(
            calculation_type="depreciation",
            result=depreciacion_anual,
            breakdown={
                "valor_activo": valor,
                "tasa_depreciacion": tasa,
                "depreciacion_anual": depreciacion_anual,
                "depreciacion_mensual": depreciacion_mensual
            },
            formula_used=self.formulas["depreciation"],
            legal_basis=["NIC 16", "Ley del Impuesto a la Renta"],
            recommendations=["Revisar vida útil según uso real"],
            period="anual"
        )
    
    def _calculate_igv(self, params: Dict) -> CalculationResult:
        """Calcula IGV"""
        base = params.get("amount", 1000)
        tasa_igv = self.legal_rates["igv_rate"]
        
        igv = base * tasa_igv
        total = base + igv
        
        return CalculationResult(
            calculation_type="igv",
            result=igv,
            breakdown={
                "base_imponible": base,
                "tasa_igv": tasa_igv,
                "igv": igv,
                "total_con_igv": total
            },
            formula_used=self.formulas["igv"],
            legal_basis=["D.S. 055-99-EF"],
            recommendations=["Verificar si operación está gravada"],
            period="por operación"
        )

# Instancia global
calculation_analyzer = CalculationAnalyzer()
