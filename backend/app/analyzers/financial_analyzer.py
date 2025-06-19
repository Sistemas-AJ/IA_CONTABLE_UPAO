"""
Analizador financiero especializado en ratios y estados financieros
"""
import math
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from ..core.utils import format_currency, calculate_percentage_change, generate_table_markdown

@dataclass
class FinancialRatio:
    """Estructura para un ratio financiero"""
    name: str
    value: float
    formula: str
    interpretation: str
    category: str
    ideal_range: Tuple[float, float]
    industry_avg: Optional[float] = None

@dataclass
class FinancialStatement:
    """Estructura para estados financieros"""
    period: str
    accounts: Dict[str, float]
    totals: Dict[str, float]

class FinancialAnalyzer:
    """Analizador especializado en análisis financiero"""
    
    def __init__(self):
        self.ratio_definitions = self._initialize_ratios()
        self.industry_benchmarks = self._load_benchmarks()
    
    def _initialize_ratios(self) -> Dict[str, Dict]:
        """Define todos los ratios financieros disponibles"""
        return {
            # RATIOS DE LIQUIDEZ
            "current_ratio": {
                "name": "Ratio de Liquidez Corriente",
                "formula": r"$$\text{Current Ratio} = \frac{\text{Activos\ Corrientes}}{\text{Pasivos\ Corrientes}}$$",
                "category": "liquidez",
                "ideal_range": (1.2, 2.0),
                "interpretation": {
                    "low": "Posibles problemas de liquidez",
                    "normal": "Liquidez adecuada",
                    "high": "Exceso de liquidez, posible ineficiencia"
                }
            },
            "quick_ratio": {
                "name": "Ratio de Liquidez Ácida",
                "formula": r"$$\text{Quick Ratio} = \frac{\text{Activos\ Corrientes} - \text{Inventarios}}{\text{Pasivos\ Corrientes}}$$",
                "category": "liquidez",
                "ideal_range": (0.8, 1.2),
                "interpretation": {
                    "low": "Dependencia excesiva de inventarios",
                    "normal": "Liquidez inmediata apropiada",
                    "high": "Excelente capacidad de pago inmediato"
                }
            },
            "cash_ratio": {
                "name": "Ratio de Liquidez Absoluta",
                "formula": r"$$\text{Cash Ratio} = \frac{\text{Efectivo} + \text{Equivalentes}}{\text{Pasivos\ Corrientes}}$$",
                "category": "liquidez",
                "ideal_range": (0.2, 0.5),
                "interpretation": {
                    "low": "Limitada capacidad de pago inmediato",
                    "normal": "Capacidad de pago inmediato adecuada",
                    "high": "Exceso de efectivo ocioso"
                }
            },

            # RATIOS DE ACTIVIDAD
            "inventory_turnover": {
                "name": "Rotación de Inventarios",
                "formula": r"$$\text{Rotación\ de\ Inventarios} = \frac{\text{Costo\ de\ Ventas}}{\text{Inventario\ Promedio}}$$",
                "category": "actividad",
                "ideal_range": (4.0, 12.0),
                "interpretation": {
                    "low": "Inventarios obsoletos o sobrestock",
                    "normal": "Gestión eficiente de inventarios",
                    "high": "Posible desabastecimiento"
                }
            },
            "receivables_turnover": {
                "name": "Rotación de Cuentas por Cobrar",
                "formula": r"$$\text{Rotación\ de\ CxC} = \frac{\text{Ventas}}{\text{Cuentas\ por\ Cobrar\ Promedio}}$$",
                "category": "actividad",
                "ideal_range": (6.0, 15.0),
                "interpretation": {
                    "low": "Políticas de cobranza deficientes",
                    "normal": "Gestión adecuada de cobranzas",
                    "high": "Excelente gestión de cobranzas"
                }
            },
            "asset_turnover": {
                "name": "Rotación de Activos Totales",
                "formula": r"$$\text{Rotación\ de\ Activos} = \frac{\text{Ventas}}{\text{Activos\ Totales\ Promedio}}$$",
                "category": "actividad",
                "ideal_range": (0.5, 2.0),
                "interpretation": {
                    "low": "Baja eficiencia en uso de activos",
                    "normal": "Uso eficiente de activos",
                    "high": "Excelente productividad de activos"
                }
            },

            # RATIOS DE ENDEUDAMIENTO
            "debt_ratio": {
                "name": "Ratio de Endeudamiento",
                "formula": r"$$\text{Debt Ratio} = \frac{\text{Total\ Pasivos}}{\text{Total\ Activos}}$$",
                "category": "endeudamiento",
                "ideal_range": (0.3, 0.6),
                "interpretation": {
                    "low": "Bajo apalancamiento, conservador",
                    "normal": "Apalancamiento equilibrado",
                    "high": "Alto riesgo financiero"
                }
            },
            "equity_ratio": {
                "name": "Ratio de Patrimonio",
                "formula": r"$$\text{Equity Ratio} = \frac{\text{Patrimonio}}{\text{Total\ Activos}}$$",
                "category": "endeudamiento",
                "ideal_range": (0.4, 0.7),
                "interpretation": {
                    "low": "Alta dependencia de deuda",
                    "normal": "Estructura financiera equilibrada",
                    "high": "Sólida autonomía financiera"
                }
            },
            "debt_to_equity": {
                "name": "Ratio Deuda/Patrimonio",
                "formula": r"$$\text{Debt to Equity} = \frac{\text{Total\ Pasivos}}{\text{Patrimonio}}$$",
                "category": "endeudamiento",
                "ideal_range": (0.3, 1.5),
                "interpretation": {
                    "low": "Estructura conservadora",
                    "normal": "Apalancamiento adecuado",
                    "high": "Estructura agresiva, alto riesgo"
                }
            },

            # RATIOS DE RENTABILIDAD
            "roa": {
                "name": "Rentabilidad sobre Activos (ROA)",
                "formula": r"$$\text{ROA} = \frac{\text{Utilidad\ Neta}}{\text{Activos\ Totales\ Promedio}}$$",
                "category": "rentabilidad",
                "ideal_range": (0.05, 0.15),
                "interpretation": {
                    "low": "Baja eficiencia en generación de utilidades",
                    "normal": "Rentabilidad adecuada de activos",
                    "high": "Excelente rentabilidad de activos"
                }
            },
            "roe": {
                "name": "Rentabilidad sobre Patrimonio (ROE)",
                "formula": r"$$\text{ROE} = \frac{\text{Utilidad\ Neta}}{\text{Patrimonio\ Promedio}}$$",
                "category": "rentabilidad",
                "ideal_range": (0.10, 0.25),
                "interpretation": {
                    "low": "Baja rentabilidad para accionistas",
                    "normal": "Rentabilidad atractiva",
                    "high": "Excelente rentabilidad para accionistas"
                }
            },
            "profit_margin": {
                "name": "Margen de Utilidad Neta",
                "formula": r"$$\text{Margen\ Neta} = \frac{\text{Utilidad\ Neta}}{\text{Ventas}}$$",
                "category": "rentabilidad",
                "ideal_range": (0.05, 0.20),
                "interpretation": {
                    "low": "Márgenes ajustados, control de costos",
                    "normal": "Márgenes saludables",
                    "high": "Excelente control de costos"
                }
            },
            "gross_margin": {
                "name": "Margen Bruto",
                "formula": r"$$\text{Margen\ Bruto} = \frac{\text{Ventas} - \text{Costo\ de\ Ventas}}{\text{Ventas}}$$",
                "category": "rentabilidad",
                "ideal_range": (0.20, 0.50),
                "interpretation": {
                    "low": "Presión en costos directos",
                    "normal": "Margen bruto saludable",
                    "high": "Excelente control de costos directos"
                }
            }
        }
    
    def _load_benchmarks(self) -> Dict[str, Dict[str, float]]:
        """Carga benchmarks de industria (valores ejemplo para Perú)"""
        return {
            "retail": {
                "current_ratio": 1.4,
                "quick_ratio": 0.9,
                "inventory_turnover": 8.0,
                "roa": 0.08,
                "roe": 0.15,
                "debt_ratio": 0.45
            },
            "manufacturing": {
                "current_ratio": 1.6,
                "quick_ratio": 1.1,
                "inventory_turnover": 6.0,
                "roa": 0.10,
                "roe": 0.18,
                "debt_ratio": 0.50
            },
            "services": {
                "current_ratio": 1.3,
                "quick_ratio": 1.2,
                "asset_turnover": 1.5,
                "roa": 0.12,
                "roe": 0.20,
                "debt_ratio": 0.40
            },
            "general": {
                "current_ratio": 1.5,
                "quick_ratio": 1.0,
                "roa": 0.10,
                "roe": 0.18,
                "debt_ratio": 0.45
            }
        }
    
    def calculate_ratio(self, ratio_name: str, data: Dict[str, float]) -> Optional[FinancialRatio]:
        """Calcula un ratio específico"""
        if ratio_name not in self.ratio_definitions:
            return None
        
        ratio_def = self.ratio_definitions[ratio_name]
        
        try:
            value = self._compute_ratio_value(ratio_name, data)
            if value is None:
                return None
            
            interpretation = self._interpret_ratio(ratio_name, value)
            
            return FinancialRatio(
                name=ratio_def["name"],
                value=value,
                formula=ratio_def["formula"],
                interpretation=interpretation,
                category=ratio_def["category"],
                ideal_range=ratio_def["ideal_range"],
                industry_avg=self._get_industry_avg(ratio_name, data.get("industry", "general"))
            )
            
        except Exception as e:
            print(f"Error calculando {ratio_name}: {e}")
            return None
    
    def _compute_ratio_value(self, ratio_name: str, data: Dict[str, float]) -> Optional[float]:
        """Computa el valor numérico del ratio"""
        
        calculations = {
            "current_ratio": lambda: data["activo_corriente"] / data["pasivo_corriente"],
            "quick_ratio": lambda: (data["activo_corriente"] - data.get("inventarios", 0)) / data["pasivo_corriente"],
            "cash_ratio": lambda: data.get("efectivo", 0) / data["pasivo_corriente"],
            "inventory_turnover": lambda: data["costo_ventas"] / data.get("inventarios", 1),
            "receivables_turnover": lambda: data["ventas"] / data.get("cuentas_por_cobrar", 1),
            "asset_turnover": lambda: data["ventas"] / data["activos_totales"],
            "debt_ratio": lambda: data["total_pasivos"] / data["activos_totales"],
            "equity_ratio": lambda: data["patrimonio"] / data["activos_totales"],
            "debt_to_equity": lambda: data["total_pasivos"] / data["patrimonio"],
            "roa": lambda: data["utilidad_neta"] / data["activos_totales"],
            "roe": lambda: data["utilidad_neta"] / data["patrimonio"],
            "profit_margin": lambda: data["utilidad_neta"] / data["ventas"],
            "gross_margin": lambda: (data["ventas"] - data["costo_ventas"]) / data["ventas"]
        }
        
        if ratio_name in calculations:
            try:
                result = calculations[ratio_name]()
                return result if not math.isnan(result) and math.isfinite(result) else None
            except (ZeroDivisionError, KeyError):
                return None
        
        return None
    
    def _interpret_ratio(self, ratio_name: str, value: float) -> str:
        """Interpreta el valor del ratio"""
        ratio_def = self.ratio_definitions[ratio_name]
        interpretations = ratio_def.get("interpretation", {})
        ideal_range = ratio_def["ideal_range"]
        
        if value < ideal_range[0]:
            return interpretations.get("low", "Valor por debajo del rango ideal")
        elif value > ideal_range[1]:
            return interpretations.get("high", "Valor por encima del rango ideal")
        else:
            return interpretations.get("normal", "Valor dentro del rango ideal")
    
    def _get_industry_avg(self, ratio_name: str, industry: str) -> Optional[float]:
        """Obtiene promedio de industria"""
        return self.industry_benchmarks.get(industry, {}).get(ratio_name)
    
    def analyze_financial_statements(self, current_period: Dict, previous_period: Optional[Dict] = None) -> Dict:
        """Análisis completo de estados financieros"""
        analysis = {
            "vertical_analysis": self._vertical_analysis(current_period),
            "ratios": self._calculate_all_ratios(current_period),
            "summary": self._generate_summary(current_period)
        }
        
        if previous_period:
            analysis["horizontal_analysis"] = self._horizontal_analysis(current_period, previous_period)
            analysis["trend_analysis"] = self._trend_analysis(current_period, previous_period)
        
        return analysis
    
    def _vertical_analysis(self, data: Dict) -> Dict:
        """Análisis vertical - composición porcentual"""
        total_assets = data.get("activos_totales", 0)
        if total_assets == 0:
            return {}
        
        return {
            "activo_corriente_pct": (data.get("activo_corriente", 0) / total_assets) * 100,
            "activo_no_corriente_pct": (data.get("activo_no_corriente", 0) / total_assets) * 100,
            "pasivo_corriente_pct": (data.get("pasivo_corriente", 0) / total_assets) * 100,
            "pasivo_no_corriente_pct": (data.get("pasivo_no_corriente", 0) / total_assets) * 100,
            "patrimonio_pct": (data.get("patrimonio", 0) / total_assets) * 100
        }
    
    def _horizontal_analysis(self, current: Dict, previous: Dict) -> Dict:
        """Análisis horizontal - variaciones período a período"""
        analysis = {}
        
        for key in current.keys():
            if key in previous and isinstance(current[key], (int, float)):
                current_val = current[key]
                previous_val = previous[key]
                
                if previous_val != 0:
                    variation_pct = calculate_percentage_change(previous_val, current_val)
                    analysis[f"{key}_variation"] = {
                        "absolute": current_val - previous_val,
                        "percentage": variation_pct,
                        "current": current_val,
                        "previous": previous_val
                    }
        
        return analysis
    
    def _trend_analysis(self, current: Dict, previous: Dict) -> Dict:
        """Análisis de tendencias"""
        trends = {}
        
        # Analizar tendencias principales
        key_metrics = ["ventas", "utilidad_neta", "activos_totales", "patrimonio"]
        
        for metric in key_metrics:
            if metric in current and metric in previous:
                change = calculate_percentage_change(previous[metric], current[metric])
                
                if change > 10:
                    trend = "crecimiento_fuerte"
                elif change > 0:
                    trend = "crecimiento_moderado"
                elif change > -10:
                    trend = "estable"
                else:
                    trend = "decrecimiento"
                
                trends[metric] = {
                    "trend": trend,
                    "change_pct": change,
                    "description": self._describe_trend(trend, change)
                }
        
        return trends
    
    def _describe_trend(self, trend: str, change_pct: float) -> str:
        """Describe la tendencia en texto"""
        descriptions = {
            "crecimiento_fuerte": f"Crecimiento fuerte del {change_pct:.1f}%",
            "crecimiento_moderado": f"Crecimiento moderado del {change_pct:.1f}%",
            "estable": f"Variación mínima del {change_pct:.1f}%",
            "decrecimiento": f"Decrecimiento del {change_pct:.1f}%"
        }
        return descriptions.get(trend, f"Variación del {change_pct:.1f}%")
    
    def _calculate_all_ratios(self, data: Dict) -> Dict[str, FinancialRatio]:
        """Calcula todos los ratios disponibles"""
        ratios = {}
        
        for ratio_name in self.ratio_definitions.keys():
            ratio = self.calculate_ratio(ratio_name, data)
            if ratio:
                ratios[ratio_name] = ratio
        
        return ratios
    
    def _generate_summary(self, data: Dict) -> Dict:
        """Genera resumen ejecutivo del análisis"""
        ratios = self._calculate_all_ratios(data)
        
        summary = {
            "liquidity_status": "adequate",
            "profitability_status": "adequate", 
            "leverage_status": "adequate",
            "efficiency_status": "adequate",
            "overall_score": 0.0,
            "key_strengths": [],
            "areas_for_improvement": [],
            "recommendations": []
        }
        
        # Evaluar cada categoría
        category_scores = {}
        
        for category in ["liquidez", "rentabilidad", "endeudamiento", "actividad"]:
            category_ratios = [r for r in ratios.values() if r.category == category]
            if category_ratios:
                # Score basado en qué tan cerca están del rango ideal
                scores = []
                for ratio in category_ratios:
                    ideal_min, ideal_max = ratio.ideal_range
                    if ideal_min <= ratio.value <= ideal_max:
                        scores.append(1.0)
                    else:
                        # Penalizar desviaciones del rango ideal
                        if ratio.value < ideal_min:
                            scores.append(max(0.0, ratio.value / ideal_min))
                        else:
                            scores.append(max(0.0, ideal_max / ratio.value))
                
                category_scores[category] = sum(scores) / len(scores) if scores else 0.5
        
        # Score general
        summary["overall_score"] = sum(category_scores.values()) / len(category_scores) if category_scores else 0.5
        
        # Determinar fortalezas y áreas de mejora
        for category, score in category_scores.items():
            if score >= 0.8:
                summary["key_strengths"].append(f"Excelente {category}")
            elif score <= 0.4:
                summary["areas_for_improvement"].append(f"Mejorar {category}")
        
        return summary

# Instancia global
financial_analyzer = FinancialAnalyzer()