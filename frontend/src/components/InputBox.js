export default function InputBox({ value, onChange, onSend, loading }) {
  return (
    <div className="flex items-center p-4 bg-gray-100 shadow-inner w-full rounded-lg">
      <textarea
        rows={2}
        className="flex-grow border rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
        placeholder="Escribe tu consulta contable..."
        value={value}
        onChange={e => onChange(e.target.value)}
        onKeyDown={e => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            onSend();
          }
        }}
        />
      <button
        onClick={onSend}
        disabled={loading || !value.trim()}
        className="ml-3 px-8 py-2 bg-upaoGold text-upaoBlue font-bold rounded-lg shadow hover:scale-105 transition-transform duration-200"
      >
        {loading ? 'Analizando…' : 'Enviar'}
      </button>
    </div>
  );
}
