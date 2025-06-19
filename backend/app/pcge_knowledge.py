"""
Base de conocimiento del Plan Contable General Empresarial (PCGE) Perú
"""

PCGE_CUENTAS = {
    # ACTIVO
    "10": {"nombre": "Efectivo y equivalentes de efectivo", "tipo": "activo"},
    "11": {"nombre": "Inversiones financieras", "tipo": "activo"},
    "12": {"nombre": "Cuentas por cobrar comerciales - terceros", "tipo": "activo"},
    "13": {"nombre": "Cuentas por cobrar comerciales - relacionadas", "tipo": "activo"},
    "14": {"nombre": "Cuentas por cobrar al personal, accionistas, directores y gerentes", "tipo": "activo"},
    "16": {"nombre": "Cuentas por cobrar diversas - terceros", "tipo": "activo"},
    "17": {"nombre": "Cuentas por cobrar diversas - relacionadas", "tipo": "activo"},
    "18": {"nombre": "Servicios y otros contratados por anticipado", "tipo": "activo"},
    "19": {"nombre": "Estimación de cuentas de cobranza dudosa", "tipo": "activo"},
    "20": {"nombre": "Mercaderías", "tipo": "activo"},
    "21": {"nombre": "Productos terminados", "tipo": "activo"},
    "22": {"nombre": "Subproductos, desechos y desperdicios", "tipo": "activo"},
    "23": {"nombre": "Productos en proceso", "tipo": "activo"},
    "24": {"nombre": "Materias primas", "tipo": "activo"},
    "25": {"nombre": "Materiales auxiliares, suministros y repuestos", "tipo": "activo"},
    "26": {"nombre": "Envases y embalajes", "tipo": "activo"},
    "27": {"nombre": "Activos no corrientes mantenidos para la venta", "tipo": "activo"},
    "28": {"nombre": "Existencias por recibir", "tipo": "activo"},
    "29": {"nombre": "Desvalorización de existencias", "tipo": "activo"},
    "30": {"nombre": "Inversiones mobiliarias", "tipo": "activo"},
    "31": {"nombre": "Inversiones inmobiliarias", "tipo": "activo"},
    "32": {"nombre": "Activos adquiridos en arrendamiento financiero", "tipo": "activo"},
    "33": {"nombre": "Inmuebles, maquinaria y equipo", "tipo": "activo"},
    "34": {"nombre": "Intangibles", "tipo": "activo"},
    "35": {"nombre": "Activos biológicos", "tipo": "activo"},
    "36": {"nombre": "Desvalorización de activo inmovilizado", "tipo": "activo"},
    "37": {"nombre": "Activo diferido", "tipo": "activo"},
    "38": {"nombre": "Otros activos", "tipo": "activo"},
    "39": {"nombre": "Depreciación, amortización y agotamiento acumulados", "tipo": "activo"},
    
    # PASIVO
    "40": {"nombre": "Tributos, contraprestaciones y aportes al sistema de pensiones y de salud por pagar", "tipo": "pasivo"},
    "41": {"nombre": "Remuneraciones y participaciones por pagar", "tipo": "pasivo"},
    "42": {"nombre": "Cuentas por pagar comerciales - terceros", "tipo": "pasivo"},
    "43": {"nombre": "Cuentas por pagar comerciales - relacionadas", "tipo": "pasivo"},
    "44": {"nombre": "Cuentas por pagar a los accionistas, directores y gerentes", "tipo": "pasivo"},
    "45": {"nombre": "Obligaciones financieras", "tipo": "pasivo"},
    "46": {"nombre": "Cuentas por pagar diversas - terceros", "tipo": "pasivo"},
    "47": {"nombre": "Cuentas por pagar diversas - relacionadas", "tipo": "pasivo"},
    "48": {"nombre": "Provisiones", "tipo": "pasivo"},
    "49": {"nombre": "Pasivo diferido", "tipo": "pasivo"},
    
    # PATRIMONIO
    "50": {"nombre": "Capital", "tipo": "patrimonio"},
    "51": {"nombre": "Acciones de inversión", "tipo": "patrimonio"},
    "52": {"nombre": "Capital adicional", "tipo": "patrimonio"},
    "56": {"nombre": "Resultados no realizados", "tipo": "patrimonio"},
    "57": {"nombre": "Excedente de revaluación", "tipo": "patrimonio"},
    "58": {"nombre": "Reservas", "tipo": "patrimonio"},
    "59": {"nombre": "Resultados acumulados", "tipo": "patrimonio"},
    
    # GASTOS
    "60": {"nombre": "Compras", "tipo": "gasto"},
    "61": {"nombre": "Variación de existencias", "tipo": "gasto"},
    "62": {"nombre": "Gastos de personal, directores y gerentes", "tipo": "gasto"},
    "63": {"nombre": "Gastos de servicios prestados por terceros", "tipo": "gasto"},
    "64": {"nombre": "Gastos por tributos", "tipo": "gasto"},
    "65": {"nombre": "Otros gastos de gestión", "tipo": "gasto"},
    "66": {"nombre": "Pérdida por medición de activos no financieros al valor razonable", "tipo": "gasto"},
    "67": {"nombre": "Gastos financieros", "tipo": "gasto"},
    "68": {"nombre": "Valuación y deterioro de activos y provisiones", "tipo": "gasto"},
    "69": {"nombre": "Costo de ventas", "tipo": "gasto"},
    
    # INGRESOS
    "70": {"nombre": "Ventas", "tipo": "ingreso"},
    "71": {"nombre": "Variación de la producción almacenada", "tipo": "ingreso"},
    "72": {"nombre": "Producción de activo inmovilizado", "tipo": "ingreso"},
    "73": {"nombre": "Descuentos, rebajas y bonificaciones obtenidos", "tipo": "ingreso"},
    "74": {"nombre": "Descuentos, rebajas y bonificaciones concedidos", "tipo": "ingreso"},
    "75": {"nombre": "Otros ingresos de gestión", "tipo": "ingreso"},
    "76": {"nombre": "Ganancia por medición de activos no financieros al valor razonable", "tipo": "ingreso"},
    "77": {"nombre": "Ingresos financieros", "tipo": "ingreso"},
    "78": {"nombre": "Cargas cubiertas por provisiones", "tipo": "ingreso"},
    "79": {"nombre": "Cargas imputables a cuentas de costos y gastos", "tipo": "ingreso"},
    
    # ANALÍTICAS DE EXPLOTACIÓN
    "80": {"nombre": "Margen comercial", "tipo": "analitica"},
    "81": {"nombre": "Producción del ejercicio", "tipo": "analitica"},
    "82": {"nombre": "Valor agregado", "tipo": "analitica"},
    "83": {"nombre": "Excedente bruto de explotación", "tipo": "analitica"},
    "84": {"nombre": "Resultado de explotación", "tipo": "analitica"},
    "85": {"nombre": "Resultado antes de participaciones e impuestos", "tipo": "analitica"},
    "86": {"nombre": "Distribución legal de la renta neta", "tipo": "analitica"},
    "87": {"nombre": "Participaciones de los trabajadores", "tipo": "analitica"},
    "88": {"nombre": "Impuesto a la renta", "tipo": "analitica"},
    "89": {"nombre": "Determinación del resultado del ejercicio", "tipo": "analitica"},
}

OPERACIONES_COMUNES = {
    "prestamo_bancario": {
        "descripcion": "Registro de préstamo bancario",
        "cuentas": {
            "efectivo": "10.1",  # Efectivo y equivalentes de efectivo
            "obligacion_corto": "45.1",  # Obligaciones financieras - corto plazo
            "obligacion_largo": "45.2",  # Obligaciones financieras - largo plazo
            "intereses_diferidos": "37.5",  # Activo diferido - Intereses diferidos
            "gastos_financieros": "67.3",  # Gastos financieros - Intereses por préstamos
        },
        "ejemplo": """
        1. REGISTRO DEL PRÉSTAMO RECIBIDO:
        10.1 Efectivo y equivalentes de efectivo    10,000.00
            45.1 Obligaciones financieras                     10,000.00
        
        2. REGISTRO DE DEVENGAMIENTO DE INTERESES MENSUAL:
        67.3 Gastos financieros - Intereses         83.33
            45.1 Obligaciones financieras                        83.33
        
        3. PAGO DE CUOTA (capital + intereses):
        45.1 Obligaciones financieras               916.67
        67.3 Gastos financieros - Intereses         83.33
            10.1 Efectivo y equivalentes de efectivo           1,000.00
        """
    },
    "compra_mercaderia": {
        "descripcion": "Compra de mercaderías",
        "cuentas": {
            "mercaderias": "20.1",
            "igv": "40.11",
            "proveedor": "42.1",
            "efectivo": "10.1"
        }
    },
    "venta_mercaderia": {
        "descripcion": "Venta de mercaderías",
        "cuentas": {
            "cliente": "12.1",
            "ventas": "70.1",
            "igv": "40.11",
            "costo_ventas": "69.1",
            "mercaderias": "20.1"
        }
    }
}

def buscar_cuenta_pcge(termino: str) -> dict:
    """Busca una cuenta en el PCGE por término"""
    termino = termino.lower()
    resultados = []
    
    for codigo, info in PCGE_CUENTAS.items():
        if (termino in info["nombre"].lower() or 
            termino in codigo or
            any(palabra in info["nombre"].lower() for palabra in termino.split())):
            resultados.append({
                "codigo": codigo,
                "nombre": info["nombre"],
                "tipo": info["tipo"]
            })
    
    return resultados

def obtener_operacion_ejemplo(tipo_operacion: str) -> dict:
    """Obtiene ejemplo de operación contable"""
    return OPERACIONES_COMUNES.get(tipo_operacion, {})

def validar_asiento_pcge(asiento_texto: str) -> dict:
    """Valida si un asiento usa cuentas del PCGE correctamente"""
    import re
    
    # Extraer códigos de cuenta del asiento
    codigos_encontrados = re.findall(r'\b\d{2}(?:\.\d+)*\b', asiento_texto)
    
    validacion = {
        "valido": True,
        "errores": [],
        "sugerencias": []
    }
    
    for codigo in codigos_encontrados:
        codigo_base = codigo.split('.')[0]
        if codigo_base not in PCGE_CUENTAS:
            validacion["valido"] = False
            validacion["errores"].append(f"Cuenta {codigo} no existe en PCGE")
            
            # Buscar sugerencias
            termino_busqueda = codigo_base
            sugerencias = buscar_cuenta_pcge(termino_busqueda)
            if sugerencias:
                validacion["sugerencias"].extend(sugerencias[:3])
    
    return validacion