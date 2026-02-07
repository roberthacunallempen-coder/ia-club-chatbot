import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout/Layout';
import { ProtectedRoute } from './components/ProtectedRoute';
import Login from './pages/Login/Login';
import Dashboard from './pages/Dashboard';
import KnowledgeList from './pages/Knowledge/KnowledgeList';
import KnowledgeAdd from './pages/Knowledge/KnowledgeAdd';
import KnowledgeEdit from './pages/Knowledge/KnowledgeEdit';
import FAQList from './pages/FAQs/FAQList';
import FAQAdd from './pages/FAQs/FAQAdd';
import FAQEdit from './pages/FAQs/FAQEdit';
import DocumentUpload from './pages/Documents/DocumentUpload';
import DocumentList from './pages/Documents/DocumentList';
import ConversationList from './pages/Conversations/ConversationList';
import ChatInterface from './pages/TestBot/ChatInterface';
import AgentSettings from './pages/Settings/AgentSettings';
import FlowsManager from './pages/Flows/FlowsManager';
import MessageTemplates from './pages/MessageTemplates/MessageTemplates';

function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route index element={<Dashboard />} />
          
          {/* Knowledge Routes */}
          <Route path="knowledge" element={<KnowledgeList />} />
          <Route path="knowledge/add" element={<KnowledgeAdd />} />
          <Route path="knowledge/:id/edit" element={<KnowledgeEdit />} />
          
          {/* FAQ Routes */}
          <Route path="faqs" element={<FAQList />} />
          <Route path="faqs/add" element={<FAQAdd />} />
          <Route path="faqs/:id/edit" element={<FAQEdit />} />
          
          {/* Document Routes */}
          <Route path="documents" element={<DocumentList />} />
          <Route path="documents/upload" element={<DocumentUpload />} />
          
          {/* Conversation Routes */}
          <Route path="conversations" element={<ConversationList />} />
          
          {/* Test Bot */}
          <Route path="test-bot" element={<ChatInterface />} />
          
          {/* Flows */}
          <Route path="flows" element={<FlowsManager />} />
          
          {/* Message Templates */}
          <Route path="templates" element={<MessageTemplates />} />
          
          {/* Settings */}
          <Route path="settings/agents" element={<AgentSettings />} />
          
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
