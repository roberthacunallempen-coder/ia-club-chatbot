import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../../api/client';
import toast from 'react-hot-toast';
import { Plus, Search, Trash2, Edit } from 'lucide-react';

export default function FAQList() {
  const [faqs, setFaqs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadFaqs();
  }, []);

  const loadFaqs = async () => {
    try {
      const response = await client.get('/api/faqs');
      setFaqs(response.data.items);
    } catch (error) {
      toast.error('Error al cargar FAQs');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const deleteFaq = async (id) => {
    if (!confirm('¿Eliminar este FAQ?')) return;
    
    try {
      await client.delete(`/api/faqs/${id}`);
      toast.success('FAQ eliminado');
      loadFaqs();
    } catch (error) {
      toast.error('Error al eliminar');
    }
  };

  const filteredFaqs = faqs.filter(faq =>
    faq.question.toLowerCase().includes(search.toLowerCase()) ||
    faq.answer.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return <div className="flex justify-center items-center h-64">Cargando...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">FAQs</h1>
        <Link
          to="/faqs/add"
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus size={20} />
          Agregar FAQ
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Buscar FAQs..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {filteredFaqs.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <p className="text-gray-500 mb-4">No hay FAQs todavía</p>
          <Link to="/faqs/add" className="text-blue-600 hover:text-blue-700">
            Agregar el primero
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredFaqs.map((faq) => (
            <div key={faq.id} className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-lg font-semibold text-gray-900">{faq.question}</h3>
                <div className="flex gap-2">
                  <Link
                    to={`/faqs/${faq.id}/edit`}
                    className="text-blue-600 hover:text-blue-700 p-2"
                  >
                    <Edit size={18} />
                  </Link>
                  <button
                    onClick={() => deleteFaq(faq.id)}
                    className="text-red-600 hover:text-red-700 p-2"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
              <p className="text-gray-600 mb-3">{faq.answer}</p>
              <div className="flex gap-2">
                <span className="text-xs px-2 py-1 bg-gray-100 rounded">
                  Categoría: {faq.category}
                </span>
                {faq.is_active && (
                  <span className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded">
                    Activo
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
