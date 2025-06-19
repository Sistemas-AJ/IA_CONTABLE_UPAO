"""
Servicio especializado en análisis financiero y ratios
"""
import re
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class FinancialService:
    """Servicio especializado en análisis financiero"""
    
    async def generate_response(self, query: str, context: Dict, metadata: Dict) -> str:
        """Genera análisis financiero"""
        query_lower = query.lower()
        
        if "roe" in query_lower:
            return self._calculate_roe(query)
        elif "roa" in query_lower:
            return self._calculate_roa(query)
        elif "current ratio" in query_lower or "liquidez" in query_lower:
            return self._calculate_current_ratio(query)
        elif "ratio" in query_lower and "ejemplo" in query_lower:
            return self._generate_ratio_example()
        else:
            return self._generate_ratios_overview()
    
    def _calculate_roe(self, query: str) -> str:
        """Calcula ROE"""
        numbers = re.findall(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', query)
        
        if len(numbers) >= 2:
            utilidad = float(numbers[0].replace(',', ''))
            patrimonio = float(numbers[1].replace(',', ''))
            roe = (utilidad / patrimonio) * 100
            
            return f"""## **📊 Cálculo de ROE**

### **📋 Datos:**
- **Utilidad Neta:** S/ {utilidad:,.2f}
- **Patrimonio:** S/ {patrimonio:,.2f}

### **📐 Fórmula:**
$$
\\text{{ROE}} = \\frac{{\\text{{Utilidad\\ Neta}}}}{{\\text{{Patrimonio}}}} \\times 100
$$

### **🧮 Cálculo:**
$$
\\text{{ROE}} = \\frac{{{utilidad:,.0f}}}{{{patrimonio:,.0f}}} \\times 100 = {roe:.2f}\\%
$$

### **🔍 Interpretación:**
- **{roe:.1f}%** {"es excelente" if roe > 15 else "es aceptable" if roe > 10 else "es bajo"}
- Por cada sol de patrimonio se generan **{roe/100:.3f} soles** de utilidad

### **⚖️ Benchmarks:**
- **< 10%:** Baja rentabilidad
- **10-15%:** Rentabilidad aceptable
- **> 15%:** Excelente rentabilidad"""
        
        return self._generate_roe_help()
    
    def _generate_ratio_example(self) -> str:
        """Ejemplo de ratio"""
        return """## **📊 Ejemplo: Current Ratio**

### **📋 Empresa ABC SAC:**
- **Activo Corriente:** S/ 150,000
- **Pasivo Corriente:** S/ 75,000

### **📐 Fórmula:**
$$
\\text{Current Ratio} = \\frac{\\text{Activos\\ Corrientes}}{\\text{Pasivos\\ Corrientes}}
$$

### **🧮 Cálculo:**
$$
\\text{Current Ratio} = \\frac{150,000}{75,000} = 2.0
$$

### **🔍 Interpretación:**
- La empresa tiene **S/ 2.00** en activos corrientes por cada **S/ 1.00** de deuda a corto plazo
- **Excelente liquidez** para cubrir obligaciones inmediatas
- Ratio ideal entre **1.5 - 2.5**"""

    def _generate_ratios_overview(self) -> str:
        """Vista general de ratios"""
        return """## **📊 Ratios Financieros**

### **💧 Liquidez:**
- **Current Ratio:** $\\frac{\\text{Activos\\ Corrientes}}{\\text{Pasivos\\ Corrientes}}$
- **Quick Ratio:** $\\frac{\\text{Activos\\ Corrientes} - \\text{Inventarios}}{\\text{Pasivos\\ Corrientes}}$

### **💰 Rentabilidad:**
- **ROE:** $\\frac{\\text{Utilidad\\ Neta}}{\\text{Patrimonio}} \\times 100$
- **ROA:** $\\frac{\\text{Utilidad\\ Neta}}{\\text{Activos\\ Totales}} \\times 100$
- **Margen Neto:** $\\frac{\\text{Utilidad\\ Neta}}{\\text{Ventas}} \\times 100$

### **⚡ Actividad:**
- **Rotación Inventarios:** $\\frac{\\text{Costo\\ de\\ Ventas}}{\\text{Inventario}}$
- **Rotación CxC:** $\\frac{\\text{Ventas}}{\\text{Cuentas\\ por\\ Cobrar}}$

### **📊 Endeudamiento:**
- **Debt Ratio:** $\\frac{\\text{Pasivos}}{\\text{Activos}}$
- **Debt-to-Equity:** $\\frac{\\text{Pasivos}}{\\text{Patrimonio}}$

**¿Qué ratio específico quieres calcular?**"""

    def _calculate_roa(self, query: str) -> str:
        """Calcula ROA"""
        numbers = re.findall(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', query)
        if len(numbers) >= 2:
            utilidad = float(numbers[0].replace(',', ''))
            activos = float(numbers[1].replace(',', ''))
            roa = (utilidad / activos) * 100

            return f"""## **📊 Cálculo de ROA**

### **📋 Datos:**
- **Utilidad Neta:** S/ {utilidad:,.2f}
- **Activos Totales:** S/ {activos:,.2f}

### **📐 Fórmula:**
$$
\\text{{ROA}} = \\frac{{\\text{{Utilidad\\ Neta}}}}{{\\text{{Activos\\ Totales}}}} \\times 100
$$

### **🧮 Cálculo:**
$$
\\text{{ROA}} = \\frac{{{utilidad:,.0f}}}{{{activos:,.0f}}} \\times 100 = {roa:.2f}\\%
$$

### **🔍 Interpretación:**
- **{roa:.1f}%** {"es excelente" if roa > 10 else "es aceptable" if roa > 5 else "es bajo"}
- Por cada sol invertido en activos, la empresa genera **{roa/100:.3f} soles** de utilidad

### **⚖️ Benchmarks:**
- **< 5%:** Baja eficiencia
- **5-10%:** Eficiencia aceptable
- **> 10%:** Excelente eficiencia"""
        return (
            "Para calcular el ROA (Return on Assets), proporciona la utilidad neta y los activos totales. "
            "Ejemplo: 'Calcula el ROA con utilidad 15,000 y activos 100,000'"
        )

    def _calculate_current_ratio(self, query: str) -> str:
        """Calcula Current Ratio o muestra la fórmula si la consulta lo pide"""
        query_lower = query.lower()
        if "fórmula" in query_lower or "formula" in query_lower:
            return """
**Fórmula:**

$$
\\text{Current Ratio} = \\frac{\\text{Activos\\ Corrientes}}{\\text{Pasivos\\ Corrientes}}
$$
"""
        numbers = re.findall(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', query)
        if len(numbers) >= 2:
            activos = float(numbers[0].replace(',', ''))
            pasivos = float(numbers[1].replace(',', ''))
            ratio = activos / pasivos

            return f"""## **📊 Cálculo de Current Ratio**

### **📋 Datos:**
- **Activo Corriente:** S/ {activos:,.2f}
- **Pasivo Corriente:** S/ {pasivos:,.2f}

### **📐 Fórmula:**
$$
\\text{{Current Ratio}} = \\frac{{\\text{{Activos\\ Corrientes}}}}{{\\text{{Pasivos\\ Corrientes}}}}
$$

### **🧮 Cálculo:**
$$
\\text{{Current Ratio}} = \\frac{{{activos:,.0f}}}{{{pasivos:,.0f}}} = {ratio:.2f}
$$

### **🔍 Interpretación:**
- La empresa tiene **S/ {ratio:.2f}** en activos corrientes por cada **S/ 1.00** de deuda a corto plazo
- {"Excelente liquidez" if ratio > 2 else "Liquidez adecuada" if ratio >= 1.5 else "Posible problema de liquidez"}
- Ratio ideal entre **1.5 - 2.5**"""
        return (
            "Para calcular el Current Ratio, proporciona el activo corriente y el pasivo corriente. "
            "Ejemplo: 'Calcula el Current Ratio con activo 150,000 y pasivo 75,000'"
        )

    def _generate_roe_help(self) -> str:
        """Ayuda para ROE"""
        return (
            "Para calcular el ROE (Return on Equity), proporciona la utilidad neta y el patrimonio. "
            "Ejemplo: 'Calcula el ROE con utilidad 15,000 y patrimonio 100,000'"
        )

# Instancia global
financial_service = FinancialService()