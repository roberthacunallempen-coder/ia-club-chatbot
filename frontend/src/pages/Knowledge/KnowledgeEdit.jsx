import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import client from '../../api/client';
import toast from 'react-hot-toast';

export default function KnowledgeEdit() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [keywordInput, setKeywordInput] = useState('');

  useEffect(() => {
    loadKnowledge();
  }, [id]);

  const loadKnowledge = async () => {
    try {
      const { data } = await client.get(`/api/knowledge/${id}`);
      setForm(data);
    } catch (error) {
      toast.error('Error cargando conocimiento');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      await client.put(`/api/knowledge/${id}`, form);
      toast.success('Conocimiento actualizado');
      navigate('/knowledge');
    } catch (error) {
      toast.error('Error actualizando conocimiento');
    }
  };

  const addKeyword = () => {
    if (keywordInput.trim()) {
      setForm({ ...form, keywords: [...(form.keywords || []), keywordInput.trim()] });
      setKeywordInput('');
    }
  };

  const removeKeyword = (index) => {
    setForm({ ...form, keywords: form.keywords.filter((_, i) => i !== index) });
  };

  if (loading) return <div>Cargando...</div>;
  if (!form) return <div>No encontrado</div>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Editar Conocimiento</h2>
      
      <form onSubmit={handleSubmit} className="card max-w-3xl">
        <div className="space-y-4">
          <div>
            <label className="label">Título *</label>
            <input
              type="text"
              className="input"
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              required
            />
          </div>

          <div>
            <label className="label">Categoría</label>
            <select
              className="input"
              value={form.category || ''}
              onChange={(e) => setForm({ ...form, category: e.target.value })}
            >
              <option value="">Seleccionar categoría</option>
              <option value="empresa">Empresa</option>
              <option value="productos">Productos</option>
              <option value="precios">Precios</option>
              <option value="promociones">Promociones</option>
              <option value="ventas">Ventas</option>
              <option value="proceso">Proceso</option>
            </select>
          </div>

          <div>
            <label className="label">Contenido *</label>
            <textarea
              className="input"
              rows={6}
              value={form.content}
              onChange={(e) => setForm({ ...form, content: e.target.value })}
              required
            />
          </div>

          <div>
            <label className="label">Palabras Clave</label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                className="input"
                value={keywordInput}
                onChange={(e) => setKeywordInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addKeyword())}
              />
              <button type="button" onClick={addKeyword} className="btn btn-secondary">
                Agregar
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {(form.keywords || []).map((keyword, index) => (
                <span key={index} className="px-2 py-1 bg-gray-200 rounded text-sm">
                  {keyword}
                  <button
                    type="button"
                    onClick={() => removeKeyword(index)}
                    className="ml-2 text-red-600"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>

          <div>
            <label className="label">Prioridad (0-100)</label>
            <input
              type="number"
              className="input"
              min="0"
              max="100"
              value={form.priority || 0}
              onChange={(e) => setForm({ ...form, priority: parseInt(e.target.value) })}
            />
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="active"
              checked={form.is_active}
              onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
            />
            <label htmlFor="active" className="text-sm font-medium">
              Activo
            </label>
          </div>

          <div className="flex gap-2 pt-4">
            <button type="submit" className="btn btn-primary">Actualizar</button>
            <button type="button" onClick={() => navigate('/knowledge')} className="btn btn-secondary">
              Cancelar
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
