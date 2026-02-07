import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../../api/client';
import toast from 'react-hot-toast';
import { Plus, Search, Trash2, Edit } from 'lucide-react';

export default function KnowledgeList() {
  const [knowledge, setKnowledge] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    loadKnowledge();
  }, [page, search]);

  const loadKnowledge = async () => {
    try {
      const { data } = await client.get(`/api/knowledge?page=${page}&search=${search}`);
      setKnowledge(data.items);
      setTotal(data.total);
    } catch (error) {
      toast.error('Error cargando conocimientos');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('¿Eliminar este conocimiento?')) return;
    
    try {
      await client.delete(`/api/knowledge/${id}`);
      toast.success('Conocimiento eliminado');
      loadKnowledge();
    } catch (error) {
      toast.error('Error eliminando conocimiento');
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold">Base de Conocimientos</h2>
          <p className="text-gray-600 mt-1">{total} conocimientos totales</p>
        </div>
        <Link to="/knowledge/add" className="btn btn-primary flex items-center gap-2">
          <Plus className="h-4 w-4" />
          Agregar Conocimiento
        </Link>
      </div>

      <div className="card mb-6">
        <div className="flex items-center gap-2">
          <Search className="h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar conocimientos..."
            className="input"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center p-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <div className="space-y-4">
          {knowledge.map((item) => (
            <div key={item.id} className="card hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900">{item.title}</h3>
                  {item.category && (
                    <span className="inline-block px-2 py-1 text-xs font-medium text-primary-700 bg-primary-100 rounded mt-1">
                      {item.category}
                    </span>
                  )}
                  <p className="text-gray-600 mt-2 line-clamp-2">{item.content}</p>
                  <div className="flex items-center gap-4 mt-3 text-sm text-gray-500">
                    <span>Usado {item.times_used} veces</span>
                    <span>Prioridad: {item.priority}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2 ml-4">
                  <Link to={`/knowledge/${item.id}/edit`} className="p-2 hover:bg-gray-100 rounded">
                    <Edit className="h-4 w-4 text-gray-600" />
                  </Link>
                  <button onClick={() => handleDelete(item.id)} className="p-2 hover:bg-red-50 rounded">
                    <Trash2 className="h-4 w-4 text-red-600" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
