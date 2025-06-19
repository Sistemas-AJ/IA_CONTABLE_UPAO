import { CloudArrowUpIcon } from '@heroicons/react/24/outline';

export default function UploadSection({ enabled, onFile, status, progress }) {
  if (!enabled) return null;

  return (
    <div className="w-full max-w-2xl mb-4">
      <label className="flex flex-col items-center justify-center border-2 border-dashed border-upaoBlue rounded-lg p-6 cursor-pointer hover:bg-blue-50 transition">
        <CloudArrowUpIcon className="h-10 w-10 text-upaoBlue mb-2" />
        <span className="font-semibold text-upaoBlue">Subir documento PDF o TXT</span>
        <input
          type="file"
          accept=".pdf,.txt"
          className="hidden"
          onChange={e => onFile(e.target.files[0])}
        />
      </label>
      {status && (
        <div className="mt-2 text-sm text-gray-700">
          {status} {progress > 0 && progress < 100 && <span>({progress}%)</span>}
        </div>
      )}
      {progress > 0 && progress < 100 && (
        <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
          <div
            className="bg-upaoBlue h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
}