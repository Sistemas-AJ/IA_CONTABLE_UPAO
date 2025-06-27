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
pip install -r ./requirements.txt

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



---

## 🖥️ Despliegue en VPS (Producción)

### 1. Requisitos VPS
- Ubuntu 22.04+ (recomendado)
- Acceso SSH y usuario con permisos sudo
- Dominio/subdominio apuntando a la IP del VPS
- **Python 3.11+** y **Node.js 20+** instalados
- Nginx instalado (`asegura`)

### 2. Clona el repositorio y sube los archivos
```bash
cd /home/ajsistemas/
git clone https://github.com/Sistemas-AJ/IA_CONTABLE_UPAO.git iacontable
cd iacontable
```

### 3. Variables de entorno (backend)
Crea `/home/ajsistemas/iacontable/backend/.env`:
```env
OPENAI_API_KEY=sk-<tu_clave_openai>
OPENAI_MODEL=gpt-4o
HOST=0.0.0.0
PORT=8000
RELOAD=false
ENVIRONMENT=production
```

### 4. Backend (FastAPI)
```bash
cd /home/ajsistemas/iacontable/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Ejecuta en modo producción (usar systemd/pm2 para servicio)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

### 5. Frontend (React)
```bash
cd /home/ajsistemas/iacontable/frontend
npm install
npm run build
```
Esto generará `/home/ajsistemas/iacontable/frontend/build/`.

### 6. Configuración de Nginx
Crea un archivo de configuración para tu sitio:
```nginx
server {
    listen 80;
    server_name iacontable.systempiura.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ajsistemas/iacontable/backend/static/;
    }

    location / {
        root /home/ajsistemas/iacontable/frontend/build/;
        try_files $uri /index.html;
    }
}
```

- cd `/home/ajsistemas/iacontable/`
- Habilita el sitio y recarga Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/iacontable /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. Acceso
- Frontend: http://iacontable.systempiura.com
- Backend API: http://iacontable.systempiura.com/api/
- Documentación Swagger: http://iacontable.systempiura.com/docs

---

## ✅ Checklist comunicación Frontend ↔ Backend en VPS

1. **CORS en FastAPI**
   - Asegúrate de permitir el dominio de producción en el backend. En `main.py` o donde configuras FastAPI:
     ```python
     from fastapi.middleware.cors import CORSMiddleware
     app.add_middleware(
         CORSMiddleware,
         allow_origins=["http://iacontable.systempiura.com"],  # o ["*"] para pruebas
         allow_credentials=True,
         allow_methods=["*"],
         allow_headers=["*"],
     )
     ```
   - Si usas varios entornos, puedes hacer que lea de una variable de entorno.

2. **Proxy en el frontend**
   - En `frontend/package.json` debe estar:
     ```json
     "proxy": "http://localhost:8000"
     ```
   - En producción, Nginx se encarga de redirigir `/api` al backend.

3. **Prueba de comunicación**
   - Sube el frontend (`npm run build`) y backend activos.
   - Accede a `http://iacontable.systempiura.com` y envía un mensaje en el chat.
   - Si el backend responde, la integración es correcta.
   - Si hay error CORS, revisa el punto 1.
   - Si hay error 502/404, revisa Nginx y que el backend esté corriendo.

4. **Debug**
   - Ver logs de Nginx: `sudo tail -f /var/log/nginx/error.log`
   - Ver logs del backend: `tail -f /home/ajsistemas/iacontable/backend/app/data/logs/app.log`

---

# ▶️ Uso local (desarrollo)

Repite los pasos de **Instalación y puesta en marcha**, pero usa `localhost` como dominio.

---
