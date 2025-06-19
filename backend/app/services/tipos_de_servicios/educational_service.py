import logging
from typing import Dict, List
from .asientos_contables import asientos_contables
from .ai_service import ai_service  # Asegúrate de tener este import

logger = logging.getLogger(__name__)

class EducationalService:
    """Servicio avanzado para educación contable profesional"""
    
    def __init__(self):
        # Base de conocimientos contables expandida y profesional
        self.conceptos = {
            "asiento_contable": {
                "definicion": "Un asiento contable es un registro en los libros contables de una empresa que refleja una transacción económica. Este registro se realiza siguiendo el principio de partida doble, donde cada transacción afecta al menos dos cuentas: una cuenta se debita y otra se acredita, manteniendo siempre el equilibrio contable.",
                "caracteristicas": [
                    "Fecha: Indica el momento en que se realiza la transacción",
                    "Cuentas Afectadas: Se especifican las cuentas que se debitan y acreditan",
                    "Importe: Monto de la transacción, que debe ser igual en el debe y el haber",
                    "Descripción: Breve explicación de la naturaleza de la transacción",
                    "Número de Asiento: Un identificador único para cada asiento, que facilita su seguimiento"
                ],
                "estructura": {
                    "Encabezado": "Fecha, número de asiento, descripción",
                    "Cuerpo": "Cuentas deudoras (DEBE) y cuentas acreedoras (HABER)",
                    "Importes": "Montos registrados en cada cuenta",
                    "Glosa": "Descripción breve y clara de la operación"
                },
                "principio_partida_doble": {
                    "definicion": "Por cada cargo debe existir al menos un abono equivalente",
                    "ecuacion": "DEBE = HABER"
                },
                "ejemplo_basico": {
                    "descripcion": "Compra de mercadería por S/ 1,000 al contado",
                    "tabla": [
                        ["Fecha", "Cuenta", "Debe (S/)", "Haber (S/)"],
                        ["01/10/2023", "Mercaderías", "1,000", ""],
                        ["01/10/2023", "Caja", "", "1,000"]
                    ]
                },
                "normativa_aplicable": "En el Perú, los asientos contables deben realizarse conforme a las Normas Internacionales de Información Financiera (NIIF) y el Plan Contable General Empresarial (PCGE), que establecen las directrices para la correcta contabilización de las transacciones económicas.",
                "importancia": "El cumplimiento de estas normativas asegura que la información financiera sea consistente, comparable y transparente, facilitando la toma de decisiones por parte de los usuarios internos y externos de la información contable."
            },
            
            "activo": {
                "definicion": "Recurso controlado por la empresa como resultado de eventos pasados, del cual se espera obtener beneficios económicos futuros. Debe ser identificable, controlable y generar flujos de efectivo positivos.",
                "caracteristicas": [
                    "Control económico real sobre el recurso",
                    "Resultado de transacciones o eventos pasados",
                    "Potencial de generar beneficios económicos futuros",
                    "Medible de forma fiable en términos monetarios",
                    "Transferible o separable de la entidad"
                ],
                "clasificacion": {
                    "Por Liquidez": {
                        "Activo Corriente": "Efectivo o se espera convertir en efectivo dentro de 12 meses o ciclo operativo normal",
                        "Activo No Corriente": "Se espera realizar, vender o consumir en más de 12 meses"
                    },
                    "Por Naturaleza": {
                        "Tangibles": "Tienen sustancia física (inventarios, PPE)",
                        "Intangibles": "No tienen sustancia física (marcas, patentes, software)",
                        "Financieros": "Instrumentos financieros (inversiones, depósitos)"
                    }
                },
                "reconocimiento_niif": "NIC 1, NIC 16, NIC 38, NIC 39, NIIF 9",
                "ejemplos_practicos": [
                    "Edificio corporativo S/ 500,000",
                    "Inventario de mercaderías S/ 85,000", 
                    "Cuentas por cobrar clientes S/ 125,000",
                    "Marca registrada S/ 75,000",
                    "Efectivo en bancos S/ 45,000"
                ]
            },
            
            "pasivo": {
                "definicion": "Obligación presente de la empresa, surgida como resultado de eventos pasados, cuya liquidación se espera que dé lugar a una salida de recursos que incorporen beneficios económicos.",
                "caracteristicas": [
                    "Obligación presente de la empresa",
                    "Resultado de eventos pasados",
                    "Liquidación probable mediante salida de recursos",
                    "Cuantía determinable de forma fiable",
                    "No discrecional para la empresa"
                ],
                "clasificacion": {
                    "Por Vencimiento": {
                        "Corriente": "Vence dentro de 12 meses o ciclo operativo",
                        "No Corriente": "Vence en más de 12 meses"
                    },
                    "Por Naturaleza": {
                        "Comerciales": "Proveedores, facturas por pagar",
                        "Laborales": "Sueldos, beneficios, aportes sociales",
                        "Tributarias": "IGV, IR, contribuciones",
                        "Financieras": "Préstamos, sobregiros, bonos"
                    }
                },
                "reconocimiento_niif": "NIC 1, NIC 19, NIC 37, NIIF 9",
                "ejemplos_practicos": [
                    "Préstamo bancario S/ 200,000",
                    "Proveedores S/ 65,000",
                    "Sueldos por pagar S/ 28,000",
                    "IGV por pagar S/ 15,000",
                    "Provisión garantías S/ 12,000"
                ]
            },
            
            "patrimonio": {
                "definicion": "Participación residual en los activos de la empresa, después de deducir todos sus pasivos. Representa la inversión de los propietarios en la empresa.",
                "caracteristicas": [
                    "Residual (Activo - Pasivo = Patrimonio)",
                    "Pertenece a los propietarios/accionistas",
                    "Puede aumentar o disminuir según resultados",
                    "Base para distribución de dividendos",
                    "Respaldo patrimonial de la empresa"
                ],
                "componentes": {
                    "Capital Social": "Aportes de los socios o accionistas",
                    "Reservas": "Utilidades retenidas para fines específicos",
                    "Resultados Acumulados": "Utilidades o pérdidas no distribuidas",
                    "Ajustes por Revaluación": "Incrementos por revaluación de activos"
                },
                "formulas": {
                    "Ecuación Básica": "Patrimonio = Activo - Pasivo",
                    "Variación": "ΔPatrimonio = Utilidad/Pérdida + Aportes - Retiros"
                }
            },
            
            "gasto": {
                "definicion": "Disminución en los beneficios económicos durante el período contable, en forma de salidas de recursos que resultan en disminuciones del patrimonio.",
                "caracteristicas": [
                    "Disminuye el patrimonio",
                    "No genera activos",
                    "Se reconoce por devengado",
                    "Afecta el resultado del período",
                    "Requiere sustento documental"
                ],
                "clasificacion": {
                    "Por Función": {
                        "Gastos de Administración": "Gastos generales de gestión",
                        "Gastos de Ventas": "Relacionados con comercialización",
                        "Gastos Financieros": "Intereses, comisiones bancarias"
                    },
                    "Por Naturaleza": {
                        "Gastos de Personal": "Sueldos, beneficios sociales",
                        "Servicios de Terceros": "Honorarios, servicios públicos",
                        "Tributos": "Impuestos, contribuciones"
                    }
                }
            },
            
            "costo": {
                "definicion": "Sacrificio económico que se incorpora al valor de un bien o servicio para su producción, y se recupera cuando se vende el producto.",
                "caracteristicas": [
                    "Se incorpora al producto",
                    "Es inventariable",
                    "Se recupera con la venta",
                    "Forma parte del activo",
                    "Afecta resultado cuando se vende"
                ],
                "tipos": {
                    "Costos Directos": "Materiales directos, mano de obra directa",
                    "Costos Indirectos": "Gastos generales de fabricación",
                    "Costos Fijos": "No varían con el volumen",
                    "Costos Variables": "Varían proporcionalmente con el volumen"
                }
            },
            
            "depreciacion": {
                "definicion": "Distribución sistemática del costo de un activo durante su vida útil, reconociendo la pérdida de valor por uso, obsolescencia o paso del tiempo.",
                "metodos": {
                    "Línea Recta": "(Costo - Valor Residual) / Vida Útil",
                    "Unidades Producidas": "(Costo - Valor Residual) × (Uso Período / Uso Total)",
                    "Doble Saldo Decreciente": "Valor Libros × (2 / Vida Útil)"
                },
                "formulas": {
                    "Depreciación Anual": "(Costo - Valor Residual) / Años Vida Útil",
                    "Valor en Libros": "Costo - Depreciación Acumulada"
                }
            },
            
            "igv": {
                "definicion": "Impuesto General a las Ventas, tributo que grava las operaciones de venta de bienes, prestación de servicios e importaciones en el Perú.",
                "tasa": "18% (16% IGV + 2% IPM)",
                "formulas": {
                    "IGV a Pagar": "IGV Ventas - IGV Compras",
                    "Precio con IGV": "Precio sin IGV × 1.18",
                    "Precio sin IGV": "Precio con IGV / 1.18",
                    "Solo IGV": "Precio con IGV × 0.152542"
                },
                "tratamiento": {
                    "Ventas": "Se cobra al cliente (débito fiscal)",
                    "Compras": "Se paga al proveedor (crédito fiscal)",
                    "Liquidación": "Diferencia entre débito y crédito fiscal"
                }
            },
            
            "roe": {
                "definicion": "Return on Equity - Rentabilidad sobre el patrimonio, mide la capacidad de la empresa para generar beneficios con el capital aportado por los accionistas.",
                "formula": "ROE = Utilidad Neta / Patrimonio Promedio × 100",
                "interpretacion": {
                    "Alto ROE": "Mayor de 15% - Excelente rentabilidad",
                    "ROE Moderado": "10%-15% - Rentabilidad aceptable",
                    "Bajo ROE": "Menor de 10% - Revisar eficiencia"
                },
                "factores": [
                    "Margen de utilidad neta",
                    "Rotación de activos",
                    "Apalancamiento financiero"
                ]
            },
            
            "roa": {
                "definicion": "Return on Assets - Rentabilidad sobre activos, mide la eficiencia de la empresa en el uso de sus activos para generar utilidades.",
                "formula": "ROA = Utilidad Neta / Activos Totales Promedio × 100",
                "interpretacion": {
                    "Alto ROA": "Mayor de 8% - Uso eficiente de activos",
                    "ROA Moderado": "4%-8% - Eficiencia aceptable",
                    "Bajo ROA": "Menor de 4% - Revisar gestión de activos"
                }
            },
            
            "ratio": {
                "definicion": "Un ratio financiero es una relación matemática entre dos partidas de los estados financieros que permite analizar la situación económica y financiera de una empresa. Los ratios ayudan a comparar, interpretar y tomar decisiones sobre la gestión y desempeño de la organización.",
                "caracteristicas": [
                    "Permiten comparar empresas de distinto tamaño",
                    "Facilitan el análisis de tendencias en el tiempo",
                    "Se clasifican en ratios de liquidez, rentabilidad, endeudamiento y gestión",
                    "Son herramientas clave para la toma de decisiones financieras"
                ],
                "tipos": {
                    "Ratios de Liquidez": "Miden la capacidad de la empresa para cumplir sus obligaciones a corto plazo (ejemplo: ratio corriente)",
                    "Ratios de Rentabilidad": "Evalúan la capacidad de generar utilidades (ejemplo: ROE, ROA, margen neto)",
                    "Ratios de Endeudamiento": "Analizan el nivel de deuda respecto al patrimonio o activos (ejemplo: ratio de endeudamiento)",
                    "Ratios de Gestión": "Miden la eficiencia operativa (ejemplo: rotación de inventarios, rotación de cuentas por cobrar)"
                },
                "ejemplos_practicos": [
                    "Ratio Corriente = Activo Corriente / Pasivo Corriente. Ejemplo: Si Activo Corriente = S/ 50,000 y Pasivo Corriente = S/ 25,000, entonces Ratio Corriente = 2.0",
                    "ROE = Utilidad Neta / Patrimonio Promedio. Ejemplo: Utilidad Neta S/ 10,000 y Patrimonio Promedio S/ 50,000, entonces ROE = 20%",
                    "Rotación de Inventarios = Costo de Ventas / Inventario Promedio. Ejemplo: Costo de Ventas S/ 120,000 e Inventario Promedio S/ 30,000, entonces Rotación = 4 veces"
                ]
            }
        }
        
        # Lista expandida de conceptos contables conocidos
        self.conceptos_contables_conocidos = [
            # Básicos
            "activo", "pasivo", "patrimonio", "ingreso", "gasto", "costo",
            "capital", "reserva", "utilidad", "perdida", "beneficio",
            
            # Asientos contables
            "asiento", "asiento contable", "partida doble", "debe", "haber",
            "libro diario", "libro mayor", "mayorizar", "balance", "ajuste",
            "registro contable", "transaccion", "glosa", 
            
            # Estados Financieros
            "balance", "estado resultado", "flujo efectivo", "cambios patrimonio",
            "notas estados financieros", "balance general", "pyg",
            
            # Cuentas Específicas
            "efectivo", "inventario", "cuentas cobrar", "cuentas pagar",
            "depreciacion", "amortizacion", "provision", "deuda",
            
            # Ratios y Análisis
            "ratio", "roe", "roa", "liquidez", "rentabilidad", "solvencia",
            "endeudamiento", "leverage", "margen", "rotacion",
            
            # Tributario
            "igv", "renta", "impuesto", "tributo", "sunat", "afecto", "exonerado",
            
            # Laboral
            "cts", "vacacion", "gratificacion", "planilla", "sueldo", "beneficio",
            "essalud", "afp", "onp", "sctr",
            
            # Contabilidad
            "pcge", "niif", "balance", "mayor", "auxiliar", "kardex", "registro",
            
            # Operaciones
            "compra", "venta", "prestamo", "credito", "debito", "factura",
            "boleta", "recibo", "contrato", "devengado",
            
            # Análisis Financiero
            "presupuesto", "proyeccion", "valorizacion", "flujo caja",
            "punto equilibrio", "margen contribucion", "apalancamiento",
            
            # Auditoría y Control
            "auditoria", "control interno", "riesgo", "materialidad",
            "evidencia", "procedimiento", "dictamen",
            
            # Costos
            "costo directo", "costo indirecto", "materia prima", "mano obra",
            "gastos fabricacion", "punto equilibrio", "margen contribucion",
            
            # Otros
            "ejemplo", "ejemplos", "diferencia", "formula", "calculo"
        ]

        # Diferencias entre conceptos
        self.diferencias = {
            ("gasto", "costo"): {
                "concepto1": "GASTO",
                "concepto2": "COSTO",
                "definicion1": "Sacrificio económico que no se incorpora al producto, afecta directamente el resultado del período",
                "definicion2": "Sacrificio económico que se incorpora al valor del producto, se recupera cuando se vende",
                "comparaciones": [
                    ("Incorporación al Producto", "❌ NO", "✅ SÍ"),
                    ("Inventariable", "❌ NO", "✅ SÍ"),
                    ("Recuperación", "No directa", "Con la venta"),
                    ("Estado Financiero", "Directo a ER", "Balance → ER"),
                    ("Timing", "Al incurrir", "Al vender"),
                    ("Ejemplo", "Sueldo Admin S/ 5,000", "Materia Prima S/ 10,000")
                ]
            },
            ("activo", "pasivo"): {
                "concepto1": "ACTIVO",
                "concepto2": "PASIVO", 
                "definicion1": "Recursos controlados que generan beneficios económicos futuros",
                "definicion2": "Obligaciones presentes que requieren salida de recursos",
                "comparaciones": [
                    ("Naturaleza", "Recurso/Bien", "Obligación/Deuda"),
                    ("Flujo Futuro", "Entrada de recursos", "Salida de recursos"),
                    ("Control", "Empresa controla", "Terceros reclaman"),
                    ("Ecuación", "Lado izquierdo", "Lado derecho"),
                    ("Aumento", "DEBE", "HABER"),
                    ("Ejemplo", "Efectivo S/ 50,000", "Préstamo S/ 80,000")
                ]
            },
            ("roe", "roa"): {
                "concepto1": "ROE",
                "concepto2": "ROA",
                "definicion1": "Rentabilidad sobre el patrimonio de los accionistas",
                "definicion2": "Rentabilidad sobre los activos totales de la empresa",
                "comparaciones": [
                    ("Fórmula", "Utilidad / Patrimonio", "Utilidad / Activos"),
                    ("Perspectiva", "Accionistas", "Empresa total"),
                    ("Incluye", "Efecto apalancamiento", "Solo eficiencia activos"),
                    ("Rango Bueno", "> 15%", "> 8%"),
                    ("Enfoque", "Rentabilidad capital", "Eficiencia gestión"),
                    ("Uso", "Decisiones inversión", "Gestión operativa")
                ]
            }
        }

        # Procedimientos contables paso a paso
        self.procedimientos = {
            "asiento_contable": {
                "titulo": "Proceso para Registrar un Asiento Contable",
                "pasos": [
                    {
                        "numero": "1️⃣",
                        "titulo": "Análisis de la Operación",
                        "acciones": [
                            "Identificar la transacción económica",
                            "Determinar cuentas afectadas",
                            "Clasificar según naturaleza (compra, venta, etc.)",
                            "Verificar documentación sustentadora"
                        ]
                    },
                    {
                        "numero": "2️⃣", 
                        "titulo": "Aplicación de Partida Doble",
                        "acciones": [
                            "Determinar cuentas del DEBE (débitos)",
                            "Determinar cuentas del HABER (créditos)",
                            "Asegurar que DEBE = HABER",
                            "Verificar códigos PCGE correctos"
                        ]
                    },
                    {
                        "numero": "3️⃣",
                        "titulo": "Registro Formal",
                        "acciones": [
                            "Fecha de la operación",
                            "Número correlativo del asiento",
                            "Glosa descriptiva clara y concisa",
                            "Importes en moneda funcional",
                            "Referencias documentales"
                        ]
                    },
                    {
                        "numero": "4️⃣",
                        "titulo": "Mayorización",
                        "acciones": [
                            "Traslado a cuentas del mayor",
                            "Actualización de saldos",
                            "Verificación de consistencia"
                        ]
                    }
                ],
                "ejemplo_practico": {
                    "escenario": "Compra de mercadería por S/ 5,000 + IGV, al crédito 30 días",
                    "analisis": "Transacción: Compra de mercadería, Documento: Factura F001-123, Cuentas afectadas: Mercaderías (+), IGV (+), Proveedores (+)",
                    "asiento": """
---------------------------- 18/06/2025 ----------------------------
60 COMPRAS                                    5,000.00
     601 Mercaderías
40 TRIBUTOS POR PAGAR                           900.00
     401 Gobierno central - IGV
                42 CUENTAS POR PAGAR COMERCIALES             5,900.00
                     421 Facturas por pagar
v/ Registro compra de mercadería según factura F001-123, 
   proveedor Distribuidora ABC SAC, crédito 30 días.
--------------------------------------------------------------------"""
                }
            },
            "calculo_depreciacion": {
                "titulo": "Cálculo de Depreciación Línea Recta",
                "pasos": [
                    {
                        "numero": "1️⃣",
                        "titulo": "Determinar Datos Base",
                        "acciones": [
                            "Costo de adquisición del activo",
                            "Valor residual estimado",
                            "Vida útil en años",
                            "Fecha de puesta en uso"
                        ]
                    },
                    {
                        "numero": "2️⃣",
                        "titulo": "Aplicar Fórmula",
                        "acciones": [
                            "Depreciación Anual = (Costo - Valor Residual) / Vida Útil",
                            "Depreciación Mensual = Depreciación Anual / 12",
                            "Verificar límites tributarios"
                        ]
                    },
                    {
                        "numero": "3️⃣",
                        "titulo": "Registro Contable",
                        "acciones": [
                            "DEBE: Depreciación del período",
                            "HABER: Depreciación acumulada",
                            "Glosa con referencia al activo"
                        ]
                    }
                ],
                "ejemplo_practico": {
                    "datos": "Equipo: S/ 60,000, Valor residual: S/ 6,000, Vida útil: 5 años",
                    "calculo": "Depreciación anual = (60,000 - 6,000) / 5 = S/ 10,800",
                    "asiento": """DEBE: Depreciación S/ 900 mensual
HABER: Depreciación Acumulada S/ 900"""
                }
            }
        }

        # Propósitos y utilidades
        self.propositos = {
            "asiento_contable": {
                "objetivos_fundamentales": [
                    "Documentar cronológicamente cada operación económica",
                    "Crear memoria económica de la empresa",
                    "Establecer historial verificable de transacciones",
                    "Cumplir requisitos legales y normativos"
                ],
                "beneficios_por_stakeholder": {
                    "Gerencia": ["Controlar operaciones", "Evaluar rendimiento", "Tomar decisiones", "Planificar estratégicamente"],
                    "Contadores": ["Elaborar EEFF fiables", "Cumplir normativa", "Mantener trazabilidad", "Sustentar informes"],
                    "Auditores": ["Verificar integridad", "Evaluar control interno", "Detectar inconsistencias", "Validar cumplimiento"],
                    "Inversionistas": ["Evaluar salud financiera", "Monitorear recursos", "Analizar rentabilidad", "Decidir inversiones"]
                }
            },
            "depreciacion": {
                "objetivos_fundamentales": [
                    "Distribuir el costo del activo durante su vida útil",
                    "Reconocer la pérdida de valor por uso y tiempo",
                    "Cumplir principio de asociación de ingresos y gastos",
                    "Proveer información real sobre valor de activos"
                ]
            }
        }

        # Momentos y timing
        self.timing = {
            "asiento_contable": {
                "principio_general": "Al ocurrir la transacción económica, siguiendo el principio de devengado",
                "momentos_clave": {
                    "Compras": "Al recibir la factura del proveedor",
                    "Ventas": "Al emitir la factura o boleta",
                    "Cobros y Pagos": "Al realizar o recibir el pago",
                    "Ajustes": "Final del período contable"
                },
                "consideraciones": [
                    "Principio de devengado: se registran cuando ocurren, no cuando se cobran o pagan",
                    "Corte de operaciones: definición clara de períodos contables",
                    "Períodos típicos: diario (control), mensual (impuestos), anual (EEFF oficial)"
                ]
            },
            "depreciacion": {
                "inicio": "Desde el momento que el activo está listo para su uso",
                "periodicidad": "Mensual o anual según política contable",
                "cese": "Cuando se alcanza el valor residual o se vende el activo"
            }
        }
    
    async def generate_response(self, query: str, context: Dict, metadata: Dict) -> str:
        """Genera respuesta educativa avanzada o delega a IA si no es concepto conocido"""
        query_lower = query.lower().strip()
        
        # ✅ VERIFICAR SI ES CONCEPTO CONTABLE
        if self._is_accounting_concept(query_lower):
            
            # 🔑 PRIORIDAD: PREGUNTAS EDUCATIVAS ("¿QUÉ ES...?")
            if "qué es" in query_lower or "que es" in query_lower:
                return self._explain_specific_concept(query_lower)
            elif "diferencia" in query_lower:
                return self._explain_differences(query_lower)
            elif "formula" in query_lower or "fórmula" in query_lower or "calculo" in query_lower:
                return self._explain_formulas(query_lower)
            elif "como se" in query_lower or "cómo se" in query_lower:
                return self._explain_procedures(query_lower)
            elif "para que" in query_lower or "para qué" in query_lower:
                return self._explain_purpose(query_lower)
            elif "cuando" in query_lower or "cuándo" in query_lower:
                return self._explain_timing(query_lower)
            
            # 🆕 SOLO SI NO ES EDUCATIVO, DELEGAR ASIENTOS CONTABLES AL SERVICIO ESPECIALIZADO
            elif asientos_contables.is_accounting_query(query):
                return await asientos_contables.generate_response(query, context, metadata)
            
            else:
                # Si no encuentra nada específico, intenta con IA
                ia_response = await ai_service.ask_ai(query, context, metadata)
                if ia_response:
                    return ia_response
                return self._generate_educational_help()
        else:
            # ❌ NO ES CONCEPTO CONTABLE - USAR IA
            logger.info(f"🤖 Pregunta general detectada: '{query}' - Enviando a IA")
            ia_response = await ai_service.ask_ai(query, context, metadata)
            if ia_response:
                return ia_response
            return self._generate_educational_help()

    def _is_accounting_concept(self, query: str) -> bool:
        """Verifica si la pregunta es sobre un concepto contable específico"""
        # Buscar palabras clave contables en la consulta
        for concepto in self.conceptos_contables_conocidos:
            if concepto in query:
                return True
        
        return False
    
    def _explain_specific_concept(self, query: str) -> str:
        """Explica un concepto contable específico con formato educativo"""
        
        # Manejar explícitamente la consulta sobre asientos contables
        if "asiento contable" in query.lower():
            return self._explain_asiento_contable()
            
        # Buscar otros conceptos en la base de conocimientos
        for concepto_key, concepto_data in self.conceptos.items():
            if concepto_key.replace("_", " ") in query or concepto_key in query:
                return self._format_concept_explanation(concepto_key, concepto_data)
        
        # Si no encuentra concepto específico, dar ayuda general
        return self._generate_educational_help()
    
    def _explain_asiento_contable(self) -> str:
        """Explicación específica de asientos contables en formato educativo"""
        data = self.conceptos["asiento_contable"]
        
        response = f"# 📚 ASIENTO CONTABLE\n\n"
        response += f"## 📝 Definición\n{data['definicion']}\n\n"
        
        response += "## ✅ Características de un Asiento Contable\n"
        for caracteristica in data['caracteristicas']:
            response += f"- **{caracteristica.split(':')[0]}:** {caracteristica.split(':')[1].strip()}\n"
        response += "\n"
        
        response += "## 📊 Ejemplo de Asiento Contable\n"
        response += f"{data['ejemplo_basico']['descripcion']}:\n\n"
        
        tabla = data['ejemplo_basico']['tabla']
        response += f"| {tabla[0][0]} | {tabla[0][1]} | {tabla[0][2]} | {tabla[0][3]} |\n"
        response += "|---------|---------|---------|----------|\n"
        for fila in tabla[1:]:
            response += f"| {fila[0]} | {fila[1]} | {fila[2]} | {fila[3]} |\n"
        response += "\n"
        
        response += "## 📚 Normativa Peruana\n"
        response += f"{data['normativa_aplicable']}\n\n"
        response += f"{data['importancia']}"
        
        return response
    
    def _format_concept_explanation(self, concepto: str, data: Dict) -> str:
        """Formatea explicación de conceptos con estructura educativa"""
        response = f"# 📚 {concepto.upper().replace('_', ' ')}\n\n"
        
        # Definición principal
        response += f"## 📝 Definición\n{data['definicion']}\n\n"
        
        # Características técnicas
        if 'caracteristicas' in data:
            response += "## ✅ Características\n"
            for char in data['caracteristicas']:
                response += f"- {char}\n"
            response += "\n"
        
        # Clasificación detallada
        if 'clasificacion' in data:
            response += "## 📊 Clasificación\n"
            for categoria, items in data['clasificacion'].items():
                response += f"### {categoria}:\n"
                if isinstance(items, dict):
                    for tipo, desc in items.items():
                        response += f"- **{tipo}:** {desc}\n"
                else:
                    response += f"- {items}\n"
                response += "\n"

        # Componentes si existen
        if 'componentes' in data:
            response += "## 🔧 Componentes\n"
            for comp, desc in data['componentes'].items():
                response += f"- **{comp}:** {desc}\n"
            response += "\n"

        # Tipos si existen
        if 'tipos' in data:
            response += "## 📋 Tipos\n"
            for tipo, desc in data['tipos'].items():
                response += f"- **{tipo}:** {desc}\n"
            response += "\n"

        # Métodos si existen
        if 'metodos' in data:
            response += "## 🛠️ Métodos\n"
            for metodo, desc in data['metodos'].items():
                response += f"- **{metodo}:** {desc}\n"
            response += "\n"

        # Fórmulas si existen
        if 'formulas' in data:
            response += "## 🧮 Fórmulas\n"
            for formula, calculo in data['formulas'].items():
                response += f"- **{formula}:** `{calculo}`\n"
            response += "\n"

        # Tratamiento específico
        if 'tratamiento' in data:
            response += "## 📝 Tratamiento Contable\n"
            for aspecto, detalle in data['tratamiento'].items():
                response += f"- **{aspecto}:** {detalle}\n"
            response += "\n"

        # Interpretación si existe
        if 'interpretacion' in data:
            response += "## 📈 Interpretación\n"
            for nivel, desc in data['interpretacion'].items():
                response += f"- **{nivel}:** {desc}\n"
            response += "\n"

        # Factores si existen
        if 'factores' in data:
            response += "## 🎯 Factores Clave\n"
            for factor in data['factores']:
                response += f"- {factor}\n"
            response += "\n"
        
        # Marco normativo NIIF
        if 'reconocimiento_niif' in data:
            response += f"## 📜 Marco Normativo\n**NIIF/NIC aplicables:** {data['reconocimiento_niif']}\n\n"
        
        # Ejemplos prácticos con números
        if 'ejemplos_practicos' in data:
            response += "## 💼 Ejemplos Prácticos\n"
            for ejemplo in data['ejemplos_practicos']:
                response += f"- {ejemplo}\n"
            response += "\n"
        
        return response
    
    def _explain_differences(self, query: str) -> str:
        """Explica diferencias entre conceptos"""
        query_lower = query.lower()
        
        # Buscar la combinación de conceptos en las diferencias definidas
        for conceptos_tuple, diferencia_data in self.diferencias.items():
            concepto1, concepto2 = conceptos_tuple
            if concepto1 in query_lower and concepto2 in query_lower:
                return self._format_difference_explanation(diferencia_data)
        
        # Si no encuentra diferencia específica, sugerir comparaciones disponibles
        return """# 📊 Comparaciones Disponibles

## 🎯 ¿Qué diferencias puedo explicarte?

### 💰 Conceptos Fundamentales:
- *"Diferencia entre gasto y costo"*
- *"Diferencia entre activo y pasivo"*

### 📈 Indicadores Financieros:
- *"Diferencia entre ROE y ROA"*

### 💡 Formato de consulta:
*"Diferencia entre [concepto A] y [concepto B]"*

**¿Qué comparación específica te interesa?**"""
    
    def _format_difference_explanation(self, data: Dict) -> str:
        """Formatea explicación de diferencias entre conceptos"""
        response = f"# 🆚 {data['concepto1']} vs {data['concepto2']}\n\n"
        
        response += f"## 📝 Definiciones\n"
        response += f"### {data['concepto1']}:\n{data['definicion1']}\n\n"
        response += f"### {data['concepto2']}:\n{data['definicion2']}\n\n"
        
        response += "## 📊 Cuadro Comparativo\n\n"
        response += "| **Criterio** | **" + data['concepto1'] + "** | **" + data['concepto2'] + "** |\n"
        response += "|--------------|------------|------------|\n"
        
        for criterio, valor1, valor2 in data['comparaciones']:
            response += f"| **{criterio}** | {valor1} | {valor2} |\n"
        
        response += "\n**¿Necesitas ejemplos específicos o más detalles sobre algún aspecto?**"
        return response
    
    def _explain_formulas(self, query: str) -> str:
        """Explica fórmulas con ejemplos detallados"""
        query_lower = query.lower()
        
        if "igv" in query_lower:
            return """# 🧮 FÓRMULAS DEL IGV

## 📊 Datos Base
- **Tasa IGV:** 18% (16% IGV + 2% IPM)

## 💰 Fórmulas Principales

### 1️⃣ Precio con IGV a Precio sin IGV:
```
Precio sin IGV = Precio con IGV ÷ 1.18
```
**Ejemplo:** S/ 1,180 ÷ 1.18 = S/ 1,000

### 2️⃣ Precio sin IGV a Precio con IGV:
```
Precio con IGV = Precio sin IGV × 1.18
```
**Ejemplo:** S/ 1,000 × 1.18 = S/ 1,180

### 3️⃣ Extraer solo el IGV:
```
Solo IGV = Precio con IGV × 0.152542
```
**Ejemplo:** S/ 1,180 × 0.152542 = S/ 180

### 4️⃣ IGV a Pagar (Liquidación):
```
IGV a Pagar = IGV Ventas - IGV Compras
```

## 💼 Ejemplo Completo
- Venta: S/ 5,900 (incluye IGV)
- Precio sin IGV: S/ 5,900 ÷ 1.18 = S/ 5,000
- IGV: S/ 5,900 × 0.152542 = S/ 900

**¿Necesitas más ejemplos o cálculos específicos?**"""
        
        elif "roe" in query_lower:
            return """# 📈 FÓRMULA ROE (Return on Equity)

## 🧮 Fórmula Principal
```
ROE = (Utilidad Neta / Patrimonio Promedio) × 100
```

## 📊 Interpretación
- **Excelente:** ROE > 15%
- **Bueno:** ROE 10% - 15%
- **Regular:** ROE 5% - 10%
- **Bajo:** ROE < 5%

## 💼 Ejemplo Práctico
- Utilidad Neta: S/ 120,000
- Patrimonio Promedio: S/ 600,000
- ROE = (120,000 / 600,000) × 100 = 20%

## 🎯 Análisis Dupont (ROE Expandido)
```
ROE = Margen Neto × Rotación Activos × Multiplicador Patrimonio
```

**¿Quieres ver ejemplos con el análisis Dupont?**"""
        
        elif "roa" in query_lower:
            return """# 📈 FÓRMULA ROA (Return on Assets)

## 🧮 Fórmula Principal
```
ROA = (Utilidad Neta / Activos Totales Promedio) × 100
```

## 📊 Interpretación
- **Excelente:** ROA > 8%
- **Bueno:** ROA 4% - 8%
- **Regular:** ROA 2% - 4%
- **Bajo:** ROA < 2%

## 💼 Ejemplo Práctico
- Utilidad Neta: S/ 80,000
- Activos Totales Promedio: S/ 1,000,000
- ROA = (80,000 / 1,000,000) × 100 = 8%

**¿Necesitas comparar con ROE o ver más ejemplos?**"""
        
        elif "depreciacion" in query_lower or "depreciación" in query_lower:
            return """# 📉 FÓRMULAS DE DEPRECIACIÓN

## 🧮 Método Línea Recta
```
Depreciación Anual = (Costo - Valor Residual) / Vida Útil
```

## 💼 Ejemplo Práctico
- Costo del Activo: S/ 60,000
- Valor Residual: S/ 6,000  
- Vida Útil: 5 años
- **Depreciación Anual:** (60,000 - 6,000) / 5 = S/ 10,800
- **Depreciación Mensual:** 10,800 / 12 = S/ 900

## 📊 Otros Métodos

### Unidades Producidas:
```
Depreciación = (Costo - V.Residual) × (Uso Período / Uso Total)
```

### Doble Saldo Decreciente:
```
Depreciación = Valor en Libros × (2 / Vida Útil)
```

**¿Quieres ver ejemplos de otros métodos?**"""
        
        else:
            return """# 🧮 Fórmulas Contables Disponibles

## 📊 ¿Qué fórmula necesitas?

### 💰 Tributarias:
- *"Fórmula IGV"* - Cálculos de impuestos
- *"Fórmula ISR"* - Impuesto a la renta

### 📈 Rentabilidad:
- *"Fórmula ROE"* - Return on Equity
- *"Fórmula ROA"* - Return on Assets

### 💧 Liquidez:
- *"Fórmula ratio corriente"*
- *"Fórmula prueba ácida"*

### 📉 Depreciación:
- *"Fórmula depreciación"*

### 💡 Formato de consulta:
*"Fórmula [concepto específico]"*

**¿Qué fórmula específica te interesa?**"""
    
    def _explain_procedures(self, query: str) -> str:
        """Explica procedimientos contables paso a paso"""
        query_lower = query.lower()
        
        # Buscar procedimiento específico
        for proc_key, proc_data in self.procedimientos.items():
            if any(keyword in query_lower for keyword in proc_key.split("_")):
                return self._format_procedure_explanation(proc_data)
        
        # Si no encuentra procedimiento específico
        return """# 🔄 Procedimientos Contables Disponibles

## 📋 ¿Qué proceso quieres aprender?

### 📝 Registros Contables:
- *"¿Cómo se registra un asiento contable?"*
- *"¿Cómo se registra una compra?"*
- *"¿Cómo se registra una venta?"*

### 📊 Cálculos:
- *"¿Cómo se calcula la depreciación?"*
- *"¿Cómo se calcula el IGV?"*

### 📈 Análisis:
- *"¿Cómo se analiza la liquidez?"*
- *"¿Cómo se calcula el ROE?"*

### 💡 Formato de consulta:
*"¿Cómo se [proceso específico]?"*

**¿Qué procedimiento específico te interesa aprender?**"""
    
    def _format_procedure_explanation(self, data: Dict) -> str:
        """Formatea explicación de procedimientos paso a paso"""
        response = f"# 🔄 {data['titulo']}\n\n"
        
        response += "## 📋 Pasos Fundamentales:\n\n"
        
        for paso in data['pasos']:
            response += f"### {paso['numero']} {paso['titulo']}:\n"
            for accion in paso['acciones']:
                response += f"- ✅ {accion}\n"
            response += "\n"
        
        if 'ejemplo_practico' in data:
            response += "## 💼 Ejemplo Paso a Paso\n\n"
            ejemplo = data['ejemplo_practico']
            
            if 'escenario' in ejemplo:
                response += f"**Escenario:** {ejemplo['escenario']}\n\n"
            
            if 'analisis' in ejemplo:
                response += f"**Análisis:** {ejemplo['analisis']}\n\n"
            
            if 'asiento' in ejemplo:
                response += f"**Registro:**\n```{ejemplo['asiento']}\n```\n"
            
            if 'datos' in ejemplo and 'calculo' in ejemplo:
                response += f"**Datos:** {ejemplo['datos']}\n"
                response += f"**Cálculo:** {ejemplo['calculo']}\n"
                if 'asiento' in ejemplo:
                    response += f"**Asiento:** {ejemplo['asiento']}\n"
        
        response += "\n**¿Necesitas aclaración sobre algún paso específico?**"
        return response
    
    def _explain_purpose(self, query: str) -> str:
        """Explica el propósito y utilidad de conceptos contables"""
        query_lower = query.lower()
        
        # Buscar propósito específico
        for prop_key, prop_data in self.propositos.items():
            if any(keyword in query_lower for keyword in prop_key.split("_")):
                return self._format_purpose_explanation(prop_key, prop_data)
        
        return """# 🎯 Propósitos en Contabilidad

## 📊 ¿Para qué sirve cada concepto?

### 📝 Registros:
- *"¿Para qué sirve un asiento contable?"*
- *"¿Para qué sirve la depreciación?"*

### 📈 Análisis:
- *"¿Para qué sirve el ROE?"*
- *"¿Para qué sirve el ratio de liquidez?"*

### 💰 Tributario:
- *"¿Para qué sirve el IGV?"*

### 💡 Formato de consulta:
*"¿Para qué sirve [concepto]?"*

**¿Sobre qué concepto quieres conocer su propósito?**"""
    
    def _explain_timing(self, query: str) -> str:
        """Explica cuándo y en qué momento aplicar conceptos contables"""
        query_lower = query.lower()
        
        # Buscar timing específico
        for timing_key, timing_data in self.timing.items():
            if any(keyword in query_lower for keyword in timing_key.split("_")):
                return self._format_timing_explanation(timing_key, timing_data)
        
        return """# ⏱️ Timing en Contabilidad

## 📅 ¿Cuándo aplicar cada concepto?

### 📝 Registros:
- *"¿Cuándo registrar un asiento contable?"*
- *"¿Cuándo calcular la depreciación?"*

### 📊 Reportes:
- *"¿Cuándo elaborar estados financieros?"*
- *"¿Cuándo hacer análisis financiero?"*

### 💡 Formato de consulta:
*"¿Cuándo [proceso/concepto]?"*

**¿Sobre qué timing específico tienes dudas?**"""
    
    def _generate_educational_help(self) -> str:
        """Ayuda general educativa"""
        return """# 📚 Educación Contable UPAO

## 🎯 ¿Qué puedo explicarte?

### 📊 Conceptos Fundamentales:
- *"¿Qué es un activo?"*
- *"¿Qué es un pasivo?"*
- *"¿Qué es el patrimonio?"*
- *"¿Qué son los ingresos?"*
- *"¿Qué son los gastos?"*

### 🧾 Asientos Contables:
- *"¿Qué es un asiento contable?"*
- *"¿Cómo se registra una compra?"*
- *"Ejemplo de asiento de venta"*
- *"¿Cómo contabilizar la depreciación?"*

### 📈 Análisis Financiero:
- *"¿Qué es un ratio?"*
- *"¿Qué es el ROE?"*
- *"¿Qué es el ROA?"*
- *"Fórmula del current ratio"*

### 💡 Formato de consulta:
- **Definiciones:** *"¿Qué es [concepto]?"*
- **Fórmulas:** *"Fórmula [concepto]"*
- **Diferencias:** *"Diferencia entre [A] y [B]"*
- **Ejemplos:** *"Ejemplo de [operación]"*

**¿Qué concepto específico te interesa aprender?**"""

# Instancia global
educational_service = EducationalService()