import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../api/client';
import { MessageSquare, BookOpen, HelpCircle, TrendingUp, Users, Clock, FileText, TestTube } from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [convStats, knowledge, faqs] = await Promise.all([
        client.get('/api/conversations/stats'),
        client.get('/api/knowledge?page_size=1'),
        client.get('/api/faqs?page_size=1'),
      ]);

      setStats({
        conversations: convStats.data,
        totalKnowledge: knowledge.data.total,
        totalFaqs: faqs.data.total,
      });
    } catch (error) {
      console.error('Error loading stats:', error);
      // Set default stats on error
      setStats({
        conversations: { total: 0, today: 0, avg_response_time: 0 },
        totalKnowledge: 0,
        totalFaqs: 0,
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900">Panel de Control</h2>
        <p className="text-gray-600 mt-1">Resumen general del chatbot</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 mb-8">
        <StatCard
          title="Conversaciones"
          value={stats?.conversations?.total_conversations || 0}
          icon={MessageSquare}
          color="blue"
        />
        <StatCard
          title="Base de Conocimientos"
          value={stats?.totalKnowledge || 0}
          icon={BookOpen}
          color="green"
        />
        <StatCard
          title="FAQs"
          value={stats?.totalFaqs || 0}
          icon={HelpCircle}
          color="purple"
        />
        <StatCard
          title="Rating Promedio"
          value={stats?.conversations?.avg_rating?.toFixed(1) || '0.0'}
          icon={TrendingUp}
          color="yellow"
          suffix="/5"
        />
        <StatCard
          title="Tasa de Ayuda"
          value={stats?.conversations?.helpful_percentage?.toFixed(0) || 0}
          icon={Users}
          color="indigo"
          suffix="%"
        />
        <StatCard
          title="Tiempo de Respuesta"
          value={stats?.conversations?.avg_response_time?.toFixed(1) || 0}
          icon={Clock}
          color="pink"
          suffix="s"
        />
      </div>

      {/* Quick Actions */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-4">Acciones Rápidas</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <QuickAction
            title="Agregar Conocimiento"
            href="/knowledge/add"
            icon={BookOpen}
          />
          <QuickAction
            title="Agregar FAQ"
            href="/faqs/add"
            icon={HelpCircle}
          />
          <QuickAction
            title="Subir Documento"
            href="/documents/upload"
            icon={FileText}
          />
          <QuickAction
            title="Probar Bot"
            href="/test-bot"
            icon={TestTube}
          />
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon, color, suffix = '' }) {
  const colors = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    purple: 'bg-purple-500',
    yellow: 'bg-yellow-500',
    indigo: 'bg-indigo-500',
    pink: 'bg-pink-500',
  };

  return (
    <div className="card">
      <div className="flex items-center">
        <div className={`p-3 rounded-full ${colors[color]} bg-opacity-10`}>
          <Icon className={`h-6 w-6 text-${color}-600`} />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">
            {value}{suffix}
          </p>
        </div>
      </div>
    </div>
  );
}

function QuickAction({ title, href, icon: Icon }) {
  return (
    <Link
      to={href}
      className="card hover:shadow-md transition-shadow cursor-pointer"
    >
      <div className="flex items-center space-x-3">
        <Icon className="h-5 w-5 text-primary-600" />
        <span className="font-medium text-gray-900">{title}</span>
      </div>
    </Link>
  );
}
