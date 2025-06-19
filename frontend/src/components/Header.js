import upaoLogo from '../assets/upao-logo.png'; 

export default function Header({ file }) {
  return (
    <header className="bg-gradient-to-r from-upaoBlue to-blue-500 text-white p-6 shadow-lg rounded-b-2xl flex flex-col sm:flex-row items-center justify-between">
      <div className="flex items-center space-x-4">
        <img src={upaoLogo} alt="UPAO Logo" className="h-14 w-auto drop-shadow" />
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight">Chatbot Contable UPAO</h1>
          <span className="block text-sm font-medium opacity-80 mt-1">Universidad Privada Antenor Orrego</span>
        </div>
      </div>
      {file && (
        <p className="mt-4 sm:mt-0 text-base font-medium bg-white/20 px-4 py-2 rounded-lg shadow text-white">
          📄 {file}
        </p>
      )}
    </header>
  );
}
