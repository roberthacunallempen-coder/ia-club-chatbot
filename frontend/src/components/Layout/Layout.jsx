import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import {  Home, BookOpen, HelpCircle, FileText, MessageSquare, TestTube, Menu, Settings, GitBranch, Mail, LogOut } from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Base de Conocimientos', href: '/knowledge', icon: BookOpen },
  { name: 'FAQs', href: '/faqs', icon: HelpCircle },
  { name: 'Documentos', href: '/documents', icon: FileText },
  { name: 'Conversaciones', href: '/conversations', icon: MessageSquare },
  { name: 'Flujos', href: '/flows', icon: GitBranch },
  { name: 'Plantillas de Mensajes', href: '/templates', icon: Mail },
  { name: 'Probar Bot', href: '/test-bot', icon: TestTube },
  { name: 'Configurar Agentes', href: '/settings/agents', icon: Settings },
];

export default function Layout() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
          <div className="fixed inset-y-0 left-0 flex w-64 flex-col bg-white">
            <Sidebar />
          </div>
        </div>
      )}

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <Sidebar />
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <div className="sticky top-0 z-10 bg-white border-b border-gray-200 px-4 py-4 lg:px-8">
          <div className="flex items-center justify-between">
            <button
              type="button"
              className="lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="h-6 w-6" />
            </button>
            <h1 className="text-xl font-semibold text-gray-900">
              {navigation.find(item => item.href === location.pathname)?.name || 'Admin Panel'}
            </h1>
          </div>
        </div>

        {/* Page content */}
        <main className="p-4 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="flex grow flex-col gap-y-5 overflow-y-auto border-r border-gray-200 bg-white px-6">
      <div className="flex h-16 shrink-0 items-center border-b">
        <h1 className="text-xl font-bold text-primary-600">IA Club - Tío IA 🤖</h1>
      </div>
      
      {/* User info */}
      {user && (
        <div className="px-3 py-2 bg-primary-50 rounded-lg">
          <p className="text-xs text-gray-500">Usuario</p>
          <p className="text-sm font-medium text-gray-900">{user.username}</p>
        </div>
      )}
      
      <nav className="flex flex-1 flex-col">
        <ul role="list" className="flex flex-1 flex-col gap-y-7">
          <li>
            <ul role="list" className="-mx-2 space-y-1">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href || 
                               (item.href !== '/' && location.pathname.startsWith(item.href));
                return (
                  <li key={item.name}>
                    <Link
                      to={item.href}
                      className={`group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold ${
                        isActive
                          ? 'bg-primary-50 text-primary-600'
                          : 'text-gray-700 hover:text-primary-600 hover:bg-gray-50'
                      }`}
                    >
                      <item.icon className="h-5 w-5 shrink-0" />
                      {item.name}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </li>
          <li className="mt-auto border-t pt-4">
            <button
              onClick={handleLogout}
              className="group flex w-full gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold text-red-600 hover:bg-red-50"
            >
              <LogOut className="h-5 w-5 shrink-0" />
              Cerrar Sesión
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
}

