import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../../api/client';
import toast from 'react-hot-toast';
import { FileText, Download, Trash2, Upload } from 'lucide-react';

export default function DocumentList() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await client.get('/api/documents');
      setDocuments(response.data.items);
    } catch (error) {
      toast.error('Error al cargar documentos');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const deleteDocument = async (id) => {
    if (!confirm('¿Eliminar este documento?')) return;
    
    try {
      await client.delete(`/api/documents/${id}`);
      toast.success('Documento eliminado');
      loadDocuments();
    } catch (error) {
      toast.error('Error al eliminar');
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Cargando...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Documentos</h1>
        <Link
          to="/documents/upload"
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Upload size={20} />
          Subir Documento
        </Link>
      </div>

      {documents.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <FileText className="mx-auto mb-4 text-gray-400" size={48} />
          <p className="text-gray-500 mb-4">No hay documentos todavía</p>
          <Link to="/documents/upload" className="text-blue-600 hover:text-blue-700">
            Subir el primero
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {documents.map((doc) => (
            <div key={doc.id} className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <FileText className="text-blue-600" size={32} />
                <button
                  onClick={() => deleteDocument(doc.id)}
                  className="text-red-600 hover:text-red-700 p-1"
                >
                  <Trash2 size={18} />
                </button>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2 truncate">
                {doc.filename}
              </h3>
              <div className="space-y-2 text-sm text-gray-600">
                <p>Tipo: {doc.file_type.toUpperCase()}</p>
                <p>Tamaño: {(doc.file_size / 1024).toFixed(2)} KB</p>
                <p>Subido: {new Date(doc.created_at).toLocaleDateString()}</p>
              </div>
              {doc.processed && (
                <div className="mt-3">
                  <span className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded">
                    Procesado
                  </span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
