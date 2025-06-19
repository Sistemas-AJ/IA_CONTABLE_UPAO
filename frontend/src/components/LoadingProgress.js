import React from 'react';

const LoadingProgress = ({ progress, stage, isVisible }) => {
  if (!isVisible) return null;

  const stages = [
    { key: 'analyzing', text: 'Analizando consulta...', icon: '🔍' },
    { key: 'searching_docs', text: 'Buscando en documentos...', icon: '📄' },
    { key: 'searching_web', text: 'Consultando información web...', icon: '🌐' },
    { key: 'processing_examples', text: 'Procesando ejemplos...', icon: '📚' },
    { key: 'generating', text: 'Generando asiento contable...', icon: '⚡' },
    { key: 'finalizing', text: 'Finalizando respuesta...', icon: '✅' }
  ];

  const currentStage = stages.find(s => s.key === stage) || stages[0];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4 shadow-2xl">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="text-4xl mb-2">{currentStage.icon}</div>
          <h3 className="text-lg font-semibold text-gray-800">
            Generando Tu pregunta Contable
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            Por favor espera mientras proceso tu consulta...
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between text-xs text-gray-600 mb-2">
            <span>Progreso</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div 
              className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        {/* Current Stage */}
        <div className="text-center">
          <div className="text-sm font-medium text-gray-700 mb-3">
            {currentStage.text}
          </div>
          
          {/* Animated dots */}
          <div className="flex justify-center space-x-1">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
          </div>
        </div>

        {/* Stage Progress */}
        <div className="mt-6">
          <div className="text-xs text-gray-500 mb-2">Etapas del proceso:</div>
          <div className="grid grid-cols-3 gap-2">
            {stages.map((stageItem, index) => {
              const isActive = stageItem.key === stage;
              const isCompleted = stages.findIndex(s => s.key === stage) > index;
              
              return (
                <div
                  key={stageItem.key}
                  className={`text-center p-2 rounded text-xs ${
                    isActive 
                      ? 'bg-blue-100 text-blue-700 border border-blue-300' 
                      : isCompleted 
                        ? 'bg-green-100 text-green-700' 
                        : 'bg-gray-100 text-gray-500'
                  }`}
                >
                  <div className="text-lg mb-1">{stageItem.icon}</div>
                  <div className="text-xs leading-tight">
                    {stageItem.text.split(' ')[0]}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Estimated time */}
        <div className="mt-4 text-center text-xs text-gray-500">
          ⏱️ Tiempo estimado: 10-15 segundos
        </div>
      </div>
    </div>
  );
};

export default LoadingProgress;