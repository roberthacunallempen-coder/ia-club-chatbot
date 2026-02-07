import { useState, useEffect } from 'react';
import { Plus, Send, Edit, Trash2, Upload, FileText, Image, FileIcon, Music, Video } from 'lucide-react';
import client from '../../api/client';

const MessageTypeIcon = ({ type }) => {
  const icons = {
    text: FileText,
    image: Image,
    document: FileIcon,
    audio: Music,
    video: Video
  };
  const Icon = icons[type] || FileText;
  return <Icon className="w-5 h-5" />;
};

export default function MessageTemplates() {
  const [templates, setTemplates] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('');
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: '',
    messages: [{ order: 0, type: 'text', content: '', file_url: '', delay_seconds: 0 }],
    trigger_keywords: [],
    is_active: true
  });
  
  const [keywordInput, setKeywordInput] = useState('');
  const [uploadingFiles, setUploadingFiles] = useState({});

  useEffect(() => {
    loadTemplates();
    loadCategories();
  }, [selectedCategory]);

  const loadTemplates = async () => {
    try {
      const params = new URLSearchParams();
      if (selectedCategory) params.append('category', selectedCategory);
      
      const { data } = await client.get(`/api/templates?${params}`);
      setTemplates(data.templates || []);
    } catch (error) {
      console.error('Error loading templates:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const { data } = await client.get('/api/templates/categories/list');
      setCategories(data);
    } catch (error) {
      console.error('Error loading categories:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (editingTemplate) {
        await client.put(`/api/templates/${editingTemplate.id}`, formData);
      } else {
        await client.post('/api/templates', formData);
      }
      
      await loadTemplates();
      resetForm();
      alert(editingTemplate ? 'Plantilla actualizada!' : 'Plantilla creada!');
    } catch (error) {
      console.error('Error saving template:', error);
      alert('Error al guardar la plantilla');
    }
  };

  const deleteTemplate = async (id) => {
    if (!confirm('¿Estás seguro de eliminar esta plantilla?')) return;
    
    try {
      await client.delete(`/api/templates/${id}`);
      await loadTemplates();
      alert('Plantilla eliminada!');
    } catch (error) {
      console.error('Error deleting template:', error);
      alert('Error al eliminar la plantilla');
    }
  };

  const editTemplate = (template) => {
    setEditingTemplate(template);
    setFormData({
      name: template.name,
      description: template.description || '',
      category: template.category || '',
      messages: template.messages,
      trigger_keywords: template.trigger_keywords || [],
      is_active: template.is_active
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      category: '',
      messages: [{ order: 0, type: 'text', content: '', file_url: '', delay_seconds: 0 }],
      trigger_keywords: [],
      is_active: true
    });
    setEditingTemplate(null);
    setShowForm(false);
  };

  const addMessage = () => {
    const newOrder = formData.messages.length;
    setFormData({
      ...formData,
      messages: [...formData.messages, { 
        order: newOrder, 
        type: 'text', 
        content: '', 
        file_url: '', 
        delay_seconds: 0 
      }]
    });
  };

  const updateMessage = (index, field, value) => {
    const updatedMessages = [...formData.messages];
    updatedMessages[index] = { ...updatedMessages[index], [field]: value };
    setFormData({ ...formData, messages: updatedMessages });
  };

  const removeMessage = (index) => {
    const updatedMessages = formData.messages.filter((_, i) => i !== index);
    // Reorder
    updatedMessages.forEach((msg, i) => msg.order = i);
    setFormData({ ...formData, messages: updatedMessages });
  };

  const moveMessage = (index, direction) => {
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= formData.messages.length) return;
    
    const updatedMessages = [...formData.messages];
    [updatedMessages[index], updatedMessages[newIndex]] = [updatedMessages[newIndex], updatedMessages[index]];
    
    // Update order
    updatedMessages.forEach((msg, i) => msg.order = i);
    setFormData({ ...formData, messages: updatedMessages });
  };

  const uploadFile = async (file, messageIndex) => {
    const formDataUpload = new FormData();
    formDataUpload.append('file', file);
    formDataUpload.append('category', formData.category || 'general');
    
    setUploadingFiles({ ...uploadingFiles, [messageIndex]: true });
    
    try {
      const { data } = await client.post('/api/templates/upload-file', formDataUpload, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      if (data.success) {
        updateMessage(messageIndex, 'file_url', data.file_path);
        updateMessage(messageIndex, 'content', file.name);
        alert('Archivo subido correctamente!');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error al subir el archivo');
    } finally {
      setUploadingFiles({ ...uploadingFiles, [messageIndex]: false });
    }
  };

  const addKeyword = () => {
    if (keywordInput.trim()) {
      setFormData({
        ...formData,
        trigger_keywords: [...formData.trigger_keywords, keywordInput.trim()]
      });
      setKeywordInput('');
    }
  };

  const removeKeyword = (keyword) => {
    setFormData({
      ...formData,
      trigger_keywords: formData.trigger_keywords.filter(k => k !== keyword)
    });
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Cargando...</div>;
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Plantillas de Mensajes</h1>
          <p className="text-gray-600 mt-2">
            Configura secuencias de mensajes predeterminadas con texto, imágenes y archivos
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Nueva Plantilla
        </button>
      </div>

      {/* Filter by category */}
      <div className="mb-6">
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg"
        >
          <option value="">Todas las categorías</option>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      {/* Create/Edit Form */}
      {showForm && (
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">
            {editingTemplate ? 'Editar Plantilla' : 'Nueva Plantilla'}
          </h2>
          
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Categoría
                </label>
                <input
                  type="text"
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  placeholder="ej: bienvenida, productos, soporte"
                />
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Descripción
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                rows="2"
              />
            </div>

            {/* Keywords */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Palabras clave (opcional)
              </label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={keywordInput}
                  onChange={(e) => setKeywordInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addKeyword())}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg"
                  placeholder="Añadir palabra clave..."
                />
                <button
                  type="button"
                  onClick={addKeyword}
                  className="bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded-lg"
                >
                  Añadir
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {formData.trigger_keywords.map(keyword => (
                  <span key={keyword} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm flex items-center gap-2">
                    {keyword}
                    <button
                      type="button"
                      onClick={() => removeKeyword(keyword)}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {/* Messages */}
            <div className="mb-4">
              <div className="flex justify-between items-center mb-3">
                <label className="block text-sm font-medium text-gray-700">
                  Mensajes (en orden) *
                </label>
                <button
                  type="button"
                  onClick={addMessage}
                  className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm flex items-center gap-1"
                >
                  <Plus className="w-4 h-4" />
                  Añadir Mensaje
                </button>
              </div>

              <div className="space-y-4">
                {formData.messages.map((message, index) => (
                  <div key={index} className="border border-gray-300 rounded-lg p-4 bg-gray-50">
                    <div className="flex justify-between items-center mb-3">
                      <span className="font-medium text-gray-700">
                        Mensaje #{index + 1}
                      </span>
                      <div className="flex gap-2">
                        {index > 0 && (
                          <button
                            type="button"
                            onClick={() => moveMessage(index, 'up')}
                            className="text-gray-600 hover:text-gray-800"
                          >
                            ↑
                          </button>
                        )}
                        {index < formData.messages.length - 1 && (
                          <button
                            type="button"
                            onClick={() => moveMessage(index, 'down')}
                            className="text-gray-600 hover:text-gray-800"
                          >
                            ↓
                          </button>
                        )}
                        {formData.messages.length > 1 && (
                          <button
                            type="button"
                            onClick={() => removeMessage(index)}
                            className="text-red-600 hover:text-red-800"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs text-gray-600 mb-1">Tipo</label>
                        <select
                          value={message.type}
                          onChange={(e) => updateMessage(index, 'type', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded text-sm"
                        >
                          <option value="text">Texto</option>
                          <option value="image">Imagen</option>
                          <option value="document">Documento/PDF</option>
                          <option value="audio">Audio</option>
                          <option value="video">Video</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-xs text-gray-600 mb-1">
                          Delay (segundos)
                        </label>
                        <input
                          type="number"
                          value={message.delay_seconds}
                          onChange={(e) => updateMessage(index, 'delay_seconds', parseInt(e.target.value))}
                          min="0"
                          max="60"
                          className="w-full px-3 py-2 border border-gray-300 rounded text-sm"
                        />
                      </div>
                    </div>

                    <div className="mt-3">
                      <label className="block text-xs text-gray-600 mb-1">Contenido</label>
                      {message.type === 'text' ? (
                        <textarea
                          value={message.content}
                          onChange={(e) => updateMessage(index, 'content', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded text-sm"
                          rows="3"
                          placeholder="Escribe el mensaje aquí... Usa {variable} para variables"
                          required
                        />
                      ) : (
                        <div>
                          <input
                            type="text"
                            value={message.file_url}
                            onChange={(e) => updateMessage(index, 'file_url', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded text-sm mb-2"
                            placeholder="Ruta del archivo o URL"
                            required
                          />
                          <div className="flex gap-2">
                            <input
                              type="file"
                              onChange={(e) => e.target.files[0] && uploadFile(e.target.files[0], index)}
                              className="text-sm"
                              accept={
                                message.type === 'image' ? 'image/*' :
                                message.type === 'document' ? '.pdf,.doc,.docx' :
                                message.type === 'audio' ? 'audio/*' :
                                message.type === 'video' ? 'video/*' : '*'
                              }
                            />
                            {uploadingFiles[index] && (
                              <span className="text-sm text-gray-500">Subiendo...</span>
                            )}
                          </div>
                          <input
                            type="text"
                            value={message.content}
                            onChange={(e) => updateMessage(index, 'content', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded text-sm mt-2"
                            placeholder="Texto descriptivo o caption (opcional)"
                          />
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="mb-4">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={formData.is_active}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  className="w-4 h-4"
                />
                <span className="text-sm text-gray-700">Plantilla activa</span>
              </label>
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
              >
                {editingTemplate ? 'Actualizar' : 'Crear'} Plantilla
              </button>
              <button
                type="button"
                onClick={resetForm}
                className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-6 py-2 rounded-lg"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Templates List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {templates.map(template => (
          <div key={template.id} className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="font-bold text-lg text-gray-900">{template.name}</h3>
                {template.category && (
                  <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded mt-1 inline-block">
                    {template.category}
                  </span>
                )}
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => editTemplate(template)}
                  className="text-blue-600 hover:text-blue-800"
                >
                  <Edit className="w-4 h-4" />
                </button>
                <button
                  onClick={() => deleteTemplate(template.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>

            {template.description && (
              <p className="text-sm text-gray-600 mb-3">{template.description}</p>
            )}

            <div className="space-y-2 mb-3">
              <div className="text-xs text-gray-500">
                {template.messages.length} mensaje(s):
              </div>
              {template.messages.slice(0, 3).map((msg, idx) => (
                <div key={idx} className="flex items-center gap-2 text-sm text-gray-700">
                  <MessageTypeIcon type={msg.type} />
                  <span className="truncate">{msg.content || msg.file_url}</span>
                </div>
              ))}
              {template.messages.length > 3 && (
                <div className="text-xs text-gray-500">
                  +{template.messages.length - 3} más...
                </div>
              )}
            </div>

            {template.trigger_keywords && template.trigger_keywords.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-3">
                {template.trigger_keywords.slice(0, 3).map(keyword => (
                  <span key={keyword} className="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded">
                    {keyword}
                  </span>
                ))}
              </div>
            )}

            <div className="flex justify-between items-center">
              <span className={`text-xs px-2 py-1 rounded ${
                template.is_active 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-600'
              }`}>
                {template.is_active ? 'Activa' : 'Inactiva'}
              </span>
            </div>
          </div>
        ))}
      </div>

      {templates.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          <FileText className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <p>No hay plantillas creadas aún</p>
          <p className="text-sm">Crea tu primera plantilla para empezar</p>
        </div>
      )}
    </div>
  );
}
