import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { MathJax } from 'better-react-mathjax'; // <-- Agrega esto

export default function Message({ message }) {
  const isUser = message.role === 'user';
  const safeContent = typeof message.content === 'string' ? message.content : JSON.stringify(message.content);

  return (
    <div className={`flex w-full my-2 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {/* Icono solo visible en sm+ */}
      {!isUser && (
        <div className="flex-shrink-0 mr-2 hidden sm:flex">
          <div className="h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold shadow">
            📊
          </div>
        </div>
      )}
      <div
        className={`
          ${isUser ? 'w-fit' : 'w-full'}
          max-w-[700px] sm:max-w-[600px] md:max-w-[700px] lg:max-w-[800px]
          px-5 py-4 rounded-2xl shadow border
          ${isUser
            ? 'bg-blue-50 text-blue-900 rounded-br-md ml-auto'
            : 'bg-white text-gray-900 rounded-bl-md mr-auto'}
          break-words
          transition-all
        `}
        style={{
          wordBreak: 'break-word',
          overflowWrap: 'anywhere'
        }}
      >
        <div className="prose prose-sm max-w-none">
          <MathJax> {/* <-- ENVUELVE AQUÍ */}
            <ReactMarkdown 
              remarkPlugins={[remarkGfm]}
              components={{
                table: ({node, ...props}) => (
                  <div className="overflow-x-auto w-full">
                    <table className="w-full border-collapse border border-gray-300 text-xs" {...props} />
                  </div>
                ),
                th: ({node, ...props}) => (
                  <th className="border border-gray-300 bg-blue-600 text-white px-2 py-1 text-center font-semibold" {...props} />
                ),
                td: ({node, ...props}) => (
                  <td className="border border-gray-300 px-2 py-1 text-center" {...props} />
                ),
              }}
            >
              {safeContent}
            </ReactMarkdown>
          </MathJax>
        </div>
      </div>
      {/* Icono solo visible en sm+ */}
      {isUser && (
        <div className="flex-shrink-0 ml-2 hidden sm:flex">
          <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center text-blue-600 font-bold shadow">
            TÚ
          </div>
        </div>
      )}
    </div>
  );
}