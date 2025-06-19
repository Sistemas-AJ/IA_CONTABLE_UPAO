"""
Analizador especializado en conceptos y educación contable
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import re

@dataclass
class ConceptInfo:
    """Estructura para un concepto contable"""
    name: str
    definition: str
    examples: List[str]
    differences: Optional[Dict[str, str]] = None
    related_terms: Optional[List[str]] = None

class EducationalAnalyzer:
    """Analizador para consultas educativas y explicaciones contables"""

    def __init__(self):
        self.concepts = self._load_concepts()

    def _load_concepts(self) -> Dict[str, ConceptInfo]:
        """Carga conceptos contables básicos"""
        return {
            "activo": ConceptInfo(
                name="Activo",
                definition="Recurso controlado por la empresa, del que se espera obtener beneficios económicos futuros.",
                examples=["Caja y Bancos", "Cuentas por cobrar", "Inventarios", "Maquinaria"],
                related_terms=["pasivo", "patrimonio"]
            ),
            "pasivo": ConceptInfo(
                name="Pasivo",
                definition="Obligaciones presentes de la empresa, surgidas a raíz de eventos pasados, cuyo pago se espera que resulte en una salida de recursos.",
                examples=["Cuentas por pagar", "Préstamos bancarios", "Proveedores"],
                related_terms=["activo", "patrimonio"]
            ),
            "patrimonio": ConceptInfo(
                name="Patrimonio",
                definition="Interés residual en los activos de la empresa, después de deducir todos sus pasivos.",
                examples=["Capital social", "Reservas", "Resultados acumulados"],
                related_terms=["activo", "pasivo"]
            ),
            "debe": ConceptInfo(
                name="Debe",
                definition="Columna del asiento contable donde se registran los aumentos de activos y gastos, y las disminuciones de pasivos y patrimonio.",
                examples=["Compra de mercadería: Debe a Mercaderías"],
                related_terms=["haber"]
            ),
            "haber": ConceptInfo(
                name="Haber",
                definition="Columna del asiento contable donde se registran los aumentos de pasivos, patrimonio e ingresos, y las disminuciones de activos y gastos.",
                examples=["Venta de mercadería: Haber a Ventas"],
                related_terms=["debe"]
            ),
            "ingreso": ConceptInfo(
                name="Ingreso",
                definition="Incremento de los beneficios económicos durante el periodo contable en forma de entradas o aumentos de activos o disminuciones de pasivos.",
                examples=["Ventas de mercaderías", "Prestación de servicios"],
                related_terms=["gasto", "utilidad"]
            ),
            "gasto": ConceptInfo(
                name="Gasto",
                definition="Disminución de los beneficios económicos durante el periodo contable en forma de salidas o disminuciones de activos o aumentos de pasivos.",
                examples=["Pago de sueldos", "Compra de suministros", "Gastos de alquiler"],
                related_terms=["ingreso", "pérdida"]
            ),
            "utilidad": ConceptInfo(
                name="Utilidad",
                definition="Exceso de los ingresos sobre los gastos en un periodo contable.",
                examples=["Utilidad neta del ejercicio", "Utilidad operativa"],
                related_terms=["pérdida", "ingreso", "gasto"]
            ),
            "pérdida": ConceptInfo(
                name="Pérdida",
                definition="Exceso de los gastos sobre los ingresos en un periodo contable.",
                examples=["Pérdida neta del ejercicio"],
                related_terms=["utilidad", "gasto"]
            ),
            "balance general": ConceptInfo(
                name="Balance General",
                definition="Estado financiero que muestra la situación económica y financiera de una empresa en un momento determinado.",
                examples=["Balance general al 31 de diciembre de 2024"],
                related_terms=["estado de resultados", "activo", "pasivo", "patrimonio"]
            ),
            "estado de resultados": ConceptInfo(
                name="Estado de Resultados",
                definition="Estado financiero que muestra el resultado de las operaciones de una empresa durante un periodo determinado.",
                examples=["Estado de resultados del año 2024"],
                related_terms=["balance general", "ingreso", "gasto", "utilidad"]
            ),
            "asiento contable": ConceptInfo(
                name="Asiento Contable",
                definition="Registro de una transacción económica en los libros contables, siguiendo la partida doble.",
                examples=["Compra de mercadería al contado", "Pago de sueldos"],
                related_terms=["debe", "haber", "libro diario"]
            ),
            "libro diario": ConceptInfo(
                name="Libro Diario",
                definition="Libro contable donde se registran cronológicamente todas las operaciones de la empresa.",
                examples=["Registro de compras y ventas diarias"],
                related_terms=["asiento contable", "libro mayor"]
            ),
            "libro mayor": ConceptInfo(
                name="Libro Mayor",
                definition="Libro contable donde se agrupan los movimientos de cada cuenta para determinar su saldo.",
                examples=["Cuenta 10 Caja y Bancos en el libro mayor"],
                related_terms=["libro diario", "asiento contable"]
            ),
            "partida doble": ConceptInfo(
                name="Partida Doble",
                definition="Principio contable según el cual, a todo cargo corresponde un abono de igual valor.",
                examples=["Compra de mercadería: Debe a Mercaderías, Haber a Caja"],
                related_terms=["debe", "haber", "asiento contable"]
            ),
            "periodo contable": ConceptInfo(
                name="Periodo Contable",
                definition="Intervalo de tiempo al que se refieren los estados financieros de una empresa, generalmente un año.",
                examples=["Ejercicio 2024", "Trimestre enero-marzo 2025"],
                related_terms=["estado financiero", "balance general"]
            ),
            "devengo": ConceptInfo(
                name="Devengo",
                definition="Principio contable que establece que las transacciones deben reconocerse cuando ocurren, independientemente de cuándo se cobren o paguen.",
                examples=["Reconocimiento de ingresos por ventas a crédito"],
                related_terms=["realización", "ingreso", "gasto"]
            ),
            "realización": ConceptInfo(
                name="Realización",
                definition="Principio contable que indica que los ingresos y gastos deben reconocerse cuando se han realizado, es decir, cuando se ha producido el hecho económico.",
                examples=["Venta de un producto entregado al cliente"],
                related_terms=["devengo", "ingreso"]
            ),
            "flujo de efectivo": ConceptInfo(
                name="Flujo de Efectivo",
                definition="Movimiento de entrada y salida de dinero en efectivo en una empresa durante un periodo.",
                examples=["Cobro de ventas", "Pago a proveedores"],
                related_terms=["estado de flujo de efectivo", "liquidez"]
            ),
            "estado de flujo de efectivo": ConceptInfo(
                name="Estado de Flujo de Efectivo",
                definition="Estado financiero que muestra las entradas y salidas de efectivo de una empresa durante un periodo.",
                examples=["Estado de flujo de efectivo del año 2024"],
                related_terms=["flujo de efectivo", "balance general"]
            ),
            "pasivo corriente": ConceptInfo(
                name="Pasivo Corriente",
                definition="Obligaciones que la empresa debe pagar en el corto plazo, generalmente dentro de un año.",
                examples=["Proveedores", "Préstamos bancarios a corto plazo"],
                related_terms=["pasivo no corriente", "activo corriente"]
            ),
            "pasivo no corriente": ConceptInfo(
                name="Pasivo No Corriente",
                definition="Obligaciones que la empresa debe pagar en el largo plazo, es decir, después de un año.",
                examples=["Préstamos bancarios a largo plazo", "Bonos emitidos"],
                related_terms=["pasivo corriente", "activo no corriente"]
            ),
            "activo corriente": ConceptInfo(
                name="Activo Corriente",
                definition="Bienes y derechos que se espera convertir en efectivo o consumir en el ciclo normal de operaciones, generalmente dentro de un año.",
                examples=["Caja y Bancos", "Cuentas por cobrar", "Inventarios"],
                related_terms=["activo no corriente", "pasivo corriente"]
            ),
            "activo no corriente": ConceptInfo(
                name="Activo No Corriente",
                definition="Bienes y derechos que no se espera convertir en efectivo o consumir en el ciclo normal de operaciones, es decir, después de un año.",
                examples=["Propiedades, planta y equipo", "Inversiones a largo plazo"],
                related_terms=["activo corriente", "pasivo no corriente"]
            ),
            "capital social": ConceptInfo(
                name="Capital Social",
                definition="Aportes realizados por los socios o accionistas a la empresa, representando la propiedad de la misma.",
                examples=["Aportes iniciales de los socios", "Emisión de acciones"],
                related_terms=["patrimonio", "reserva legal"]
            ),
            "reserva legal": ConceptInfo(
                name="Reserva Legal",
                definition="Porción de las utilidades que la ley obliga a las empresas a retener para fortalecer su patrimonio.",
                examples=["Reserva legal constituida con el 10% de la utilidad neta"],
                related_terms=["patrimonio", "capital social"]
            ),
            "provisión": ConceptInfo(
                name="Provisión",
                definition="Reconocimiento contable de una obligación probable, cuyo importe o fecha de pago es incierto.",
                examples=["Provisión para cuentas incobrables", "Provisión para litigios"],
                related_terms=["pasivo", "estimación"]
            ),
            "amortización": ConceptInfo(
                name="Amortización",
                definition="Distribución sistemática del costo de un activo intangible a lo largo de su vida útil.",
                examples=["Amortización de una patente", "Amortización de gastos de organización"],
                related_terms=["depreciación", "activo intangible"]
            ),
            "depreciación": ConceptInfo(
                name="Depreciación",
                definition="Distribución sistemática del costo de un activo tangible a lo largo de su vida útil.",
                examples=["Depreciación de maquinaria", "Depreciación de edificios"],
                related_terms=["amortización", "activo fijo"]
            ),
            "activo intangible": ConceptInfo(
                name="Activo Intangible",
                definition="Activo no monetario identificable, sin apariencia física, que genera beneficios económicos futuros.",
                examples=["Marcas", "Patentes", "Derechos de autor"],
                related_terms=["amortización", "activo no corriente"]
            ),
            "activo fijo": ConceptInfo(
                name="Activo Fijo",
                definition="Bien tangible utilizado en la producción o suministro de bienes y servicios, con vida útil superior a un año.",
                examples=["Maquinaria", "Edificios", "Vehículos"],
                related_terms=["depreciación", "activo no corriente"]
            ),
            "costo de ventas": ConceptInfo(
                name="Costo de Ventas",
                definition="Costo directo de los bienes vendidos o servicios prestados durante un periodo.",
                examples=["Costo de mercaderías vendidas", "Costo de servicios prestados"],
                related_terms=["ingreso", "utilidad bruta"]
            ),
            "utilidad bruta": ConceptInfo(
                name="Utilidad Bruta",
                definition="Diferencia entre los ingresos por ventas y el costo de ventas.",
                examples=["Ventas S/ 10,000 - Costo de ventas S/ 7,000 = Utilidad bruta S/ 3,000"],
                related_terms=["utilidad operativa", "costo de ventas"]
            ),
            "utilidad operativa": ConceptInfo(
                name="Utilidad Operativa",
                definition="Resultado de restar los gastos operativos a la utilidad bruta.",
                examples=["Utilidad bruta S/ 3,000 - Gastos operativos S/ 1,000 = Utilidad operativa S/ 2,000"],
                related_terms=["utilidad bruta", "utilidad neta"]
            ),
            "utilidad neta": ConceptInfo(
                name="Utilidad Neta",
                definition="Resultado final después de deducir todos los gastos, incluidos los impuestos, de los ingresos totales.",
                examples=["Utilidad operativa S/ 2,000 - Impuestos S/ 400 = Utilidad neta S/ 1,600"],
                related_terms=["utilidad operativa", "utilidad bruta"]
            ),
            "cts": ConceptInfo(
                name="CTS (Compensación por Tiempo de Servicios)",
                definition="La CTS es un beneficio social que otorgan los empleadores a sus trabajadores en planilla, con el objetivo de protegerlos ante el cese laboral. Consiste en un depósito semestral equivalente a una fracción del sueldo, más asignaciones y otros conceptos.",
                examples=[
                    "Depósito de CTS en mayo y noviembre",
                    "Cálculo de CTS para un sueldo de S/ 3,000"
                ],
                related_terms=["beneficio social", "gratificación", "vacaciones"]
            ),
            "gratificación": ConceptInfo(
                name="Gratificación",
                definition="Beneficio social que consiste en el pago adicional al trabajador en julio y diciembre, equivalente a una remuneración mensual.",
                examples=[
                    "Gratificación de Fiestas Patrias",
                    "Gratificación de Navidad"
                ],
                related_terms=["cts", "vacaciones", "beneficio social"]
            ),
            "vacaciones": ConceptInfo(
                name="Vacaciones",
                definition="Derecho laboral que consiste en el descanso remunerado de 30 días calendario por cada año completo de servicios.",
                examples=[
                    "Vacaciones anuales de un trabajador",
                    "Pago de vacaciones truncas"
                ],
                related_terms=["cts", "gratificación", "beneficio social"]
            ),
            "igv": ConceptInfo(
                name="IGV (Impuesto General a las Ventas)",
                definition="Impuesto indirecto que grava la venta de bienes, prestación de servicios y contratos de construcción en el Perú. La tasa general es 18%.",
                examples=[
                    "IGV en la venta de mercaderías",
                    "Cálculo de IGV en una factura"
                ],
                related_terms=["impuesto", "renta", "detracción"]
            ),
            "renta": ConceptInfo(
                name="Impuesto a la Renta",
                definition="Impuesto directo que grava las rentas obtenidas por personas naturales y jurídicas, según las categorías establecidas por la ley.",
                examples=[
                    "Impuesto a la renta de quinta categoría",
                    "Impuesto a la renta de tercera categoría"
                ],
                related_terms=["igv", "tributo", "detracción"]
            ),
            "detracción": ConceptInfo(
                name="Detracción",
                definition="Sistema de pago anticipado de impuestos en el Perú, donde una parte del importe de la operación es depositada en una cuenta del Banco de la Nación a nombre del proveedor.",
                examples=[
                    "Detracción en servicios de transporte",
                    "Detracción en venta de bienes"
                ],
                related_terms=["igv", "percepción", "retención"]
            ),
            "percepción": ConceptInfo(
                name="Percepción",
                definition="Mecanismo de recaudación anticipada del IGV, aplicado en la importación y comercialización de determinados bienes.",
                examples=[
                    "Percepción en importación de bienes",
                    "Percepción en venta de combustibles"
                ],
                related_terms=["igv", "detracción", "retención"]
            ),
            "retención": ConceptInfo(
                name="Retención",
                definition="Mecanismo de recaudación anticipada del IGV, donde el comprador retiene un porcentaje del pago al proveedor y lo deposita a la SUNAT.",
                examples=[
                    "Retención en servicios de terceros",
                    "Retención en contratos de locación"
                ],
                related_terms=["igv", "detracción", "percepción"]
            ),
            # Puedes seguir agregando más conceptos según necesidad...
        }

    def explain_concept(self, term: str) -> Optional[ConceptInfo]:
        key = term.lower().strip()
        # 1. Coincidencia exacta
        if key in self.concepts:
            return self.concepts[key]
        # 2. Buscar por substring (más flexible)
        for concept_key in self.concepts:
            if concept_key in key or key in concept_key:
                return self.concepts[concept_key]
        # 3. Extraer palabra clave de la pregunta (ej: "que es el cts" -> "cts")
        import re
        match = re.search(r"(qué|que)\s+es\s+(el|la|los|las)?\s*([a-zA-Z0-9\s]+)", key)
        if match:
            concept_candidate = match.group(3).strip()
            # Eliminar artículos y preposiciones comunes
            concept_candidate = re.sub(r"\b(el|la|los|las|de|del|un|una|en|por|para|a|y|o|es|son)\b", "", concept_candidate).strip()
            for concept_key in self.concepts:
                if concept_candidate == concept_key or concept_candidate in concept_key or concept_key in concept_candidate:
                    return self.concepts[concept_key]
        # 4. Buscar por palabras clave dentro de la frase
        for concept_key in self.concepts:
            if any(word in key for word in concept_key.split()):
                return self.concepts[concept_key]
        # 5. Último recurso: usar la última palabra relevante
        palabras = [w for w in key.split() if len(w) > 2]
        if palabras:
            posible = palabras[-1]
            for concept_key in self.concepts:
                if posible == concept_key or posible in concept_key:
                    return self.concepts[concept_key]
        return None

    def list_concepts(self) -> List[str]:
        """Lista los conceptos disponibles"""
        return list(self.concepts.keys())

    def compare_terms(self, term1: str, term2: str) -> Optional[str]:
        """Explica la diferencia entre dos términos"""
        c1 = self.concepts.get(term1.lower())
        c2 = self.concepts.get(term2.lower())
        if c1 and c2:
            return (
                f"**{c1.name}:** {c1.definition}\n\n"
                f"**{c2.name}:** {c2.definition}\n\n"
                f"**Diferencia principal:**\n"
                f"- {c1.name} se refiere a ...\n"
                f"- {c2.name} se refiere a ..."
            )
        return None

    def get_example(self, term: str) -> Optional[List[str]]:
        """Devuelve ejemplos de un concepto"""
        c = self.concepts.get(term.lower())
        return c.examples if c else None

# Instancia global
educational_analyzer = EducationalAnalyzer()