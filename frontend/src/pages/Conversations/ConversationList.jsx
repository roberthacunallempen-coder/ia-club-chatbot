import { useEffect, useState } from 'react';
import client from '../../api/client';
import toast from 'react-hot-toast';
import { MessageSquare, ThumbsUp, ThumbsDown, Clock } from 'lucide-react';

export default function ConversationList() {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const response = await client.get('/api/conversations');
      setConversations(response.data.items);
    } catch (error) {
      toast.error('Error al cargar conversaciones');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Cargando...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Conversaciones</h1>
      </div>

      {conversations.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <MessageSquare className="mx-auto mb-4 text-gray-400" size={48} />
          <p className="text-gray-500">No hay conversaciones todavía</p>
          <p className="text-sm text-gray-400 mt-2">
            Las conversaciones aparecerán aquí cuando los usuarios interactúen con el bot
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {conversations.map((conv) => (
            <div key={conv.id} className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    Conversación #{conv.chatwoot_conversation_id}
                  </h3>
                  <p className="text-sm text-gray-500">
                    {new Date(conv.started_at).toLocaleString()}
                  </p>
                </div>
                <div className="flex gap-2">
                  {conv.was_helpful === true && (
                    <ThumbsUp className="text-green-600" size={20} />
                  )}
                  {conv.was_helpful === false && (
                    <ThumbsDown className="text-red-600" size={20} />
                  )}
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                <div>
                  <p className="text-xs text-gray-500">Mensajes</p>
                  <p className="text-lg font-semibold">{conv.total_messages}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Tiempo Promedio</p>
                  <p className="text-lg font-semibold">
                    {conv.avg_response_time ? `${conv.avg_response_time.toFixed(1)}s` : 'N/A'}
                  </p>
                </div>
                {conv.customer_rating && (
                  <div>
                    <p className="text-xs text-gray-500">Rating</p>
                    <p className="text-lg font-semibold">⭐ {conv.customer_rating}/5</p>
                  </div>
                )}
                {conv.needed_human_agent && (
                  <div>
                    <span className="text-xs px-2 py-1 bg-orange-100 text-orange-700 rounded">
                      Escalado a Humano
                    </span>
                  </div>
                )}
              </div>

              {conv.customer_feedback && (
                <div className="mt-3 p-3 bg-gray-50 rounded">
                  <p className="text-sm text-gray-600">{conv.customer_feedback}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
