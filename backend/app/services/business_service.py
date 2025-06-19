"""
Servicio especializado en constitución de empresas y negocios
"""
import logging
import re
from typing import Dict

logger = logging.getLogger(__name__)

class BusinessService:
    """Servicio especializado en constitución y gestión empresarial"""
    
    async def generate_response(self, query: str, context: Dict, metadata: Dict) -> str:
        """Genera respuesta sobre constitución y negocios"""
        query_lower = query.lower()
        
        if "constituir" in query_lower or "constitucion" in query_lower:
            return self._constitution_process()
        elif "tipo" in query_lower and ("empresa" in query_lower or "sociedad" in query_lower):
            return self._business_types()
        elif "capital" in query_lower and ("minimo" in query_lower or "social" in query_lower):
            return self._minimum_capital()
        else:
            return self._general_business_help()
    
    def _constitution_process(self) -> str:
        """Proceso de constitución de empresas"""
        return """## **🏢 Constitución de Empresas en Perú**

### **📋 Pasos para Constituir una Empresa:**

#### **1️⃣ Búsqueda y Reserva de Nombre**
- **SUNARP** - Búsqueda en registros públicos
- **Reserva:** 30 días hábiles
- **Costo:** S/ 18.00

#### **2️⃣ Elaboración de Minuta**
- **Notario** - Redacción del acto constitutivo
- **Incluye:** Estatutos, capital social, socios
- **Costo:** S/ 300 - S/ 500

#### **3️⃣ Escritura Pública**
- **Notario** - Elevación a escritura pública
- **Firmas** de todos los socios
- **Costo:** S/ 200 - S/ 400

#### **4️⃣ Inscripción en SUNARP**
- **Registro Mercantil**
- **Plazo:** 7-15 días hábiles
- **Costo:** S/ 40 - S/ 120

#### **5️⃣ RUC en SUNAT**
- **Obtención de RUC** empresarial
- **Régimen tributario**
- **Gratuito**

### **💰 Costos Aproximados:**
- **SAC:** S/ 800 - S/ 1,500
- **EIRL:** S/ 600 - S/ 1,200
- **SRL:** S/ 1,000 - S/ 2,000

**¿Necesitas información específica sobre algún tipo de empresa?**"""

    def _business_types(self) -> str:
        """Tipos de empresas en Perú"""
        return """## **🏢 Tipos de Empresas en Perú**

### **🔹 Sociedad Anónima Cerrada (SAC)**
- **Socios:** 2 a 20 accionistas
- **Capital mínimo:** No hay mínimo legal
- **Responsabilidad:** Limitada al capital aportado
- **Gestión:** Directorio opcional

### **🔸 Empresa Individual de Responsabilidad Limitada (EIRL)**
- **Titulares:** 1 persona natural
- **Capital mínimo:** No hay mínimo legal
- **Responsabilidad:** Limitada al patrimonio empresarial
- **Gestión:** Gerente general

### **🔹 Sociedad de Responsabilidad Limitada (SRL)**
- **Socios:** 2 a 20 participacionistas
- **Capital mínimo:** No hay mínimo legal
- **Responsabilidad:** Limitada a participaciones
- **Gestión:** Gerencia obligatoria

### **🔸 Sociedad Anónima (SA)**
- **Accionistas:** Mínimo 2, sin máximo
- **Capital mínimo:** No hay mínimo legal
- **Responsabilidad:** Limitada al capital
- **Gestión:** Directorio obligatorio

### **📊 Comparativa Rápida:**

| Tipo | Socios | Capital | Órganos |
|------|--------|---------|----------|
| **SAC** | 2-20 | Libre | Junta/Gerencia |
| **EIRL** | 1 | Libre | Gerencia |
| **SRL** | 2-20 | Libre | Junta/Gerencia |
| **SA** | 2+ | Libre | Junta/Directorio |

**¿Qué tipo se adapta mejor a tu proyecto?**"""

    def _minimum_capital(self) -> str:
        """Capital mínimo para empresas"""
        return """## **💰 Capital Social en Empresas Peruanas**

### **⚖️ Marco Legal:**
- **Nueva Ley General de Sociedades** (2021)
- **No existe capital mínimo** legal obligatorio
- **Capital simbólico:** Desde S/ 1.00

### **💡 Recomendaciones Prácticas:**

#### **🔹 SAC - Pequeña Empresa:**
- **Recomendado:** S/ 5,000 - S/ 20,000
- **Para:** Servicios profesionales, comercio menor

#### **🔸 EIRL - Emprendimiento:**
- **Recomendado:** S/ 2,000 - S/ 10,000
- **Para:** Actividad personal, freelance

#### **🔹 SRL - Negocio Familiar:**
- **Recomendado:** S/ 10,000 - S/ 50,000
- **Para:** Comercio, servicios

#### **🔸 SA - Empresa Grande:**
- **Recomendado:** S/ 50,000+
- **Para:** Industria, gran comercio

### **📋 Consideraciones:**
- **Credibilidad** ante proveedores
- **Capacidad operativa** inicial
- **Respaldo** para créditos
- **Gastos** de constitución

### **📊 Estructura del Capital:**
```
Capital Social = Aportes en Efectivo + Bienes + Servicios
```

**¿Necesitas ayuda para calcular el capital de tu empresa?**"""

    def _general_business_help(self) -> str:
        """Ayuda general sobre negocios"""
        return """## **🏢 Asesoría Empresarial**

### **📋 Servicios Disponibles:**

#### **🎯 Constitución:**
- Tipos de empresas
- Procesos y requisitos
- Costos y tiempos

#### **💰 Capital Social:**
- Montos recomendados
- Formas de aporte
- Aumentos de capital

#### **⚖️ Aspectos Legales:**
- Estatutos sociales
- Órganos de gobierno
- Responsabilidades

#### **📊 Contabilidad:**
- Libros obligatorios
- Regímenes tributarios
- Estados financieros

### **💬 Ejemplos de Consultas:**
- *"¿Cómo constituir una SAC?"*
- *"¿Cuál es el capital mínimo?"*
- *"¿Qué tipo de empresa me conviene?"*
- *"¿Cuáles son los costos de constitución?"*

**¿En qué aspecto empresarial necesitas asesoría?**"""

def extract_concept_from_query(query: str) -> str:
    # Busca patrones como "qué es el/la/los/las <concepto>"
    match = re.search(r"(qué|que) es (el|la|los|las)?\s*([a-zA-Z0-9\s]+)", query.lower())
    if match:
        return match.group(3).strip()
    return query.strip()

# Instancia global
business_service = BusinessService()