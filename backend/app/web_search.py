import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import re
from typing import List, Dict

def buscar_en_web(query: str, max_results: int = 3) -> List[Dict]:
    """Busca información actualizada en la web usando DuckDuckGo."""
    try:
        ddgs = DDGS()
        # Agregar términos específicos para mejorar la búsqueda contable
        query_contable = f"{query} contabilidad perú SUNAT PCGE"
        
        results = []
        search_results = ddgs.text(query_contable, max_results=max_results)
        
        for result in search_results:
            # Extraer contenido de la página
            content = extraer_contenido_pagina(result.get('href', ''))
            if content:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'snippet': result.get('body', ''),
                    'content': content[:1000]  # Limitar contenido
                })
        
        return results
    except Exception as e:
        print(f"Error en búsqueda web: {e}")
        return []

def extraer_contenido_pagina(url: str) -> str:
    """Extrae contenido relevante de una página web."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)  # ⬅️ Reducir timeout a 5 segundos
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remover elementos no deseados
        for elemento in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            elemento.decompose()
        
        # Extraer texto de párrafos y divs principales
        texto = ""
        for tag in soup.find_all(['p', 'div', 'article', 'section']):
            if tag.get_text(strip=True):
                texto += tag.get_text(strip=True) + "\n"
        
        # Limpiar y normalizar texto
        texto = re.sub(r'\s+', ' ', texto)
        return texto.strip()
        
    except requests.exceptions.Timeout:
        print(f"Timeout extrayendo contenido de {url}")
        return ""
    except requests.exceptions.ConnectionError:
        print(f"Error de conexión extrayendo contenido de {url}")
        return ""
    except Exception as e:
        print(f"Error extrayendo contenido de {url}: {e}")
        return ""

def buscar_normativa_sunat(consulta: str) -> List[Dict]:
    """Búsqueda específica en sitios de SUNAT y normativa tributaria."""
    sitios_oficiales = [
        "site:sunat.gob.pe",
        "site:mef.gob.pe", 
        "site:sbs.gob.pe",
        "site:smv.gob.pe"
    ]
    
    resultados = []
    for sitio in sitios_oficiales:
        query = f"{consulta} {sitio}"
        try:
            ddgs = DDGS()
            search_results = ddgs.text(query, max_results=2)
            for result in search_results:
                resultados.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'snippet': result.get('body', ''),
                    'source': 'Oficial'
                })
        except:
            continue
    
    return resultados