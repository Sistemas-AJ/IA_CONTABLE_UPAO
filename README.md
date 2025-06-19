# 🤖 IA_CONTABLE – Chatbot Contable y Financiero

**Desarrollador:**  
**Adrian Alejandro Ruiz Carreño**  
Edad: 19 
CEO y dueño de **SCORPIONS**  
Desarrollador de la empresa **Adolfo Jurado**

---

## 🚀 Tecnologías

- **Frontend:** React + TailwindCSS  
- **Backend:** FastAPI (Python)  
- **Procesamiento de documentos:** PyPDF2   
- **Vectorstore:** FAISS  
- **Base de datos:** SQLite (por defecto)

---

## 📋 Requisitos

- **Python 3.11+**
- **Node.js 20+** (incluye npm)
- **Clave de OpenAI** con acceso a GPT-4o
- Conexión a Internet para llamadas a la API de OpenAI

---

## 🔧 Instalación y puesta en marcha

### 1. Configura variables de entorno

En la raíz del proyecto (`IA_CONTABLE/`), crea un archivo `.env`:

```dotenv
OPENAI_API_KEY=sk-<tu_clave_openai>
```

---

### 2. Backend (FastAPI + OpenAI + PyPDF2)

```bash
cd IA_CONTABLE/backend/app

# Instala dependencias
pip install --upgrade pip
pip install -r ../requirements.txt

# Ejecuta el servidor
python run.py
```

- Acceso backend: [http://localhost:8000](http://localhost:8000)
- Documentación Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 3. Frontend (React + TailwindCSS)

```bash
cd IA_CONTABLE/frontend

# Instala dependencias
npm install

# Asegúrate que en package.json:
#   "proxy": "http://localhost:8000"
npm start
```

- Acceso frontend: [http://localhost:3000](http://localhost:3000)

---

## ▶️ Uso

### Modo Entrenamiento

- Activa el modo “Entrenamiento” en la interfaz.
- Sube un archivo `.pdf` o `.txt` (PCGE, manuales, etc.).
- Espera el mensaje de confirmación.

### Chat Contable

- Escribe tu consulta en el área de texto.
- Pulsa **Enviar**.
- La respuesta aparecerá formateada en Markdown (tablas, listas, explicaciones), cumpliendo con el PCGE 2019 y la normativa tributaria peruana.

---

## 🏆 Buenas prácticas

- Mantén tu `.env` fuera del control de versiones (`.gitignore`).
- Para producción, elimina `--reload` de Uvicorn y ajusta CORS a tu dominio.
- Actualiza dependencias regularmente:
  ```bash
  pip install --upgrade fastapi uvicorn openai
  npm audit fix
  ```

---

## 📚 Ejemplos de consulta

- **Asientos contables:**  
  `"Registra un préstamo bancario de S/ 10,000 al 15% anual"`
- **Cálculos:**  
  `"Calcula CTS de S/ 3,000"`
- **Ratios financieros:**  
  `"Calcula ROE con utilidad S/ 15,000 y patrimonio S/ 100,000"`
- **Explicaciones:**  
  `"¿Qué es el activo corriente?"`

---

## 💬 Soporte

- **Email:** soporte@upao.edu.pe
- **Sitio web:** https://upao.edu.pe

---

**¿Listo para automatizar tu contabilidad?**
# IA_CONTABLE_UPAO
