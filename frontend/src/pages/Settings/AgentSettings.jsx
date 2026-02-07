import { useEffect, useState } from 'react';
import client from '../../api/client';
import toast from 'react-hot-toast';
import { Save, RotateCcw, Bot, Settings as SettingsIcon } from 'lucide-react';

export default function AgentSettings() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(null);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [responseStyle, setResponseStyle] = useState('concisa');
  const [maxTokens, setMaxTokens] = useState(150);
  const [savingGeneral, setSavingGeneral] = useState(false);

  useEffect(() => {
    loadAgents();
    loadGeneralSettings();
  }, []);

  const loadAgents = async () => {
    try {
      const response = await client.get('/api/agents');
      setAgents(response.data);
      if (response.data.length > 0 && !selectedAgent) {
        setSelectedAgent(response.data[0]);
      }
    } catch (error) {
      toast.error('Error al cargar agentes');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const loadGeneralSettings = async () => {
    try {
      // Cargar response_style
      const styleResponse = await client.get('/api/settings/response_style');
      if (styleResponse.data) {
        setResponseStyle(styleResponse.data.value || 'concisa');
      }
      
      // Cargar max_response_tokens
      const tokensResponse = await client.get('/api/settings/max_response_tokens');
      if (tokensResponse.data) {
        setMaxTokens(parseInt(tokensResponse.data.value) || 150);
      }
    } catch (error) {
      console.log('Using default general settings');
    }
  };

  const saveGeneralSettings = async () => {
    setSavingGeneral(true);
    try {
      // Guardar response_style
      await client.post('/api/settings', {
        key: 'response_style',
        value: responseStyle,
        category: 'bot_behavior',
        description: 'Estilo de longitud de respuestas del bot'
      });

      // Guardar max_response_tokens
      await client.post('/api/settings', {
        key: 'max_response_tokens',
        value: maxTokens.toString(),
        category: 'bot_behavior',
        description: 'Número máximo de tokens por respuesta'
      });

      toast.success('Configuración guardada');
    } catch (error) {
      toast.error('Error al guardar configuración');
      console.error(error);
    } finally {
      setSavingGeneral(false);
    }
  };

  const saveAgent = async (agentType) => {
    setSaving(agentType);
    try {
      await client.put(`/api/agents/${agentType}`, selectedAgent);
      toast.success('Agente actualizado');
      loadAgents();
    } catch (error) {
      toast.error('Error al guardar');
      console.error(error);
    } finally {
      setSaving(null);
    }
  };

  const resetToDefaults = async () => {
    if (!confirm('¿Resetear todos los agentes a configuración por defecto?')) return;
    
    try {
      await client.post('/api/agents/reset-defaults');
      toast.success('Agentes reseteados');
      loadAgents();
    } catch (error) {
      toast.error('Error al resetear');
    }
  };

  const handleAgentSelect = (agent) => {
    setSelectedAgent({...agent});
  };

  const updateField = (field, value) => {
    setSelectedAgent({
      ...selectedAgent,
      [field]: value
    });
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Cargando...</div>;
  }

  const agentIcons = {
    sales: '💰',
    design: '🎨',
    order_tracking: '📦',
    support: '🆘',
    general: '💬'
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Configuración de Agentes</h1>
          <p className="text-gray-600 mt-1">Personaliza el comportamiento de cada agente especializado</p>
        </div>
        <button
          onClick={resetToDefaults}
          className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
        >
          <RotateCcw size={20} />
          Resetear a Defaults
        </button>
      </div>

      {/* Configuración General de Respuestas */}
      <div className="bg-white rounded-lg shadow">
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-4 rounded-t-lg">
          <div className="flex items-center gap-3">
            <SettingsIcon size={24} />
            <div>
              <h2 className="text-xl font-semibold">Configuración General de Respuestas</h2>
              <p className="text-sm text-purple-100 mt-1">Controla la longitud y estilo de todas las respuestas del bot</p>
            </div>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {/* Response Style */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Estilo de Respuesta
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button
                onClick={() => {
                  setResponseStyle('concisa');
                  setMaxTokens(150);
                }}
                className={`p-4 border-2 rounded-lg text-left transition-all ${
                  responseStyle === 'concisa'
                    ? 'border-green-500 bg-green-50 shadow-md'
                    : 'border-gray-200 hover:border-green-300'
                }`}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-2xl">⚡</span>
                  <span className="font-semibold text-gray-900">Concisa</span>
                  {responseStyle === 'concisa' && (
                    <span className="ml-auto px-2 py-0.5 bg-green-500 text-white text-xs rounded-full">
                      Recomendado
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-600">2-3 oraciones máximo</p>
                <p className="text-xs text-gray-500 mt-1">~150 tokens • Ahorra costos</p>
              </button>

              <button
                onClick={() => {
                  setResponseStyle('normal');
                  setMaxTokens(250);
                }}
                className={`p-4 border-2 rounded-lg text-left transition-all ${
                  responseStyle === 'normal'
                    ? 'border-blue-500 bg-blue-50 shadow-md'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-2xl">💬</span>
                  <span className="font-semibold text-gray-900">Normal</span>
                </div>
                <p className="text-sm text-gray-600">Longitud media</p>
                <p className="text-xs text-gray-500 mt-1">~250 tokens • Balance</p>
              </button>

              <button
                onClick={() => {
                  setResponseStyle('detallada');
                  setMaxTokens(400);
                }}
                className={`p-4 border-2 rounded-lg text-left transition-all ${
                  responseStyle === 'detallada'
                    ? 'border-purple-500 bg-purple-50 shadow-md'
                    : 'border-gray-200 hover:border-purple-300'
                }`}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-2xl">📝</span>
                  <span className="font-semibold text-gray-900">Detallada</span>
                </div>
                <p className="text-sm text-gray-600">Respuestas completas</p>
                <p className="text-xs text-gray-500 mt-1">~400 tokens • Más contexto</p>
              </button>
            </div>
          </div>

          {/* Max Tokens Slider */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Máximo de Tokens (Personalizado)
              <span className="text-gray-500 font-normal ml-2">{maxTokens} tokens</span>
            </label>
            <input
              type="range"
              min="100"
              max="500"
              step="25"
              value={maxTokens}
              onChange={(e) => {
                setMaxTokens(parseInt(e.target.value));
                setResponseStyle('custom');
              }}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>100 (muy corto)</span>
              <span>250 (medio)</span>
              <span>500 (largo)</span>
            </div>
          </div>

          {/* Info Alert */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex gap-3">
              <span className="text-2xl">💡</span>
              <div className="flex-1">
                <h4 className="font-medium text-blue-900 mb-1">¿Qué afecta esta configuración?</h4>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>✓ Solo afecta respuestas generadas por IA (cuando no hay plantilla)</li>
                  <li>✓ Las <strong>plantillas de mensajes</strong> NO se afectan</li>
                  <li>✓ Respuestas concisas ahorran costos de OpenAI significativamente</li>
                  <li>✓ Los cambios se aplican inmediatamente a nuevas conversaciones</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end">
            <button
              onClick={saveGeneralSettings}
              disabled={savingGeneral}
              className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 shadow-md"
            >
              <Save size={20} />
              {savingGeneral ? 'Guardando...' : 'Guardar Configuración General'}
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Agent List Sidebar */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="bg-blue-600 text-white px-4 py-3 flex items-center gap-2">
              <Bot size={20} />
              <h2 className="font-semibold">Agentes</h2>
            </div>
            <div className="divide-y">
              {agents.map((agent) => (
                <button
                  key={agent.id}
                  onClick={() => handleAgentSelect(agent)}
                  className={`w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors ${
                    selectedAgent?.agent_type === agent.agent_type ? 'bg-blue-50 border-l-4 border-blue-600' : ''
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{agentIcons[agent.agent_type]}</span>
                    <div className="flex-1">
                      <div className="font-medium text-gray-900">{agent.agent_name}</div>
                      <div className="text-xs text-gray-500 mt-0.5">{agent.role_description}</div>
                    </div>
                    {agent.is_active && (
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Agent Configuration Panel */}
        {selectedAgent && (
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow">
              <div className="bg-gray-50 px-6 py-4 border-b flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">{agentIcons[selectedAgent.agent_type]}</span>
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">{selectedAgent.agent_name}</h2>
                    <p className="text-sm text-gray-600">{selectedAgent.role_description}</p>
                  </div>
                </div>
                <button
                  onClick={() => saveAgent(selectedAgent.agent_type)}
                  disabled={saving === selectedAgent.agent_type}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  <Save size={18} />
                  {saving === selectedAgent.agent_type ? 'Guardando...' : 'Guardar Cambios'}
                </button>
              </div>

              <div className="p-6 space-y-6">
                {/* Agent Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nombre del Agente
                  </label>
                  <input
                    type="text"
                    value={selectedAgent.agent_name}
                    onChange={(e) => updateField('agent_name', e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                {/* Role Description */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Descripción del Rol
                  </label>
                  <input
                    type="text"
                    value={selectedAgent.role_description}
                    onChange={(e) => updateField('role_description', e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                {/* Instructions */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Instrucciones del Agente
                    <span className="text-gray-500 font-normal ml-2">(Define cómo debe comportarse)</span>
                  </label>
                  <textarea
                    value={selectedAgent.instructions}
                    onChange={(e) => updateField('instructions', e.target.value)}
                    rows={12}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                  />
                </div>

                {/* Temperature & Max Tokens */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Temperatura (Creatividad)
                      <span className="text-gray-500 font-normal ml-2">{selectedAgent.temperature}%</span>
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={selectedAgent.temperature}
                      onChange={(e) => updateField('temperature', parseInt(e.target.value))}
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>Preciso (0%)</span>
                      <span>Creativo (100%)</span>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Máximo de Tokens
                      <span className="text-gray-500 font-normal ml-2">{selectedAgent.max_tokens}</span>
                    </label>
                    <input
                      type="range"
                      min="100"
                      max="2000"
                      step="50"
                      value={selectedAgent.max_tokens}
                      onChange={(e) => updateField('max_tokens', parseInt(e.target.value))}
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>Corto (100)</span>
                      <span>Largo (2000)</span>
                    </div>
                  </div>
                </div>

                {/* Active Status */}
                <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                  <input
                    type="checkbox"
                    id="is_active"
                    checked={selectedAgent.is_active}
                    onChange={(e) => updateField('is_active', e.target.checked)}
                    className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                  />
                  <label htmlFor="is_active" className="text-sm font-medium text-gray-700 cursor-pointer">
                    Agente Activo
                    <span className="text-gray-500 font-normal ml-2">
                      (Si está desactivado, no se usará en las conversaciones)
                    </span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
