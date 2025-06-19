import os
import sys

# Agregar el directorio backend al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.embedding_utils import procesar_documentos, leer_documento, dividir_por_secciones, extraer_autor, extraer_autor_texto
from app.vectorstore import add_text_chunk, save_index
import json

def procesar_y_entrenar_documentos(directorio: str = "uploads"):
    """
    Procesa todos los documentos en el directorio uploads y los agrega al sistema de vectores.
    Compatible con el nuevo sistema de chunks y FAISS.
    """
    
    if not os.path.exists(directorio):
        print(f"❌ El directorio {directorio} no existe")
        return
    
    archivos_pdf = [f for f in os.listdir(directorio) if f.lower().endswith('.pdf')]
    archivos_txt = [f for f in os.listdir(directorio) if f.lower().endswith('.txt')]
    
    if not archivos_pdf and not archivos_txt:
        print(f"❌ No se encontraron archivos PDF o TXT en {directorio}")
        return
    
    print(f"📁 Procesando {len(archivos_pdf)} archivos PDF y {len(archivos_txt)} archivos TXT...")
    
    total_chunks = 0
    documentos_procesados = []
    
    # Procesar archivos PDF
    for archivo in archivos_pdf:
        ruta_completa = os.path.join(directorio, archivo)
        print(f"📄 Procesando: {archivo}")
        
        try:
            # Leer el documento
            texto = leer_documento(ruta_completa)
            
            # Extraer metadatos
            autor = extraer_autor(ruta_completa) or extraer_autor_texto(texto)
            
            # Agregar información del título del documento
            add_text_chunk(archivo, f"Título del documento: {archivo}")
            if autor:
                add_text_chunk(archivo, f"Autor del documento: {autor}")
            
            # Dividir en secciones
            secciones = dividir_por_secciones(texto)
            
            # Agregar cada sección como chunk
            chunks_archivo = 0
            for seccion in secciones:
                contenido = seccion.get("contenido", "")
                if contenido.strip():  # Solo procesar secciones no vacías
                    add_text_chunk(archivo, contenido)
                    chunks_archivo += 1
            
            total_chunks += chunks_archivo
            documentos_procesados.append({
                "archivo": archivo,
                "tipo": "PDF",
                "chunks": chunks_archivo,
                "autor": autor
            })
            
            print(f"   ✅ {chunks_archivo} chunks procesados")
            
        except Exception as e:
            print(f"   ❌ Error procesando {archivo}: {str(e)}")
    
    # Procesar archivos TXT
    for archivo in archivos_txt:
        ruta_completa = os.path.join(directorio, archivo)
        print(f"📄 Procesando: {archivo}")
        
        try:
            # Leer archivo de texto
            with open(ruta_completa, "r", encoding="utf-8") as f:
                texto = f.read()
            
            # Extraer metadatos
            autor = extraer_autor_texto(texto)
            
            # Agregar información del título del documento
            add_text_chunk(archivo, f"Título del documento: {archivo}")
            if autor:
                add_text_chunk(archivo, f"Autor del documento: {autor}")
            
            # Dividir en secciones
            secciones = dividir_por_secciones(texto)
            
            # Agregar cada sección como chunk
            chunks_archivo = 0
            for seccion in secciones:
                contenido = seccion.get("contenido", "")
                if contenido.strip():  # Solo procesar secciones no vacías
                    add_text_chunk(archivo, contenido)
                    chunks_archivo += 1
            
            total_chunks += chunks_archivo
            documentos_procesados.append({
                "archivo": archivo,
                "tipo": "TXT",
                "chunks": chunks_archivo,
                "autor": autor
            })
            
            print(f"   ✅ {chunks_archivo} chunks procesados")
            
        except Exception as e:
            print(f"   ❌ Error procesando {archivo}: {str(e)}")
    
    # Guardar el índice FAISS
    save_index()
    
    # Generar reporte de procesamiento
    reporte = {
        "timestamp": str(datetime.now()),
        "total_documentos": len(documentos_procesados),
        "total_chunks": total_chunks,
        "documentos": documentos_procesados,
        "directorio": directorio
    }
    
    # Guardar reporte en JSON
    with open("reporte_procesamiento.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)
    
    # Mostrar resumen
    print(f"\n🎉 PROCESAMIENTO COMPLETADO")
    print(f"📊 Total documentos: {len(documentos_procesados)}")
    print(f"📊 Total chunks: {total_chunks}")
    print(f"💾 Índice FAISS actualizado")
    print(f"📄 Reporte guardado en: reporte_procesamiento.json")
    
    return reporte

def verificar_estado_vectorstore():
    """Verifica el estado actual del vectorstore"""
    from app.vectorstore import faiss_index
    from app.db import Session, chunks_table
    
    print("🔍 VERIFICANDO ESTADO DEL VECTORSTORE")
    
    # Verificar FAISS
    if faiss_index:
        print(f"📊 Vectores en FAISS: {faiss_index.ntotal}")
    else:
        print("❌ Índice FAISS no encontrado")
    
    # Verificar base de datos
    db = Session()
    try:
        total_chunks = db.execute("SELECT COUNT(*) FROM chunks").scalar()
        print(f"📊 Chunks en base de datos: {total_chunks}")
        
        # Mostrar fuentes únicas
        fuentes = db.execute("SELECT DISTINCT source FROM chunks").fetchall()
        print(f"📊 Documentos únicos: {len(fuentes)}")
        for fuente in fuentes[:10]:  # Mostrar solo los primeros 10
            print(f"   - {fuente[0]}")
        
        if len(fuentes) > 10:
            print(f"   ... y {len(fuentes) - 10} más")
            
    finally:
        db.close()

def limpiar_vectorstore():
    """Limpia completamente el vectorstore (usar con precaución)"""
    respuesta = input("⚠️ ¿Estás seguro de que quieres limpiar TODA la base de vectores? (escribir 'SI' para confirmar): ")
    
    if respuesta != "SI":
        print("❌ Operación cancelada")
        return
    
    from app.vectorstore import faiss_index, VECTOR_INDEX_PATH
    from app.db import Session, chunks_table
    
    # Limpiar base de datos
    db = Session()
    try:
        db.execute(chunks_table.delete())
        db.commit()
        print("✅ Base de datos limpiada")
    finally:
        db.close()
    
    # Recrear índice FAISS vacío
    import faiss
    from app.config import EMBED_DIM
    
    new_index = faiss.IndexFlatL2(EMBED_DIM)
    faiss.write_index(new_index, VECTOR_INDEX_PATH)
    print("✅ Índice FAISS recreado")

if __name__ == "__main__":
    from datetime import datetime
    
    print("🤖 GENERADOR DE EMBEDDINGS PARA IA CONTABLE")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == "procesar":
            directorio = sys.argv[2] if len(sys.argv) > 2 else "uploads"
            procesar_y_entrenar_documentos(directorio)
            
        elif comando == "verificar":
            verificar_estado_vectorstore()
            
        elif comando == "limpiar":
            limpiar_vectorstore()
            
        else:
            print("❌ Comando no reconocido")
            print("Uso:")
            print("  python generar_json.py procesar [directorio]")
            print("  python generar_json.py verificar")
            print("  python generar_json.py limpiar")
    else:
        # Ejecutar procesamiento por defecto
        procesar_y_entrenar_documentos("uploads")