# 🤖 Chatbot Knowledge System

Sistema completo de chatbot inteligente con IA (ChatGPT) y panel de administración visual.

## 🎯 Características

- ✅ Bot inteligente con ChatGPT + Base de Conocimientos
- ✅ Panel Admin visual (React) para gestión sin código
- ✅ CRUD de Conocimientos y FAQs
- ✅ Subida de documentos (PDF, DOCX, TXT) con extracción automática
- ✅ **Sistema de Plantillas de Mensajes Predeterminadas (NUEVO)**
- ✅ Sistema de Flujos Conversacionales
- ✅ Analytics y estadísticas de conversaciones
- ✅ Integración con Chatwoot + WordPress
- ✅ Docker + EasyPanel ready

## 🏗️ Arquitectura

```
WordPress → Chatwoot → Backend (FastAPI) → PostgreSQL + Redis
                           ↓
                    Frontend (React/Vite)
```

## 🚀 Despliegue Rápido con EasyPanel

### 1. Clonar proyecto
```bash
git clone <tu-repo>
cd chatbot-knowledge-system
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env.local
# Editar .env.local con tus credenciales
```

### 3. Levantar con Docker
```bash
docker-compose up -d
```

### 4. Inicializar base de datos
```bash
docker-compose exec backend alembic upgrade head
```

## 🔧 Configuración en EasyPanel

1. **Crear nuevo proyecto** en EasyPanel
2. **Importar docker-compose.yml**
3. **Configurar dominios:**
   - Frontend: `iaclub.pro`
   - Backend: `api.iaclub.pro`
4. **Configurar variables de entorno** desde el panel
5. **Deploy** 🚀

## 📝 Variables de Entorno Necesarias

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Chatwoot
CHATWOOT_API_KEY=...
CHATWOOT_BASE_URL=https://app.chatwoot.com
CHATWOOT_ACCOUNT_ID=1

# Database
DATABASE_URL=postgresql://...
```

## 📚 API Endpoints

- `GET /api/knowledge` - Listar conocimientos
- `POST /api/knowledge` - Crear conocimiento
- `GET /api/faqs` - Listar FAQs
- `POST /api/documents/upload` - Subir documento
- `GET /api/conversations` - Ver conversaciones
- `POST /api/test/chat` - Probar bot
- `GET /templates` - Listar plantillas de mensajes
- `POST /templates/send` - Enviar plantilla a conversación

## 🔗 Integración WordPress

1. Instalar plugin de Chatwoot en WordPress
2. Configurar webhook en Chatwoot → `https://api.iaclub.pro/webhook/chatwoot`
3. Listo ✅

## 📖 Documentación

- [Guía de instalación completa](./docs/installation.md)
- [Configuración de Chatwoot](./docs/chatwoot-setup.md)
- [Sistema de Plantillas de Mensajes](./GUIA_PLANTILLAS_MENSAJES.md) ⭐ NUEVO
- [Sistema de Flujos Conversacionales](./GUIA_FLUJOS.md)
- [API Reference](./docs/api.md)

## 🛠️ Stack Tecnológico

**Backend:**
- FastAPI
- SQLAlchemy + PostgreSQL
- Redis
- OpenAI API
- PyPDF2, python-docx

**Frontend:**
- React 18
- Vite
- TailwindCSS
- Axios

**DevOps:**
- Docker + Docker Compose
- Nginx
- EasyPanel

## 📄 Licencia

MIT

## 👨‍💻 Autor

Tu nombre - [iaclub.pro](https://iaclub.pro)
