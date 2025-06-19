import re
from ...core.utils import format_currency

class AsientosContables:
    """Generador universal de asientos contables dinámicos"""

    def _extract_amount(self, query: str) -> float:
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

    async def generate_response(self, query: str, context, metadata) -> str:
        q = query.lower()
        monto = self._extract_amount(query)
        interes = self._extract_interest(query, monto)
        partes = self._extract_partes(query)
        glosa = self._extract_glosa(query)



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
            return self._asiento_prestamo_bancario(monto, interes, partes, glosa)
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

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|-----------------------------------------------|------|-------|
| 67     | GASTOS FINANCIEROS                           | {format_currency(interes)} |   |
| 673    | INTERESES POR PRESTAMOS                      |   |   |
| 37     | ACTIVO DIFERIDO                              |   | {format_currency(interes)} |
| 373    | INTERESES DIFERIDOS                          |   |   |
| 3731   | INT. NO DEVEN. EN TRANSC. CON TERC.          |   |   |

**X/X Por el devengo de los intereses hasta la fecha de cancelación**
"""
        # 2. Cancelación de capital e intereses
        asiento2 = f"""
### 2️⃣ Cancelación del capital e intereses del préstamo

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|-----------------------------------------------|------|-------|
| 45     | OBLIGACIONES FINANCIERAS                     | {format_currency(monto)} |   |
| 451    | PRESTAMOS                                    |   |   |
| 45     | OBLIGACIONES FINANCIERAS                     | {format_currency(interes)} |   |
| 455    | COSTOS DE FINANCIACIÓN POR PAGAR             |   |   |
| 4551   | PRESTAMOS                                    |   |   |
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO           |   | {format_currency(monto + interes)} |
| 104    | CUENTAS CORRIENTES EN INST. FINANC.          |   |   |
| 1041   | CUENTAS CORRIENTES OPER.                     |   |   |

**X/X Por la cancelación de interés y capital**
"""
        # 3. Extorno de intereses a devengar
        asiento3 = f"""
### 3️⃣ Extorno de los intereses a devengar

| CUENTA | DENOMINACIÓN | DEBE | HABER |
|--------|-----------------------------------------------|------|-------|
| 45     | OBLIGACIONES FINANCIERAS                     | {format_currency(interes)} |   |
| 451    | PRESTAMOS                                    |   |   |
| 37     | ACTIVO DIFERIDO                              |   | {format_currency(interes)} |
| 373    | INTERESES DIFERIDOS                          |   |   |
| 3731   | INT. NO DEVEN. EN TRANSC. CON TERC.          |   |   |

**X/X Por el extorno de los intereses a devengar**
"""
        return asiento1 + asiento2 + asiento3

    def _asiento_prestamo_bancario(self, monto, interes, partes, glosa):
        """
        Asiento profesional para préstamo financiero bancario (PCGE) y pago de la primera cuota.
        Si no se pasan los valores, usa los del ejemplo.
        """
        # Valores por defecto si no se pasan
        if not monto:
            monto = 10000
        if not interes:
            interes = monto * 0.15  # 15% anual

        cuotas = 12
        amortizacion_cuota = round(monto / cuotas, 2)
        interes_cuota = round(interes / cuotas, 2)
        cuota_total = round(amortizacion_cuota + interes_cuota, 2)
        glosa_final = glosa or "Por el préstamo financiero recibido."

        # 1️⃣ Registro inicial del préstamo financiero
        asiento1 = f"""
### 1️⃣ Registro inicial del préstamo financiero

| CUENTA | DENOMINACIÓN                              | DEBE           | HABER         |
|--------|-------------------------------------------|----------------|---------------|
| 10     | EFECTIVO Y EQUIVALENTE DE EFECTIVO       | {format_currency(monto)} |               |
| 104    | CUENTAS CORRIENTES EN INST. FINANC.       |                |               |
| 1041   | CUENTAS CORRIENTES OPER.                  |                |               |
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

        # 2️⃣ Devengo del interés de la primera cuota
        asiento2 = f"""
### 2️⃣ Devengo del interés de la primera cuota

| CUENTA | DENOMINACIÓN                              | DEBE           | HABER         |
|--------|-------------------------------------------|----------------|---------------|
| 67     | GASTOS FINANCIEROS                        | {format_currency(interes_cuota)} |               |
| 673    | INTERES. POR PREST. Y OTRAS OBLIG.        |                |               |
| 6731   | PREST. DE INST. FINANC. Y OTRAS ENT.      |                |               |
| 37     | ACTIVO DIFERIDO                           |                | {format_currency(interes_cuota)} |
| 373    | INTERESES DIFERIDOS                       |                |               |
| 3731   | INT. NO DEVEN. EN TRANSC. CON TERC.       |                |               |

**X/X Por el devengo de los intereses de la primera cuota**
"""

        # 3️⃣ Cancelación de la primera cuota
        asiento3 = f"""
### 3️⃣ Cancelación de la primera cuota

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
| 1041   | CUENTAS CORRIENTES OPER.                  |                |               |

**X/X Por la cancelación de la primera cuota**
"""

        return asiento1 + asiento2 + asiento3

    def _asiento_interes_diferido(self, monto, tipo="por_cobrar"):
        """
        Genera los asientos contables para el registro del interés diferido según PCGE 2019.
        tipo: "por_cobrar" o "por_pagar"
        """
        if tipo == "por_cobrar":
            return f"""
### 1️⃣ Intereses por Cobrar Diferidos

| CÓDIGO | CUENTA                        | DEBE      | HABER     |
|--------|-------------------------------|-----------|-----------|
| 1212   | Intereses por cobrar          | {format_currency(monto)} |           |
| 761    | Ingresos financieros          |           | {format_currency(monto)} |

**X/X Registro del devengo de intereses por cobrar diferidos.**
"""
        else:
            return f"""
### 2️⃣ Intereses por Pagar Diferidos

| CÓDIGO | CUENTA                        | DEBE      | HABER     |
|--------|-------------------------------|-----------|-----------|
| 671    | Gastos financieros            | {format_currency(monto)} |           |
| 4112   | Intereses por pagar           |           | {format_currency(monto)} |

**X/X Registro del devengo de intereses por pagar diferidos.**
"""
# Instancia global
asientos_contables = AsientosContables()