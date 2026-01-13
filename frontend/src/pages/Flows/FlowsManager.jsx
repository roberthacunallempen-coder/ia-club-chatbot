import { useEffect, useState } from 'react';
import client from '../../api/client';
import toast from 'react-hot-toast';
import { Play, Pause, RotateCcw, TrendingUp } from 'lucide-react';

export default function FlowsManager() {
  const [flows, setFlows] = useState([]);
  const [selectedFlow, setSelectedFlow] = useState(null);
  const [testConversationId, setTestConversationId] = useState(1);

  useEffect(() => {
    loadAvailableFlows();
  }, []);

  const loadAvailableFlows = async () => {
    try {
      const { data } = await client.get('/api/flows/available');
      setFlows(data.flows);
    } catch (error) {
      toast.error('Error cargando flujos');
    }
  };

  const startFlow = async (flowId) => {
    try {
      const { data } = await client.post('/api/flows/start', {
        flow_id: flowId,
        conversation_id: testConversationId
      });
      
      toast.success(`Flujo ${flowId} iniciado`);
      setSelectedFlow(data);
    } catch (error) {
      toast.error('Error iniciando flujo');
    }
  };

  const abandonFlow = async () => {
    try {
      await client.delete(`/api/flows/abandon/${testConversationId}`);
      toast.success('Flujo abandonado');
      setSelectedFlow(null);
    } catch (error) {
      toast.error('Error abandonando flujo');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Flujos Conversacionales</h1>
          <p className="text-gray-600 mt-1">Guía a tus clientes con flujos estructurados</p>
        </div>
        <div className="flex items-center gap-2">
          <TrendingUp className="text-blue-600" size={24} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Lista de Flujos */}
        <div className="lg:col-span-1 space-y-4">
          <h2 className="text-lg font-semibold mb-4">Flujos Disponibles</h2>
          
          {flows.map((flow) => (
            <div key={flow.id} className="card hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-gray-900">{flow.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{flow.description}</p>
                </div>
              </div>
              
              <button
                onClick={() => startFlow(flow.id)}
                className="btn btn-primary w-full flex items-center justify-center gap-2"
              >
                <Play size={16} />
                Iniciar Flujo
              </button>
            </div>
          ))}
        </div>

        {/* Panel de Información */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-lg font-semibold mb-4">¿Qué son los Flujos?</h2>
            
            <div className="space-y-4">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-semibold text-blue-900 mb-2">💡 Concepto</h3>
                <p className="text-sm text-blue-800">
                  Los flujos son conversaciones estructuradas que guían al cliente paso a paso hacia un objetivo específico (onboarding, compra, soporte).
                </p>
              </div>

              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h3 className="font-semibold text-green-900 mb-2">✅ Beneficios</h3>
                <ul className="text-sm text-green-800 space-y-1 list-disc list-inside">
                  <li>Mayor tasa de conversión</li>
                  <li>Experiencia consistente</li>
                  <li>Captura de información estructurada</li>
                  <li>Reducción de abandono</li>
                </ul>
              </div>

              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <h3 className="font-semibold text-purple-900 mb-2">🎯 Flujos Incluidos</h3>
                <div className="text-sm text-purple-800 space-y-2">
                  <div>
                    <strong>Onboarding:</strong> Bienvenida, detección de perfil, selección de plan y captura de contacto
                  </div>
                  <div>
                    <strong>Recuperación:</strong> Reactiva clientes que abandonaron con ofertas especiales
                  </div>
                </div>
              </div>

              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h3 className="font-semibold text-yellow-900 mb-2">⚙️ Personalización</h3>
                <p className="text-sm text-yellow-800">
                  Puedes editar los flujos en <code className="bg-yellow-100 px-2 py-0.5 rounded">backend/app/bot/conversation_flows.py</code>
                </p>
              </div>
            </div>
          </div>

          {/* Preview del Flujo Activo */}
          {selectedFlow && (
            <div className="card mt-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold">Flujo Activo</h2>
                <button
                  onClick={abandonFlow}
                  className="text-red-600 hover:text-red-700 flex items-center gap-2"
                >
                  <Pause size={16} />
                  Abandonar
                </button>
              </div>

              <div className="bg-gray-50 rounded-lg p-4 mb-4">
                <p className="text-sm font-medium text-gray-700 mb-2">Primer Mensaje:</p>
                <div className="bg-white rounded p-3 text-sm">
                  {selectedFlow.message}
                </div>
              </div>

              <div className="text-xs text-gray-500">
                <p>Flow ID: {selectedFlow.flow_id}</p>
                <p>Estado: {selectedFlow.flow_started ? 'Iniciado' : 'No iniciado'}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Sección de Cómo Usar */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">📖 Cómo Usar los Flujos</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="border-l-4 border-blue-500 pl-4">
            <h3 className="font-semibold text-gray-900 mb-2">1. Inicio Automático</h3>
            <p className="text-sm text-gray-600">
              Los flujos pueden iniciarse automáticamente cuando un usuario nuevo llega al chat
            </p>
          </div>

          <div className="border-l-4 border-green-500 pl-4">
            <h3 className="font-semibold text-gray-900 mb-2">2. Guía Paso a Paso</h3>
            <p className="text-sm text-gray-600">
              El bot guía al usuario con preguntas y opciones claras en cada paso
            </p>
          </div>

          <div className="border-l-4 border-purple-500 pl-4">
            <h3 className="font-semibold text-gray-900 mb-2">3. Captura de Datos</h3>
            <p className="text-sm text-gray-600">
              Se captura información importante (nombre, contacto, preferencias) automáticamente
            </p>
          </div>
        </div>

        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <h3 className="font-semibold mb-2">💡 Tip Pro</h3>
          <p className="text-sm text-gray-700">
            Combina flujos con el sistema de perfiles para personalizar cada paso según el tipo de cliente (académico, creativo, desarrollador).
          </p>
        </div>
      </div>
    </div>
  );
}
