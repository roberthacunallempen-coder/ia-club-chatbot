import { useState } from 'react';
import client from '../../api/client';
import toast from 'react-hot-toast';
import { Upload } from 'lucide-react';

export default function DocumentUpload() {
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState('');
  const [description, setDescription] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('category', category);
    formData.append('description', description);

    setUploading(true);
    try {
      await client.post('/api/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      toast.success('Documento subido. Procesando en segundo plano...');
      setFile(null);
      setCategory('');
      setDescription('');
    } catch (error) {
      toast.error('Error subiendo documento');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Subir Documento</h2>

      <form onSubmit={handleSubmit} className="card max-w-2xl">
        <div className="space-y-4">
          <div>
            <label className="label">Archivo (PDF, DOCX, TXT, CSV)</label>
            <input
              type="file"
              accept=".pdf,.docx,.txt,.csv"
              onChange={(e) => setFile(e.target.files[0])}
              className="input"
              required
            />
          </div>

          <div>
            <label className="label">Categoría</label>
            <input
              type="text"
              className="input"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            />
          </div>

          <div>
            <label className="label">Descripción</label>
            <textarea
              className="input"
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <button
            type="submit"
            disabled={uploading}
            className="btn btn-primary flex items-center gap-2"
          >
            <Upload className="h-4 w-4" />
            {uploading ? 'Subiendo...' : 'Subir Documento'}
          </button>
        </div>
      </form>
    </div>
  );
}
