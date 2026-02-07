import { useState, useEffect } from 'react';
import client from '../../api/client';
import { Send } from 'lucide-react';
import Markdown from 'react-markdown';

export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Reset error when sending new message
  useEffect(() => {
    if (input) {
      setError(null);
    }
  }, [input]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const { data } = await client.post('/api/test/chat', {
        message: input,
        conversation_history: messages,
      });

      setMessages((prev) => [
        ...prev,
        { 
          role: 'assistant', 
          content: data.response || 'Error: respuesta vacía',
          metadata: {
            agent: data.agent_used || 'Unknown',
            intent: data.intent || 'unknown',
            confidence: data.confidence || 0,
            knowledge_count: data.knowledge_used?.length || 0,
            faq_count: data.faqs_used?.length || 0,
            profile: data.customer_profile || null,
            engagement: data.engagement_level || null
          }
        },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        { 
          role: 'assistant', 
          content: '❌ **Error de conexión**\n\nNo pude conectarme con el servidor. Por favor verifica que el backend esté funcionando.',
          metadata: {
            agent: 'Error Handler',
            intent: 'error',
            confidence: 0,
            knowledge_count: 0,
            faq_count: 0,
            profile: null,
            engagement: null
          }
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Probar Bot</h2>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          <strong>Error:</strong> {error}
        </div>
      )}

      <div className="card max-w-4xl mx-auto">
        <div className="h-96 overflow-y-auto mb-4 space-y-4">
          {messages.map((msg, idx) => {
            try {
              return (
                <div
                  key={idx}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={msg.role === 'user' ? 'max-w-md' : 'max-w-2xl'}>
                    <div
                      className={`px-4 py-2 rounded-lg ${
                        msg.role === 'user'
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-200 text-gray-900'
                      }`}
                    >
                      {msg.role === 'assistant' ? (
                        <div className="prose prose-sm max-w-none">
                          <Markdown
                            components={{
                              a: ({node, ...props}) => (
                                <a 
                                  {...props} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="text-blue-600 hover:text-blue-800 underline font-medium"
                                />
                              ),
                            }}
                          >
                            {msg.content || 'Mensaje vacío'}
                          </Markdown>
                        </div>
                      ) : (
                        msg.content
                      )}
                    </div>
                {msg.metadata && (
                  <div className="text-xs text-gray-500 mt-1 px-2">
                    <span className="font-semibold">🤖 {msg.metadata.agent || 'Unknown'}</span>
                    <span className="mx-2">•</span>
                    <span>Intención: {msg.metadata.intent || 'unknown'}</span>
                    <span className="mx-2">•</span>
                    <span>Confianza: {((msg.metadata.confidence || 0) * 100).toFixed(0)}%</span>
                    {msg.metadata.profile && msg.metadata.profile !== 'general' && (
                      <>
                        <span className="mx-2">•</span>
                        <span className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded">
                          Perfil: {msg.metadata.profile}
                        </span>
                      </>
                    )}
                    {msg.metadata.engagement && (
                      <>
                        <span className="mx-2">•</span>
                        <span className={`px-2 py-0.5 rounded ${
                          msg.metadata.engagement === 'high' ? 'bg-green-100 text-green-800' :
                          msg.metadata.engagement === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-600'
                        }`}>
                          {msg.metadata.engagement === 'high' ? '🔥 Hot Lead' :
                           msg.metadata.engagement === 'medium' ? '⚡ Warm Lead' :
                           '❄️ Cold Lead'}
                        </span>
                      </>
                    )}
                    {msg.metadata.knowledge_count > 0 && (
                      <>
                        <span className="mx-2">•</span>
                        <span>📚 {msg.metadata.knowledge_count} conocimientos</span>
                      </>
                    )}
                    {msg.metadata.faq_count > 0 && (
                      <>
                        <span className="mx-2">•</span>
                        <span>❓ {msg.metadata.faq_count} FAQs</span>
                      </>
                    )}
                  </div>
                )}
              </div>
            </div>
              );
            } catch (err) {
              console.error('Error rendering message:', err, msg);
              return (
                <div key={idx} className="flex justify-start">
                  <div className="bg-red-100 text-red-700 px-4 py-2 rounded-lg text-sm">
                    ⚠️ Error mostrando mensaje
                  </div>
                </div>
              );
            }
          })}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-200 px-4 py-2 rounded-lg">
                Escribiendo...
              </div>
            </div>
          )}
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            className="input flex-1"
            placeholder="Escribe tu mensaje..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button onClick={sendMessage} className="btn btn-primary">
            <Send className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
