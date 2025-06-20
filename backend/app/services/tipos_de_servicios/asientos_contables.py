import re
from ...core.utils import format_currency

class AsientosContables:
    """Generador universal de asientos contables dinámicos"""

    def _extract_amount(self, query: str) -> float:
        # Detectar patrones flexibles de cantidad y precio unitario
        match = re.search(
            r'(\d+)\s+\w+\s*(?:de\s+precio\s+de|de\s+precio|a\s+un\s+precio\s+de|a\s+|de\s+|con\s+un\s+precio\s+de|con\s+precio\s+de|con\s+precio|a|de)\s*([\d][\d.,]*)',
            query, re.IGNORECASE)
        if match:
            cantidad = int(match.group(1))
            raw_precio = match.group(2)
            # Normalizar el precio
            if '.' in raw_precio and ',' in raw_precio:
                if raw_precio.find('.') < raw_precio.find(','):
                    raw_precio = raw_precio.replace('.', '').replace(',', '.')
                else:
                    raw_precio = raw_precio.replace(',', '')
            elif ',' in raw_precio:
                if raw_precio.count(',') == 1 and len(raw_precio.split(',')[-1]) <= 2:
                    raw_precio = raw_precio.replace(',', '.')
                else:
                    raw_precio = raw_precio.replace(',', '')
            elif '.' in raw_precio:
                if raw_precio.count('.') == 1 and len(raw_precio.split('.')[-1]) <= 2:
                    pass
                else:
                    raw_precio = raw_precio.replace('.', '')
            try:
                precio = float(raw_precio)
                monto = cantidad * precio
                if monto > 0:
                    return monto
            except Exception:
                pass
        # Busca el primer monto grande (no porcentaje ni interés)
        patterns = [
            r'(?:monto|de|por|por un monto de|por la suma de|por valor de|S/|soles)\s*([\d][\d.,]*)',
            r'([\d][\d.,]*)\s*(?:soles|S/)?'
        ]
        for pat in patterns:
            match = re.search(pat, query, re.IGNORECASE)
            if match:
                raw = match.group(1)
                if '.' in raw and ',' in raw:
                    if raw.find('.') < raw.find(','):
                        raw = raw.replace('.', '').replace(',', '.')
                    else:
                        raw = raw.replace(',', '')
                elif ',' in raw:
                    if raw.count(',') == 1 and len(raw.split(',')[-1]) <= 2:
                        raw = raw.replace(',', '.')
                    else:
                        raw = raw.replace(',', '')
                elif '.' in raw:
                    if raw.count('.') == 1 and len(raw.split('.')[-1]) <= 2:
                        pass
                    else:
                        raw = raw.replace('.', '')
                try:
                    value = float(raw)
                    if value > 0:
                        return value
                except Exception:
                    continue
        return 0.0

    def _extract_interest(self, query: str, monto: float) -> float:
        q = query.lower()
        # Caso 1: "más 500 soles de intereses" o "500 soles de intereses"
        match_monto = re.search(r'(?:más|mas)?\s*([\d][\d.,]*)\s*(?:soles)?\s*(?:de)?\s*inter[eé]s(?:es)?', q)
        if not match_monto:
            # Caso 2: "intereses de 500", "interés de 500"
            match_monto = re.search(r'inter[eé]s(?:es)?(?: de)?\s*(?:s/?\s*)?([\d][\d.,]*)', q)
        if match_monto:
            raw = match_monto.group(1)
            if '.' in raw and ',' in raw:
                if raw.find('.') < raw.find(','):
                    raw = raw.replace('.', '').replace(',', '.')
                else:
                    raw = raw.replace(',', '')
            elif ',' in raw:
                if raw.count(',') == 1 and len(raw.split(',')[-1]) <= 2:
                    raw = raw.replace(',', '.')
                else:
                    raw = raw.replace(',', '')
            elif '.' in raw:
                if raw.count('.') == 1 and len(raw.split('.')[-1]) <= 2:
                    pass
                else:
                    raw = raw.replace('.', '')
            try:
                value = float(raw)
                if value > 0 and (not monto or value < monto * 2):
                    return value
            except Exception:
                pass
        # Caso 3: porcentaje
        match_pct = re.search(r'inter[eé]s(?: del?| de)?\s*([\d][\d.,]*)\s*(%|por\s?ciento|porciento)', q)
        if match_pct and monto > 0:
            pct_raw = match_pct.group(1)
            if '.' in pct_raw and ',' in pct_raw:
                if pct_raw.find('.') < pct_raw.find(','):
                    pct_raw = pct_raw.replace('.', '').replace(',', '.')
                else:
                    pct_raw = pct_raw.replace(',', '')
            elif ',' in pct_raw:
                if pct_raw.count(',') == 1 and len(pct_raw.split(',')[-1]) <= 2:
                    pct_raw = pct_raw.replace(',', '.')
                else:
                    pct_raw = pct_raw.replace(',', '')
            elif '.' in pct_raw:
                if pct_raw.count('.') == 1 and len(pct_raw.split('.')[-1]) <= 2:
                    pass
                else:
                    pct_raw = pct_raw.replace('.', '')
            try:
                pct = float(pct_raw)
                if 0 < pct < 100:
                    return monto * pct / 100
            except Exception:
                pass
        return 0.0

    def _extract_partes(self, query: str):
        # Busca nombres de empresas/personas después de "la empresa", "a la empresa", "por", "de", etc.
        partes = []
        # Busca patrones tipo "la empresa X", "a la empresa Y", "por la empresa Z"
        matches = re.findall(r'(?:la empresa|a la empresa|de la empresa|para la empresa|empresa)\s+([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑñ\s\S]{2,50}?)(?=[\.,;]|$)', query)
        for m in matches:
            m = m.strip()
            if not re.search(r'\d|monto|soles|inter[eé]s|pr[eé]stamo|capital|importe|por ', m, re.I):
                partes.append(m)
        return list(dict.fromkeys(partes))  # Quita duplicados

    def _extract_glosa(self, query: str) -> str:
        # Busca glosa después de "por", pero solo si es frase larga y no contiene solo números o palabras genéricas
        match = re.search(r'por\s+([a-záéíóúñ0-9\s,\.]{5,})', query.lower())
        if match:
            glosa = match.group(1).strip().capitalize()
            if not re.fullmatch(r'[\d,\. ]+', glosa) and not re.search(r'monto|soles|inter[eé]s|pr[eé]stamo', glosa):
                return glosa
        return ""

    def _extract_cuotas(self, query: str) -> int:
        # Busca frases como "3 cuotas", "tres cuotas", "primeras 3 cuotas", etc.
        match = re.search(r'(\d+)\s*(primeras|primeros)?\s*cuotas?', query, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except Exception:
                pass
        return 1  # Por defecto 1 cuota

    async def generate_response(self, query: str, context, metadata) -> str:
        q = query.lower()
        monto = self._extract_amount(query)
        interes = self._extract_interest(query, monto)
        partes = self._extract_partes(query)
        glosa = self._extract_glosa(query)
        cuotas_pagar = self._extract_cuotas(query)  # <-- Nuevo

        # Detecta tipo de asiento as
        if "pago a cuenta" in q and ("marzo" in q or "anticipo" in q):
            return self._asiento_pago_cuenta_renta(monto, partes, glosa)
        if "compensación" in q and "saldo a favor" in q:
            return self._asiento_compensacion_saldo_favor(monto, partes, glosa)
        if "dividendo" in q or "dividendos" in q:
            return self._asiento_dividendos(monto, partes, glosa)
        if "cuarta categoría" in q or "honorario" in q or "recibo por honorario" in q:
            return self._asiento_retencion_cuarta(monto, partes, glosa)
        if "pago a cuenta" in q and "diciembre" in q:
            return self._asiento_pago_cuenta_renta_diciembre(monto, partes, glosa)
        if "impuesto a la renta" in q:
            return self._asiento_impuesto_renta_anual(monto, partes, glosa)
        if "fcjmms" in q or "fondo complementario de jubilación minera" in q:
            return self._asiento_fcjmms(monto, partes, glosa)
        if "accionista" in q and ("préstamo" in q or "prestamo" in q):
            return self._asiento_prestamo_accionista(monto, interes, partes, glosa)
        if "préstamo bancario" in q or "prestamo bancario" in q or "préstamo financiero" in q or "prestamo financiero" in q or "cuota" in q or "mensual" in q or "plazo" in q:
            return self._asiento_prestamo_bancario(monto, interes, partes, glosa, cuotas_pagar=cuotas_pagar)
        elif ("préstamo" in q or "prestamo" in q) and ("sin interés" in q or "sin intereses" in q or interes == 0):
            return self._asiento_prestamo_sin_interes(monto, partes, glosa)
        elif "préstamo" in q or "prestamo" in q:
            return self._asiento_prestamo(monto, interes, partes, glosa)
        elif "compra" in q:
            return self._asiento_compra(monto, partes, glosa)
        elif "venta" in q:
            return self._asiento_venta(monto, partes, glosa)
        elif "depreciacion" in q or "depreciación" in q:
            return self._asiento_depreciacion(monto, partes, glosa)
        elif "interés diferido" in q or "interes diferido" in q:
            tipo = "por_cobrar" if "por cobrar" in q else "por_pagar" if "por pagar" in q else "por_cobrar"
            return self._asiento_interes_diferido(monto, tipo=tipo)
        else:
            return self._asiento_generico(monto, interes, partes, glosa)
        


    def _asiento_prestamo(self, monto, interes, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto del préstamo. Escribe por ejemplo: 'asiento de préstamo de 10,000 con interés del 10%'"
        total = monto + interes
        empresa_destino = partes[0] if partes else "la empresa"
        glosa_final = glosa or f"Por el préstamo otorgado a {empresa_destino}."
        # 1. Otorgamiento del préstamo
        asiento1 = f"""


## 💼 Asiento Contable de Préstamo a Empresa

### 1️⃣ Otorgamiento del Préstamo

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 16     | CUENTAS POR COBRAR DIVERSAS – TERCEROS | {format_currency(total)} |   |
| 161    | PRÉSTAMOS |   |   |
| 49     | PASIVO DIFERIDO |   | {format_currency(interes)} |
| 493    | INTERESES DIFERIDOS |   |   |
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO |   | {format_currency(monto)} |
| 104    | CUENTAS CORRIENTES EN INSTITUCIONES FINANCIERAS |   |   |
| 1041   | CUENTAS CORRIENTES OPERATIVAS |   |   |

**X/X {glosa_final}**
Posteriormente, se devengarán los intereses.
"""
        # 2. Devengo de intereses
        asiento2 = f"""
### 2️⃣ Devengo de Intereses

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 49     | PASIVO DIFERIDO | {format_currency(interes)} |   |
| 493    | INTERESES DIFERIDOS |   |   |
| 77     | INGRESOS FINANCIEROS |   | {format_currency(interes)} |
| 779    | OTROS INGRESOS FINANCIEROS |   |   |

**X/X Por los intereses devengados.**
"""
        # 3. Cobro del préstamo
        asiento3 = f"""
### 3️⃣ Cobro del Préstamo

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO | {format_currency(total)} |   |
| 104    | CUENTAS CORRIENTES EN INSTITUCIONES FINANCIERAS |   |   |
| 1041   | CUENTAS CORRIENTES OPERATIVAS |   |   |
| 16     | CUENTAS POR COBRAR DIVERSAS – TERCEROS |   | {format_currency(total)} |
| 161    | PRÉSTAMOS |   |   |

**X/X Por el cobro del préstamo otorgado a la empresa.**
"""
        return asiento1 + asiento2 + asiento3

    def _asiento_prestamo_sin_interes(self, monto, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto del préstamo. Escribe por ejemplo: 'asiento de préstamo de 4,000 sin intereses'"
        persona_destino = partes[0] if partes else "la persona natural"
        glosa_final = glosa or f"Por el préstamo otorgado a {persona_destino}."
        # 1. Otorgamiento del préstamo
        asiento1 = f"""


        
## 💼 Asiento Contable de Préstamo sin Intereses

### 1️⃣ Otorgamiento del Préstamo

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 16     | CUENTAS POR COBRAR DIVERSAS – TERCEROS | {format_currency(monto)} |   |
| 161    | PRÉSTAMOS |   |   |
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO |   | {format_currency(monto)} |
| 104    | CUENTAS CORRIENTES EN INSTITUCIONES FINANCIERAS |   |   |
| 1041   | CUENTAS CORRIENTES OPERATIVAS |   |   |

**X/X {glosa_final}**
Posteriormente, la empresa cobra el préstamo otorgado a la persona natural.
"""
        # 2. Cobro del préstamo
        asiento2 = f"""
### 2️⃣ Cobro del Préstamo

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO | {format_currency(monto)} |   |
| 104    | CUENTAS CORRIENTES EN INSTITUCIONES FINANCIERAS |   |   |
| 1041   | CUENTAS CORRIENTES OPERATIVAS |   |   |
| 16     | CUENTAS POR COBRAR DIVERSAS – TERCEROS |   | {format_currency(monto)} |
| 161    | PRÉSTAMOS |   |   |

**X/X Por el cobro del préstamo otorgado a la persona natural.**
"""
        return asiento1 + asiento2

    def _asiento_prestamo_accionista(self, monto, interes, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto del préstamo. Escribe por ejemplo: 'préstamo de accionista de 30,000 con interés de 400'"
        total = monto + interes
        glosa_final = glosa or "Por el préstamo recibido del accionista"
        # 1. Préstamo recibido
        asiento1 = f"""


## 🏦 Asiento Contable de Préstamo de un Accionista

### 1️⃣ Préstamo recibido

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO | {format_currency(monto)} |   |
| 1041   | CUENTAS CORRIENTES OPERATIVAS |   |   |
| 37     | ACTIVO DIFERIDO | {format_currency(interes)} |   |
| 373    | INTERESES DIFERIDOS |   |   |
| 44     | CUENT. POR PAGAR A LOS ACC. Y DIRECTORES |   | {format_currency(total)} |
| 4411   | ACCIONISTAS |   |   |

**X/X {glosa_final}**
Posteriormente, pasará el tiempo, y se devengará el interés.
"""
        # 2. Devengo de intereses
        asiento2 = f"""
### 2️⃣ Devengo de intereses

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 67     | GASTOS FINANCIEROS | {format_currency(interes)} |   |
| 673    | INTERESES POR PRÉSTAMOS |   |   |
| 37     | ACTIVO DIFERIDO |   | {format_currency(interes)} |
| 373    | INTERESES DIFERIDOS |   |   |

**X/X Por el devengo de los intereses**
"""
        # 3. Cancelación del préstamo
        asiento3 = f"""
### 3️⃣ Cancelación del préstamo

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 44     | CUENT. POR PAGAR A LOS ACC. Y DIRECTORES | {format_currency(total)} |   |
| 4411   | ACCIONISTAS |   |   |
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO |   | {format_currency(total)} |
| 1041   | CUENTAS CORRIENTES OPERATIVAS |   |   |

**X/X Por el pago del préstamo recibido del accionista**
"""
        return asiento1 + asiento2 + asiento3

    def _asiento_fcjmms(self, monto, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto del aporte. Escribe por ejemplo: 'asiento FCJMMS de 99,000'"
        glosa_final = glosa or "Por el reconocimiento del tributo FCJMMS."
        return f"""


## 🏭 Asiento Contable del FCJMMS

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 64     | GASTOS POR TRIBUTOS | {format_currency(monto)} |   |
| 641    | GOBIERNO NACIONAL |   |   |
| 6419   | OTROS |   |   |
| 40     | TRIB. CONT. Y AP. AL SIST. DE PENS. Y DE SALUD POR PAG. |   | {format_currency(monto)} |
| 401    | GOBIERNO CENTRAL |   |   |
| 4018   | OTROS IMPUESTOS Y CONTRAPRESTACIONES |   |   |
| 40189  | OTROS IMPUESTOS |   |   |

**X/X {glosa_final}**
"""
    def _asiento_impuesto_renta_anual(self, monto, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto del impuesto. Escribe por ejemplo: 'impuesto a la renta de 45,000'"
        glosa_final = glosa or "Por la determinación del impuesto a la renta."
        # 1. Determinación del impuesto
        asiento1 = f"""


## 🧾 Asiento Contable de Impuesto a la Renta Anual

### 1️⃣ Determinación del impuesto

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 88     | IMPUESTO A LA RENTA | {format_currency(monto)} |   |
| 881    | IMPUESTO A LAS GANANCIAS – CORRIENTE |   |   |
| 40     | TRIB. CONT. Y APORTES AL SIST. DE PENS. Y DE SALUD POR PAG. |   | {format_currency(monto)} |
| 401    | GOBIERNO CENTRAL |   |   |
| 40171  | RENTA DE TERCERA CATEGORÍA |   |   |

**X/X {glosa_final}**
Por otra parte, podemos cancelar el impuesto a la renta del ejercicio con los pagos a cuenta y, si fuera necesario, con efectivo.
"""
        # 2. Compensación con pagos a cuenta (ejemplo: S/ 40,000)
        pagos_cuenta = monto - 5000 if monto > 5000 else monto
        asiento2 = f"""
### 2️⃣ Compensación con pagos a cuenta

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 40     | TRIB. CONT. Y APORTES AL SIST. DE PENS. Y DE SALUD POR PAG. | {format_currency(pagos_cuenta)} |   |
| 401    | GOBIERNO CENTRAL |   |   |
| 40171  | RENTA DE TERCERA CATEGORÍA |   |   |
| 16     | CUENTAS POR COBRAR DIVERSAS – TERCEROS |   | {format_currency(pagos_cuenta)} |
| 167    | TRIBUTOS POR ACREDITAR |   |   |
| 1671   | PAGOS A CUENTA DEL IMPUESTO A LA RENTA |   |   |

**X/X Por la compensación con los pagos a cuenta.**
La diferencia lo cancelas con una transferencia.
"""
        # 3. Cancelación con efectivo (ejemplo: S/ 5,000)
        diferencia = monto - pagos_cuenta
        asiento3 = f"""
### 3️⃣ Cancelación con efectivo

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 40     | TRIB. CONT. Y APORTES AL SIST. DE PENS. Y DE SALUD POR PAG. | {format_currency(diferencia)} |   |
| 401    | GOBIERNO CENTRAL |   |   |
| 40171  | RENTA DE TERCERA CATEGORÍA |   |   |
| 10     | EFECTIVO Y EQUIVALENTES DE EFECTIVO |   | {format_currency(diferencia)} |
| 104    | CUENTAS CORRIE. INST FINANCIERAS |   |   |

**X/X Por la cancelación del impuesto a la renta.**
Posteriormente, aplicaremos el impuesto a la renta al resultado del ejercicio.
"""
        # 4. Aplicación del impuesto a la utilidad
        asiento4 = f"""
### 4️⃣ Aplicación del impuesto a la utilidad

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 89     | DETERMINACIÓN DEL RESULTADO DEL EJERCICIO | {format_currency(monto)} |   |
| 891    | UTILIDAD |   |   |
| 88     | IMPUESTO A LA RENTA |   | {format_currency(monto)} |
| 881    | IMPUESTO A LAS GANANCIAS – CORRIENTE |   |   |

**X/X Por aplicación del impuesto a la renta a la utilidad.**
Finalmente, el saldo deudor de esta cuenta, al cierre del período, con cargo a la cuenta 59 resultados acumulados.
"""
        # 5. Cierre con resultados acumululados
        asiento5 = f"""
### 5️⃣ Cierre con resultados acumulados

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 59     | RESULTADOS ACUMULADOS | {format_currency(monto)} |   |
| 591    | UTILIDADES NO DISTRIBUIDAS |   |   |
| 89     | DETERMINACIÓN DEL RESULTADO DEL EJERCICIO |   | {format_currency(monto)} |
| 891    | UTILIDAD |   |   |

**X/X Por aplicación del impuesto a la renta a la utilidad.**
"""
        return asiento1 + asiento2 + asiento3 + asiento4 + asiento5

    def _asiento_pago_cuenta_renta_diciembre(self, monto, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto del pago a cuenta. Escribe por ejemplo: 'pago a cuenta de diciembre de 300'"
        glosa_final = glosa or "Por el reconocimiento del pago a cuenta del periodo diciembre."
        # 1. Reconocimiento del pago a cuenta
        asiento1 = f"""


## 💵 Asiento Contable: Pago a Cuenta del Impuesto a la Renta de Diciembre

### 1️⃣ Reconocimiento del pago a cuenta

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 16     | CUENTAS POR COBRAR DIVERSAS – TERCEROS | {format_currency(monto)} |   |
| 167    | TRIBUTOS POR ACREDITAR |   |   |
| 1671   | PAGOS A CUENTA DEL IMPUESTO A LA RENTA |   |   |
| 40     | TRIBUTOS CONT. APORT. AL SIST. DE PENS. Y DE SALUD POR PAGAR |   | {format_currency(monto)} |
| 401    | GOBIERNO CENTRAL |   |   |
| 4017   | IMPUESTO A LA RENTA |   |   |
| 40171  | RENTA DE TERCERA CATEGORÍA |   |   |

**X/X {glosa_final}**
"""
        # 2. Cancelación del pago a cuenta
        asiento2 = f"""
### 2️⃣ Cancelación del pago a cuenta

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 40     | TRIBUTOS CONT. APORT. AL SIST. DE PENS. Y DE SALUD POR PAGAR | {format_currency(monto)} |   |
| 401    | GOBIERNO CENTRAL |   |   |
| 4017   | IMPUESTO A LA RENTA |   |   |
| 40171  | RENTA DE TERCERA CATEGORÍA |   |   |
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO |   | {format_currency(monto)} |
| 104    | CUENT. CORRIE. EN INST. FINANC. |   |   |
| 1041   | CUENT. CORRIE. OPERATIVAS |   |   |

**X/X Por la cancelación del pago a cuenta del periodo diciembre.**
"""
        return asiento1 + asiento2
    

    def _asiento_pago_cuenta_renta(self, monto, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto del pago a cuenta. Escribe por ejemplo: 'pago a cuenta de 850'"
        glosa_final = glosa or "Por el reconocimiento del anticipo del impuesto a la renta."
        return f"""
## 💵 Asiento Contable: Pago a Cuenta del Impuesto a la Renta

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 16     | CUENTAS POR COBRAR DIVERSAS – TERCEROS | {format_currency(monto)} |   |
| 167    | TRIBUTOS POR ACREDITAR |   |   |
| 1671   | PAGOS A CUENTA DE IMPUESTO A LA RENTA |   |   |
| 16711  | RENTA DE TERCERA CATEGORÍA |   |   |
| 10     | EFECTIVO Y EQUIVALENTES DE EFECTIVO |   | {format_currency(monto)} |
| 104    | CUENTAS CORRIENTES EN INSTIT. FINAN. |   |   |
| 1041   | CUENTAS CORRIENTES OPERATIVAS |   |   |

**X/X {glosa_final}**
"""

    def _asiento_dividendos(self, monto, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto de los dividendos. Escribe por ejemplo: 'dividendos de 78,500'"
        retencion = round(monto * 0.05, 2)
        neto = monto - retencion
        glosa_final = glosa or "Por el registro del reparto de dividendos"
        return f"""
## 💰 Asiento Contable: Reparto de Dividendos

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 59     | RESULTADOS ACUMULADOS | {format_currency(monto)} |   |
| 591    | UTILIDADES NO DISTRIBUIDAS |   |   |
| 5911   | UTILIDADES ACUMULADAS |   |   |
| 44     | CUENT. POR PAGAR A LOS ACCI., DIREC. Y GERENTES |   | {format_currency(neto)} |
| 441    | ACCIONISTAS (O SOCIOS) |   |   |
| 4412   | DIVIDENDOS |   |   |
| 40     | TRIB. CONT. Y APORTES AL SIST. DE PENS. Y DE SALUD POR PAG. |   | {format_currency(retencion)} |
| 401    | GOBIERNO CENTRAL |   |   |
| 4018   | OTROS IMPUESTOS Y CONTRAPRESTACIONES |   |   |
| 40185  | IMPUESTO A LOS DIVIDENDOS |   |   |

**X/X {glosa_final}**
"""

    def _asiento_compensacion_saldo_favor(self, monto, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto de la compensación. Escribe por ejemplo: 'compensación saldo a favor de 1,200'"
        glosa_final = glosa or "Por la compensación del saldo a favor contra el pago a cuenta."
        return f"""
## 🔄 Asiento Contable: Compensación de Saldo a Favor

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 16     | CUENTAS POR COBRAR DIVERSAS – TERCEROS | {format_currency(monto)} |   |
| 167    | TRIBUTOS POR ACREDITAR |   |   |
| 1671   | PAGOS A CUENTA DE IMPUESTO A LA RENTA |   |   |
| 16711  | RENTA DE TERCERA CATEGORÍA |   |   |
| 40     | TRIB. CONT. Y APORTES AL SIST. DE PENS. Y DE SALUD POR PAG. |   | {format_currency(monto)} |
| 401    | GOBIERNO CENTRAL |   |   |
| 4017   | IMPUESTO A LA RENTA |   |   |
| 40171  | RENTA DE TERCERA CATEGORÍA |   |   |
| 401711 | SALDO A FAVOR EJERCICIO 2024 |   |   |

**X/X {glosa_final}**
"""

    def _asiento_retencion_cuarta(self, monto, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto del recibo. Escribe por ejemplo: 'honorarios de 2,400'"
        retencion = round(monto * 0.08, 2)
        neto = monto - retencion
        glosa_final = glosa or "Por el registro del recibo por honorarios"
        return f"""
## 🧾 Asiento Contable: Retención de Cuarta Categoría

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 63     | GASTOS DE SERVICIOS PRESTADOS POR TERCEROS | {format_currency(monto)} |   |
| 632    | ASESORÍA Y CONSULTORÍA |   |   |
| 6326   | INVESTIGACIÓN Y DESARROLLO |   |   |
| 40     | TRIB. CONT. Y APORTES AL SIST. DE PENS. Y DE SALUD POR PAG. |   | {format_currency(retencion)} |
| 401    | GOBIERNO CENTRAL |   |   |
| 4017   | IMPUESTO A LA RENTA |   |   |
| 40172  | RENTA DE CUARTA CATEGORÍA |   |   |
| 42     | CUENTAS POR PAGAR COMERCIALES – TERCEROS |   | {format_currency(neto)} |
| 424    | HONORARIOS POR PAGAR |   |   |

**X/X {glosa_final}**
"""

    def _asiento_amortizacion_prestamo(self, monto, interes, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto de la amortización. Escribe por ejemplo: 'amortización de préstamo de 10,000 con interés de 500'"
        glosa_final = glosa or "Por la amortización del préstamo bancario."
        # 1. Devengo de intereses
        asiento1 = f"""
## 🏦 Asiento Contable: Amortización de Préstamo Bancario

### 1️⃣ Devengo de intereses hasta la fecha de cancelación

| CUENTA | DENOMINACIÓN                              | DEBE           | HABER         |
|--------|-------------------------------------------|----------------|---------------|
| 67     | GASTOS FINANCIEROS                        | {format_currency(interes)} |   |
| 673    | INTERES. POR PREST. Y OTRAS OBLIG.        |                |               |
| 6731   | PREST. DE INST. FINANC. Y OTRAS ENT.      |                |               |
| 37     | ACTIVO DIFERIDO                           |                | {format_currency(interes)} |
| 373    | INTERESES DIFERIDOS                       |                |               |
| 3731   | INT. NO DEVEN. EN TRANSC. CON TERC.       |                |               |

**X/X Por el devengo de los intereses hasta la fecha de cancelación**
"""
        # 2. Cancelación de capital e intereses
        asiento2 = f"""
### 2️⃣ Cancelación del capital e intereses del préstamo

| CUENTA | DENOMINACIÓN                              | DEBE           | HABER         |
|--------|-------------------------------------------|----------------|---------------|
| 45     | OBLIGACIONES FINANCIERAS                     | {format_currency(monto)} |   |
| 451    | PRESTAMOS                                    |                |               |
| 45     | OBLIGACIONES FINANCIERAS                     | {format_currency(interes)} |   |
| 455    | COSTOS DE FINANCIACIÓN POR PAGAR             |                |               |
| 4551   | PRESTAMOS                                    |                |               |
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO           |                | {format_currency(monto + interes)} |
| 104    | CUENTAS CORRIENTES EN INST. FINANC.          |                |               |
| 1041   | CUENTAS CORRIENTES OPERATIVAS                |                |               |

**X/X Por la cancelación de interés y capital**
"""
        # 3. Extorno de intereses a devengar
        asiento3 = f"""
### 3️⃣ Extorno de los intereses a devengar

| CUENTA | DENOMINACIÓN                              | DEBE           | HABER         |
|--------|-------------------------------------------|----------------|---------------|
| 45     | OBLIGACIONES FINANCIERAS                     | {format_currency(interes)} |   |
| 451    | PRESTAMOS                                    |                |               |
| 37     | ACTIVO DIFERIDO                           |                | {format_currency(interes)} |
| 373    | INTERESES DIFERIDOS                       |                |               |
| 3731   | INT. NO DEVEN. EN TRANSC. CON TERC.       |                |               |

**X/X Por el extorno de los intereses a devengar**
"""
        return asiento1 + asiento2 + asiento3

    def _asiento_prestamo_bancario(self, monto, interes, partes, glosa, cuotas_pagar=1, cuotas_totales=12):
        """
        Genera el asiento contable para un préstamo financiero bancario (PCGE)
        y el pago de las primeras N cuotas (por defecto 1, pero puede ser 3, etc.).
        Todo es dinámico y profesional.
        """
        # Validación y asignación dinámica
        if not monto or monto <= 0:
            return "Por favor indica el monto del préstamo para generar el asiento contable."
        if not interes or interes <= 0:
            interes = monto * 0.10  # 10% anual por defecto si no se indica
        if not cuotas_totales or cuotas_totales < cuotas_pagar:
            cuotas_totales = 12  # Por defecto 12 cuotas

        amortizacion_cuota = round(monto / cuotas_totales, 2)
        interes_cuota = round(interes / cuotas_totales, 2)
        cuota_total = round(amortizacion_cuota + interes_cuota, 2)
        glosa_final = glosa or "Por el préstamo financiero recibido."

        # 1️⃣ Registro inicial del préstamo financiero
        asiento1 = f"""
### 1️⃣ Registro inicial del préstamo financiero

| CUENTA | DENOMINACIÓN                              | DEBE           | HABER         |
|--------|-------------------------------------------|----------------|---------------|
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO       | {format_currency(monto)} |               |
| 104    | CUENTAS CORRIENTES EN INST. FINANC.       |                |               |
| 1041   | CUENTAS CORRIENTES OPERATIVAS                |                |               |
| 37     | ACTIVO DIFERIDO                           | {format_currency(interes)} |               |
| 373    | INTERESES DIFERIDOS                       |                |               |
| 3731   | INT. NO DEVEN. EN TRANSC. CON TERC.       |                |               |
| 45     | OBLIGACIONES FINANCIERAS                     |                | {format_currency(monto)} |
| 451    | PREST. DE INST. FINANC. Y OTR. ENT.       |                |               |
| 4511   | INSTITUCIONES FINANCIERAS                 |                |               |
| 45     | OBLIGACIONES FINANCIERAS                  |                | {format_currency(interes)} |
| 455    | COSTOS DE FINANCIACIÓN POR PAGAR          |                |               |
| 4551   | PREST. DE INST. FINANC. Y OTR. ENT.       |                |               |
| 45511  | INSTITUCIONES FINANCIERAS                 |                |               |

**X/X {glosa_final}**
"""

        # Generar asientos para cada cuota solicitada
        asientos_cuotas = ""
        for i in range(1, cuotas_pagar + 1):
            asientos_cuotas += f"""
### {2*i}️⃣ Devengo del interés de la cuota {i}

| CUENTA | DENOMINACIÓN                              | DEBE           | HABER         |
|--------|-------------------------------------------|----------------|---------------|
| 67     | GASTOS FINANCIEROS                        | {format_currency(interes_cuota)} |               |
| 673    | INTERES. POR PREST. Y OTRAS OBLIG.        |                |               |
| 6731   | PREST. DE INST. FINANC. Y OTRAS ENT.      |                |               |
| 37     | ACTIVO DIFERIDO                           |                | {format_currency(interes_cuota)} |
| 373    | INTERESES DIFERIDOS                       |                |               |
| 3731   | INT. NO DEVEN. EN TRANSC. CON TERC.       |                |               |

**X/X Por el devengo de los intereses de la cuota {i}**

### {2*i+1}️⃣ Cancelación de la cuota {i}

| CUENTA | DENOMINACIÓN                              | DEBE           | HABER         |
|--------|-------------------------------------------|----------------|---------------|
| 45     | OBLIGACIONES FINANCIERAS                  | {format_currency(amortizacion_cuota)} |               |
| 451    | PREST. DE INST. FINANC. Y OTR. ENT.       |                |               |
| 4511   | INSTITUCIONES FINANCIERAS                 |                |               |
| 45     | OBLIGACIONES FINANCIERAS                  | {format_currency(interes_cuota)} |               |
| 455    | COSTOS DE FINANCIACIÓN POR PAGAR          |                |               |
| 4551   | PREST. DE INST. FINANC. Y OTR. ENT.       |                |               |
| 45511  | INSTITUCIONES FINANCIERAS                 |                |               |
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO        |                | {format_currency(cuota_total)} |
| 104    | CUENTAS CORRIENTES EN INST. FINANC.       |                |               |
| 1041   | CUENTAS CORRIENTES OPERATIVAS                |                |               |

**X/X Por la cancelación de la cuota {i}**
"""

        return asiento1 + asientos_cuotas

    def _calcular_igv(self, monto, incluido_igv=False):
        tasa_igv = 0.18
        if incluido_igv:
            base = round(monto / (1 + tasa_igv), 2)
            igv = round(monto - base, 2)
            total = monto
        else:
            base = monto
            igv = round(monto * tasa_igv, 2)
            total = round(base + igv, 2)
        return base, igv, total

    def _asiento_compra(self, monto, partes, glosa):
        if monto == 0:
            return "❌ No se detectó el monto de la compra. Ejemplo: 'compra de mercadería de 2,500 más IGV' o 'compra de teclados por 590 incluido IGV'."

        q = (glosa or "").lower()
        incluido_igv = "incluido igv" in q or "con igv" in q or "igv incluido" in q

        # Detectar tipo de compra según palabras clave
        cuenta_gasto, subcuenta, subsubcuenta = "60", "601", "6011"
        descripcion, detalle = "COMPRAS", "MERCADERÍAS"

        es_servicio = cuenta_gasto == "63"

        base, igv, total = self._calcular_igv(monto, incluido_igv=incluido_igv)

        # Buscar número de factura en el texto
        match_factura = re.search(r'(factura electrónica|factura|fv[-\s]?\d{2,}-\d+)', q, re.I)
        factura = match_factura.group(0) if match_factura else ""

        glosa_final = f"Por el registro de la compra de mercadería{' según ' + factura if factura else ''}."

        asiento1 = f"""
## 🛒 Asiento Contable: Compra de mercadería

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 60     | COMPRAS      | {format_currency(base)} |   |
| 601    | MERCADERÍAS  |      |   |
| 6011   | MERCADERÍAS  |      |   |
| 40     | TRIB. CONT. Y APORTES AL SIST. DE PENS. Y DE SALUD POR PAG. | {format_currency(igv)} |   |
| 401    | GOBIERNO CENTRAL |   |   |
| 4011   | IMPUESTO GENERAL A LAS VENTAS |   |   |
| 40111  | IGV – CUENTA PROPIA |   |   |
| 42     | CUENTAS POR PAGAR COMERCIALES TERCEROS |   | {format_currency(total)} |
| 421    | FACTURAS, BOLETAS Y OTROS COMPROBANTES POR PAGAR |   |   |
| 4212   | EMITIDAS |   |   |

**X/X {glosa_final}**

### Detalle del cálculo:
- Base Imponible: {format_currency(base)}
- IGV (18%): {format_currency(igv)}
- Total: {format_currency(total)}
"""

        asiento2 = f"""
| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|--------------|------|-------|
| 20     | MERCADERÍAS  | {format_currency(base)} |   |
| 201    | MERCADERÍAS  |      |   |
| 2011   | MERCADERÍAS  |      |   |
| 20111  | COSTO        |      |   |
| 61     | VARIACIÓN DE INVENTARIOS |   | {format_currency(base)} |
| 611    | MERCADERÍAS  |   |   |
| 6111   | MERCADERÍAS  |   |   |

**X/X Por el ingreso de la mercadería al almacén.**
"""

        return asiento1 + asiento2
    

# Instancia global
asientos_contables = AsientosContables()