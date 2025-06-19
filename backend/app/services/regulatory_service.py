"""
Servicio especializado en normativa y regulaciones contables
"""
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class RegulatoryService:
    """Servicio especializado en normativa contable peruana"""
    
    async def generate_response(self, query: str, context: Dict, metadata: Dict) -> str:
        """Genera respuesta sobre normativa contable"""
        query_lower = query.lower()
        
        if "pcge" in query_lower or "plan contable" in query_lower:
            return self._pcge_info()
        elif "niif" in query_lower or "ifrs" in query_lower:
            return self._niif_info()
        elif "sunat" in query_lower:
            return self._sunat_regulations()
        elif "libros" in query_lower and "contable" in query_lower:
            return self._accounting_books()
        else:
            return self._general_regulatory_help()
    
    def _pcge_info(self) -> str:
        """Información sobre PCGE"""
        return """## **📚 Plan Contable General Empresarial (PCGE)**

### **📋 Información General:**
- **Vigencia:** Desde 2019 (Resolución CNC N° 043-2019-EF/30)
- **Ámbito:** Todas las empresas del país
- **Base:** Normas Internacionales de Información Financiera (NIIF)

### **📊 Estructura del PCGE:**

#### **Elemento 1: Activo Disponible y Exigible**
- **10** Efectivo y equivalentes de efectivo
- **11** Inversiones financieras
- **12** Cuentas por cobrar comerciales - terceros
- **16** Cuentas por cobrar diversas - terceros
- **19** Estimación de cuentas de cobranza dudosa

#### **Elemento 2: Activo Realizable**
- **20** Mercaderías
- **21** Productos terminados
- **23** Productos en proceso
- **24** Materias primas
- **28** Existencias por recibir

#### **Elemento 3: Activo Inmovilizado**
- **30** Inversiones mobiliarias
- **31** Inversiones inmobiliarias
- **33** Inmuebles, maquinaria y equipo
- **34** Intangibles
- **39** Depreciación, amortización y agotamiento acumulados

#### **Elemento 4: Pasivo**
- **40** Tributos, contraprestaciones y aportes al sistema de pensiones
- **41** Remuneraciones y participaciones por pagar
- **42** Cuentas por pagar comerciales - terceros
- **45** Obligaciones financieras
- **49** Pasivo diferido

#### **Elemento 5: Patrimonio**
- **50** Capital
- **52** Capital adicional
- **56** Resultados no realizados
- **58** Reservas
- **59** Resultados acumulados

### **🔗 Principales Cambios 2019:**
- Mayor detalle en subcuentas
- Alineación total con NIIF
- Nuevas cuentas para instrumentos financieros
- Actualización de estimaciones y provisiones

**¿Necesitas información específica de alguna cuenta?**"""

    def _niif_info(self) -> str:
        """Información sobre NIIF"""
        return """## **🌐 Normas Internacionales de Información Financiera (NIIF)**

### **📋 NIIF Vigentes en Perú:**

#### **📊 NIIF Principales:**
- **NIIF 1:** Adopción por Primera Vez
- **NIIF 9:** Instrumentos Financieros
- **NIIF 15:** Ingresos de Actividades Ordinarias
- **NIIF 16:** Arrendamientos

#### **📈 NIC Principales:**
- **NIC 1:** Presentación de Estados Financieros
- **NIC 2:** Inventarios
- **NIC 16:** Propiedades, Planta y Equipo
- **NIC 18:** Ingresos de Actividades Ordinarias
- **NIC 36:** Deterioro del Valor de los Activos

### **⚖️ Aplicación en Perú:**

#### **📋 Empresas Obligadas:**
- Sociedades anónimas abiertas
- Bancos y financieras
- Seguros y AFP
- Empresas de interés público

#### **📊 NIIF para PYMES:**
- Empresas pequeñas y medianas
- Versión simplificada
- Mayor flexibilidad

### **🔄 Actualizaciones Recientes:**
- **NIIF 17:** Contratos de Seguros (2023)
- **NIIF 16:** Arrendamientos (implementación)
- **CINIIF 23:** Incertidumbre frente a Tratamientos del Impuesto

### **📚 Recursos:**
- Consejo Normativo de Contabilidad (CNC)
- Colegio de Contadores Públicos
- IASB (International Accounting Standards Board)

**¿Necesitas información específica sobre alguna NIIF?**"""

    def _accounting_books(self) -> str:
        """Libros contables obligatorios"""
        return """## **📚 Libros Contables Obligatorios**

### **📋 Según Régimen Tributario:**

#### **🟢 Régimen General:**
- ✅ Registro de Compras
- ✅ Registro de Ventas
- ✅ Libro Diario
- ✅ Libro Mayor
- ✅ Libro de Inventarios y Balances
- ✅ Libro Caja y Bancos (si aplica)

#### **🟡 Régimen MYPE Tributario:**
- ✅ Registro de Compras
- ✅ Registro de Ventas
- ✅ Libro Diario Simplificado

#### **🔵 Régimen Especial (RER):**
- ✅ Registro de Compras
- ✅ Registro de Ventas

### **📊 Libros Societarios:**
- **Libro de Actas** de Junta General
- **Libro de Actas** del Directorio
- **Libro de Matrícula** de Acciones
- **Libro de Transferencias** de Acciones

### **⏰ Plazos de Atraso Máximo:**
- **Régimen General:** 3 meses
- **MYPE:** 10 meses
- **RER:** 10 meses

### **💰 Multas por Atraso:**
- **0.6% UIT** por cada mes de atraso
- **Cierre temporal** en casos graves
- **Pérdida de beneficios** tributarios

### **📱 Llevado Electrónico:**
- **PLE SUNAT** para la mayoría
- **Sistemas contables** certificados
- **Validación mensual** obligatoria

**¿Necesitas ayuda con algún libro específico?**"""

    def _general_regulatory_help(self) -> str:
        """Ayuda general sobre normativa"""
        return """## **⚖️ Normativa Contable Peruana**

### **📋 Principales Normas:**

#### **🏛️ Marco Regulatorio:**
- **CNC:** Consejo Normativo de Contabilidad
- **SUNAT:** Superintendencia Nacional de Aduanas
- **SMV:** Superintendencia del Mercado de Valores

#### **📚 Normas Principales:**
- **PCGE 2019:** Plan Contable General
- **NIIF:** Normas Internacionales
- **Ley del IGV:** Decreto Legislativo 821
- **Ley del Impuesto a la Renta:** TUO

### **📊 Áreas de Consulta:**
- **Contabilidad:** PCGE, NIIF, registros
- **Tributaria:** IGV, Renta, libros
- **Laboral:** Planillas, CTS, gratificaciones
- **Societaria:** Constitución, órganos

### **💡 Ejemplos de Consultas:**
- *"¿Cuáles son las cuentas del PCGE para inventarios?"*
- *"¿Qué libros debo llevar en Régimen General?"*
- *"¿Cómo aplicar NIIF 16 en arrendamientos?"*
- *"¿Cuáles son las multas por atraso en libros?"*

**¿Sobre qué normativa específica necesitas información?**"""

# Instancia global
regulatory_service = RegulatoryService()