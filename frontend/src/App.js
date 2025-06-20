import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { PaperClipIcon, UserIcon } from '@heroicons/react/24/outline';
import { BlockMath, InlineMath } from 'react-katex';

// Importar componentes
import Header from './components/Header';
import ChatWindow from './components/ChatWindow';
import InputBox from './components/InputBox';
import UploadSection from './components/UploadSection';
import LoadingProgress from './components/LoadingProgress';


function App() {
  const [sessionId] = useState(uuidv4());
  const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState('');
  const [loading, setLoading] = useState(false);
  
  // Estados para progreso de carga
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [loadingStage, setLoadingStage] = useState('analyzing');
  
  const [userContext, setUserContext] = useState({});

  // Para mostrar/ocultar el menú de subida
  const [showUploadMenu, setShowUploadMenu] = useState(false);
  const [uploadMode, setUploadMode] = useState('train');
  const [uploadStatus, setUploadStatus] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);

  // Cargar contexto del usuario al iniciar
  useEffect(() => {
    loadUserContext();
  }, [sessionId]);

  const loadUserContext = async () => {
    try {
      const res = await fetch(`/api/user-context/${sessionId}`);
      if (res.ok) {
        const data = await res.json();
        setUserContext(data.context || {});
      }
    } catch (error) {
      console.error('Error cargando contexto:', error);
    }
  };

  // Función para simular progreso
  const simulateProgress = () => {
    const stages = [
      { key: 'analyzing', duration: 2000, progress: 15 },
      { key: 'searching_docs', duration: 3000, progress: 35 },
      { key: 'searching_web', duration: 2500, progress: 55 },
      { key: 'processing_examples', duration: 2000, progress: 75 },
      { key: 'generating', duration: 4000, progress: 95 },
      { key: 'finalizing', duration: 1000, progress: 100 }
    ];

    let currentProgress = 0;
    let stageIndex = 0;

    const updateProgress = () => {
      if (stageIndex < stages.length) {
        const stage = stages[stageIndex];
        setLoadingStage(stage.key);
        
        const increment = (stage.progress - currentProgress) / (stage.duration / 100);
        
        const progressInterval = setInterval(() => {
          currentProgress += increment;
          setLoadingProgress(Math.min(currentProgress, stage.progress));
          
          if (currentProgress >= stage.progress) {
            clearInterval(progressInterval);
            stageIndex++;
            
            if (stageIndex < stages.length) {
              setTimeout(updateProgress, 200);
            }
          }
        }, 100);
      }
    };

    updateProgress();
  };

  // Handler de subida
  const handleFileUpload = file => {
    if (!file) return;

    setUploadStatus('Subiendo...');
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', sessionId);

    const xhr = new XMLHttpRequest();

    xhr.upload.onprogress = e => {
      if (e.lengthComputable) {
        const percentComplete = (e.loaded / e.total) * 100;
        setUploadProgress(percentComplete);
      }
    };

    xhr.onload = () => {
      if (xhr.status === 200) {
        try {
          const response = JSON.parse(xhr.responseText);
          if (response.success) {
            setUploadStatus('✅ Archivo subido y procesado correctamente.');
            setUploadProgress(100);
          } else if (response.is_duplicate) {
            setUploadProgress(100);
            setUploadStatus('Este archivo ya fue subido.');
          }
        } catch (e) {
          setUploadStatus('❌ Error procesando respuesta del servidor.');
        }
      } else {
        setUploadStatus('❌ Error al subir el archivo.');
        setUploadProgress(0);
      }
    };

    xhr.onerror = () => {
      setUploadStatus('❌ Error al subir el archivo.');
      setUploadProgress(0);
    };

    // Usar la ruta correcta según el modo
    const endpoint = uploadMode === 'train' ? '/api/upload/file' : '/api/upload/file';
    xhr.open('POST', `${endpoint}?session_id=${sessionId}`);
    xhr.send(formData);
  };

  // Función principal para enviar mensajes
  const sendMessage = async () => {
    if (!userMessage.trim()) return;

    // Agregar mensaje del usuario
    const newUserMessage = { role: 'user', content: userMessage };
    setMessages(m => [...m, newUserMessage]);

    // Tomar los últimos 5 mensajes (sin incluir el que se está enviando)
    const lastMessages = [...messages, newUserMessage].slice(-5);

    setLoading(true);
    setLoadingProgress(0);
    setLoadingStage('analyzing');
    simulateProgress();

    try {
      const res = await fetch('/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          session_id: sessionId,
          user_context: userContext,
          history: lastMessages // <-- Nuevo campo
        })
      });
      
      const data = await res.json();
      
      // Completar progreso
      setLoadingProgress(100);
      setLoadingStage('finalizing');
      
      // Pausa para mostrar 100%
      setTimeout(() => {
        if (data.response) {
          setMessages(m => [...m, { role: 'assistant', content: data.response }]);
          loadUserContext();
        }
        setUserMessage('');
        setLoading(false);
        setLoadingProgress(0);
      }, 500);
      
    } catch (error) {
      console.error('Error:', error);
      
      // Manejo de errores con progreso
      setLoadingProgress(100);
      setTimeout(() => {
        setMessages(m => [
          ...m,
          { role: 'assistant', content: '❌ **Error de conexión**\n\nNo pude procesar tu consulta. Por favor verifica:\n- Que el servidor esté funcionando\n- Tu conexión a internet\n- Intenta nuevamente en unos momentos' }
        ]);
        setLoading(false);
        setLoadingProgress(0);
      }, 500);
    }
  };

  return (
    <div className="bg-upaoGray min-h-screen w-full">
      {/* Header */}
      <div className="fixed top-0 left-0 w-full z-50">
        <Header />
      </div>
      
      {/* Panel de contexto del usuario */}
      {Object.keys(userContext).length > 0 && (
        <div className="fixed top-20 right-4 w-64 bg-white rounded-lg shadow-lg p-4 z-40">
          <div className="flex items-center gap-2 mb-2">
            <UserIcon className="h-5 w-5 text-upaoBlue" />
            <span className="font-semibold text-sm text-upaoBlue">Tu Contexto</span>
          </div>
          <div className="space-y-1">
            {Object.entries(userContext).map(([key, value]) => (
              <div key={key} className="text-xs">
                <span className="font-medium">{key}:</span> {value}
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Chat */}
      <div className="flex flex-col items-center w-full pt-36 pb-9 gap-6">
        <div className="flex-1 w-full flex justify-center overflow-y-auto px-4 sm:px-16" style={{ minHeight: 'calc(100vh - 7rem)' }}>
          <div className="w-full max-w-4xl">
            <ChatWindow messages={messages} />
          </div>
        </div>
      </div>
      
      {/* Barra de envío */}
      <div className="fixed bottom-0 left-0 w-full bg-white border-t z-50 flex justify-center shadow-lg">
        <div className="w-full max-w-3xl flex items-center gap-2 px-2 py-1 relative">
          {/* Indicador de modo actual */}
          <div className="absolute left-2 -top-8 flex items-center gap-2">
            <span className={`px-3 py-1 rounded-full text-xs font-semibold shadow
              ${uploadMode === 'train' ? 'bg-blue-100 text-blue-700 border border-blue-300' : 'bg-green-100 text-green-700 border border-green-300'}`}>
              {uploadMode === 'train' ? 'Modo Entrenamiento' : 'Modo Contexto'}
            </span>
          </div>
          
          {/* Botón de adjuntar */}
          <button
            className="p-1 rounded hover:bg-gray-100 border"
            onClick={() => setShowUploadMenu(v => !v)}
            title="Adjuntar documento"
            type="button"
          >
            <PaperClipIcon className="h-5 w-5 text-upaoBlue" />
          </button>
          
          {/* Menú de subida */}
          {showUploadMenu && (
            <div className="absolute bottom-14 left-2 bg-white border rounded shadow-lg p-4 z-50 w-80">
              <div className="flex gap-2 mb-2">
                <button
                  className={`flex-1 px-2 py-1 rounded ${uploadMode === 'train' ? 'bg-upaoBlue text-white' : 'bg-gray-100 text-upaoBlue'}`}
                  onClick={() => setUploadMode('train')}
                >
                  Entrenar
                </button>
                <button
                  className={`flex-1 px-2 py-1 rounded ${uploadMode === 'context' ? 'bg-upaoBlue text-white' : 'bg-gray-100 text-upaoBlue'}`}
                  onClick={() => setUploadMode('context')}
                >
                  Contexto
                </button>
              </div>
              <UploadSection
                enabled={true}
                onFile={handleFileUpload}
                status={uploadStatus}
                progress={uploadProgress}
              />
              <button
                className="mt-2 text-xs text-gray-500 underline"
                onClick={() => setShowUploadMenu(false)}
              >
                Cerrar
              </button>
            </div>
          )}
          
          {/* InputBox */}
          <div className="flex-1">
            <InputBox
              value={userMessage}
              onChange={setUserMessage}
              onSend={sendMessage}
              loading={loading}
            />
          </div>
        </div>
      </div>

      {/* Componente de progreso de carga */}
      <LoadingProgress 
        progress={loadingProgress}
        stage={loadingStage}
        isVisible={loading}
      />
    </div>
  );
}

export default App;