import os
import re
import json
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import openai

# ─── Carga de la clave de entorno y configuración OpenAI ────────────────────────
load_dotenv()  # lee .env en backend/
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY no configurada en .env")

# ─── 1) Extraer texto de PDF ────────────────────────────────────────────────────
def leer_documento(path: str) -> str:
    """Extrae todo el texto de cada página de un PDF."""
    reader = PdfReader(path)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() or ""
    return texto

# ─── 2) Convertir cualquier archivo a texto plano normalizado ───────────────────
def text_to_plain(path: str) -> str:
    """Lee PDF o TXT, extrae su texto y lo normaliza."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        raw = leer_documento(path)
    else:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    text = raw.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

# ─── 3) Limpiar tabla de contenido ──────────────────────────────────────────────
def limpiar_tabla_contenido(texto: str) -> str:
    """Elimina la sección de tabla de contenido, si existe."""
    match = re.search(
        r'(Contenido|Tabla de contenido)[\s\S]{0,3000}?(\n\s*\d+\s*\n)',
        texto, re.IGNORECASE
    )
    if match:
        return texto[match.end():].lstrip()
    return texto

# ─── 4) Dividir texto en secciones por títulos comunes ──────────────────────────
def dividir_por_secciones(texto: str) -> list[dict]:
    """Divide el texto en secciones usando títulos frecuentes de documentos contables."""
    texto = limpiar_tabla_contenido(texto)
    patron = re.compile(
        r'(?P<titulo>'
          # Títulos generales
          r'PR[ÓO]LOGO|INTRODUCCI[ÓO]N|CONCEPTO|'
          r'CAP[ÍI]TULO\s+\w+.*?|DEFINICI[ÓO]N|OBJETIVOS?|'
          r'RESUMEN|CONCLUSI[ÓO]N(?:ES)?|ANEXOS?|BIBLIOGRAF[ÍI]A|'
          # Títulos contables específicos
          r'PLAN\s+CONTABLE|PCGE|CUENTAS?\s+DEL?\s+ACTIVO|CUENTAS?\s+DEL?\s+PASIVO|'
          r'CUENTAS?\s+DEL?\s+PATRIMONIO|CUENTAS?\s+DE\s+RESULTADOS?|'
          r'CONSTITUCI[ÓO]N\s+DE\s+EMPRESAS?|SOCIEDAD\s+AN[ÓO]NIMA|'
          r'CAPITAL\s+SOCIAL|APORTES?|RESERVAS?|UTILIDADES?|'
          r'ASIENTOS?\s+CONTABLES?|LIBRO\s+DIARIO|MAYOR|'
          r'ESTADOS?\s+FINANCIEROS?|BALANCE|GANANCIAS?\s+Y\s+P[EÉ]RDIDAS?|'
          r'FLUJO\s+DE\s+EFECTIVO|PATRIMONIO\s+NETO|'
          # Títulos de normativa
          r'LEY\s+GENERAL\s+DE\s+SOCIEDADES?|SUNAT|TRIBUTACI[ÓO]N|'
          r'IGV|IMPUESTO\s+A\s+LA\s+RENTA|IR|'
          r'PROCEDIMIENTOS?|FORMULARIOS?|DECLARACIONES?'
        r')\s*\n',
        re.IGNORECASE
    )
    
    matches = list(patron.finditer(texto))
    if not matches:
        return [{"titulo": "Documento completo", "contenido": texto}]
    
    secciones = []
    indices = [m.start() for m in matches] + [len(texto)]
    titulos = [m.group("titulo").strip() for m in matches]
    
    for i, titulo in enumerate(titulos):
        inicio = indices[i]
        fin    = indices[i+1]
        contenido = texto[inicio:fin].strip()
        secciones.append({"titulo": titulo, "contenido": contenido})
    
    return secciones

# ─── 5) Generar embeddings vía OpenAI ───────────────────────────────────────────
def generar_embeddings(texto: str) -> list[float]:
    """Llama al endpoint embeddings.create() de openai-python>=1.0.0"""
    # Rough estimate: 1 token ≈ 0.75 words
    estimated_tokens = len(texto.split()) * 1.33
    
    if estimated_tokens > 8000:  # Safety margin below 8192 limit
        # Truncate text if too long
        words = texto.split()
        texto = ' '.join(words[:6000])  # Keep approximately 8000 tokens
    
    resp = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=[texto]
    )
    return resp.data[0].embedding

# ─── 6) (Opcional) Preprocesar todo un directorio ──────────────────────────────
def procesar_documentos(directorio: str, salida: str = "embeddings.json"):
    """Procesa todos los PDFs en un directorio y guarda embeddings en un JSON."""
    documentos = []
    embs       = []
    for archivo in os.listdir(directorio):
        if not archivo.lower().endswith(".pdf"):
            continue
        ruta  = os.path.join(directorio, archivo)
        texto = text_to_plain(ruta)
        documentos.append({"file": archivo, "text": texto})
        embs.append({"file": archivo, "vector": generar_embeddings(texto)})
    with open(salida, "w", encoding="utf-8") as f:
        json.dump({"docs": documentos, "embs": embs}, f, ensure_ascii=False, indent=2)
    print(f"Procesados {len(documentos)} archivos. Embeddings guardados en {salida}.")

# ─── 7) Extraer autor del PDF o texto ──────────────────────────────────────────
def extraer_autor(path: str) -> str | None:
    """Intenta extraer el autor de los metadatos del PDF."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        try:
            reader = PdfReader(path)
            meta = reader.metadata
            autor = getattr(meta, "author", None)
            if autor and autor.strip():
                return autor.strip()
        except Exception:
            pass
    return None

def extraer_autor_texto(texto: str) -> str | None:
    """Busca el autor en el texto plano (líneas iniciales)."""
    patrones = [
        r"Autor(?:es)?:\s*(.+)",
        r"Por:\s*(.+)",
        r"Escrito por\s*:?(.+)",
    ]
    for linea in texto.splitlines()[:20]:
        for patron in patrones:
            m = re.search(patron, linea, re.IGNORECASE)
            if m:
                return m.group(1).strip()
    return None

# AGREGAR ESTA FUNCIÓN AL FINAL:
def extraer_tipo_documento(texto: str) -> str:
    """Identifica el tipo de documento contable basado en su contenido."""
    texto_lower = texto.lower()
    
    if any(kw in texto_lower for kw in ["plan contable", "pcge", "cuentas del activo"]):
        return "Plan Contable"
    elif any(kw in texto_lower for kw in ["constitución", "sociedad anónima", "capital social"]):
        return "Constitución de Empresas"
    elif any(kw in texto_lower for kw in ["asiento contable", "debe", "haber", "libro diario"]):
        return "Registro Contable"
    elif any(kw in texto_lower for kw in ["balance", "estado de resultados", "flujo de efectivo"]):
        return "Estados Financieros"
    elif any(kw in texto_lower for kw in ["ley general", "sunat", "tributación", "igv"]):
        return "Normativa Tributaria"
    else:
        return "Documento General"