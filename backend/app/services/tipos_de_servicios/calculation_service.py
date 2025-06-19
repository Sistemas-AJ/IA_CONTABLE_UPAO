"""
Servicio especializado en cálculos contables
"""
import re
import logging
from typing import Dict
from datetime import datetime
from ...core.utils import format_currency  # ⬅️ CORREGIR: tres puntos en lugar de dos

logger = logging.getLogger(__name__)

class CalculationService:
    """Servicio especializado en cálculos contables"""
    
    async def generate_response(self, query: str, context: Dict, metadata: Dict) -> str:
        """Genera respuesta para cálculos contables"""
        query_lower = query.lower()
        
        if "cts" in query_lower:
            return self._calculate_cts(query)
        elif "deprecia" in query_lower:
            return self._calculate_depreciation(query)
        elif "igv" in query_lower:
            return self._calculate_igv(query)
        elif "vacacion" in query_lower:
            return self._calculate_vacation(query)
        else:
            return self._generate_calculation_help()
    
    def _calculate_cts(self, query: str) -> str:
        """Calcula CTS"""
        sueldo_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', query)
        sueldo = float(sueldo_match.group(1).replace(',', '')) if sueldo_match else 3000
        
        cts_mensual = sueldo / 12
        cts_semestral = cts_mensual * 6
        
        return f"""## **🧮 Cálculo de CTS**

### **📋 Datos:**
- **Sueldo básico:** {format_currency(sueldo)}
- **Período:** 6 meses

### **📐 Fórmula:**
```
CTS = Sueldo ÷ 12 × Meses trabajados
```

### **🧮 Cálculo:**
- **CTS mensual:** {format_currency(sueldo)} ÷ 12 = {format_currency(cts_mensual)}
- **CTS semestral:** {format_currency(cts_mensual)} × 6 = {format_currency(cts_semestral)}

### **📋 Asiento Contable:**

| Cuenta | Denominación | Debe | Haber |
|--------|--------------|------|-------|
| 62171 | CTS | {format_currency(cts_semestral)} | - |
| 41511 | CTS por pagar | - | {format_currency(cts_semestral)} |

**¿Necesitas calcular para otros períodos?**"""

    def _calculate_depreciation(self, query: str) -> str:
        """Calcula depreciación"""
        valor_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', query)
        valor = float(valor_match.group(1).replace(',', '')) if valor_match else 30000
        
        if "maquinaria" in query.lower():
            tasa = 0.10
            tipo = "Maquinaria"
        elif "vehiculo" in query.lower():
            tasa = 0.20
            tipo = "Vehículo"
        else:
            tasa = 0.10
            tipo = "Activo Fijo"
        
        dep_anual = valor * tasa
        dep_mensual = dep_anual / 12
        
        return f"""## **🧮 Cálculo de Depreciación**

### **📋 Datos:**
- **Tipo:** {tipo}
- **Valor:** {format_currency(valor)}
- **Tasa:** {tasa*100:.0f}% anual

### **🧮 Cálculo:**
- **Depreciación anual:** {format_currency(dep_anual)}
- **Depreciación mensual:** {format_currency(dep_mensual)}

### **📋 Asiento Mensual:**

| Cuenta | Denominación | Debe | Haber |
|--------|--------------|------|-------|
| 68141 | Depreciación | {format_currency(dep_mensual)} | - |
| 39131 | Depreciación acumulada | - | {format_currency(dep_mensual)} |"""

    def _calculate_igv(self, query: str) -> str:
        """Calcula IGV"""
        monto_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', query)
        monto = float(monto_match.group(1).replace(',', '')) if monto_match else 1000
        
        igv = monto * 0.18
        total = monto + igv
        
        return f"""## **🧮 Cálculo de IGV**

### **📋 Datos:**
- **Base imponible:** {format_currency(monto)}
- **Tasa IGV:** 18%

### **🧮 Cálculo:**
- **IGV:** {format_currency(monto)} × 18% = {format_currency(igv)}
- **Total:** {format_currency(total)}

### **📋 Asiento de Compra:**

| Cuenta | Denominación | Debe | Haber |
|--------|--------------|------|-------|
| 60111 | Mercaderías | {format_currency(monto)} | - |
| 40111 | IGV Crédito fiscal | {format_currency(igv)} | - |
| 42121 | Facturas por pagar | - | {format_currency(total)} |"""

    def _calculate_vacation(self, query: str) -> str:
        """Calcula vacaciones"""
        sueldo_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', query)
        sueldo = float(sueldo_match.group(1).replace(',', '')) if sueldo_match else 3000
        
        vacacion_mensual = sueldo
        dias_vacaciones = 30
        
        return f"""## **🧮 Cálculo de Vacaciones**

### **📋 Datos:**
- **Sueldo básico:** {format_currency(sueldo)}
- **Días de vacaciones:** {dias_vacaciones} días

### **📐 Fórmula:**
```
Vacaciones = Sueldo mensual × 1 mes
```

### **🧮 Cálculo:**
- **Vacaciones:** {format_currency(vacacion_mensual)}

### **📋 Asiento Contable:**

| Cuenta | Denominación | Debe | Haber |
|--------|--------------|------|-------|
| 62172 | Vacaciones | {format_currency(vacacion_mensual)} | - |
| 41512 | Vacaciones por pagar | - | {format_currency(vacacion_mensual)} |

**¿Necesitas calcular para otros períodos?**"""

    def _generate_calculation_help(self) -> str:
        """Ayuda general sobre cálculos"""
        return """## **🧮 Cálculos Disponibles**

### **👥 Laborales:**
- **CTS:** *"Calcula CTS de S/ 3,000"*
- **Vacaciones:** *"Vacaciones de S/ 2,500"*

### **🏢 Activos:**
- **Depreciación:** *"Depreciación de maquinaria S/ 50,000"*

### **💰 Tributarios:**
- **IGV:** *"IGV de S/ 5,000"*

**¿Qué cálculo necesitas?**"""

# Instancia global
calculation_service = CalculationService()