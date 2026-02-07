# 🚀 GUÍA DE DESPLIEGUE EN EASYPANEL

## 📋 Pre-requisitos

1. ✅ Cuenta de EasyPanel con VPS configurado
2. ✅ Dominio: **iaclub.pro** apuntando al VPS
3. ✅ API Keys:
   - OpenAI API Key
   - Chatwoot API Key + Base URL + Account ID

---

## 🔧 PASO 1: Preparar el Proyecto

### 1.1 Configurar variables de entorno

Copia `.env.example` a `.env.local` y edita:

```bash
cp .env.example .env.local
nano .env.local
```

**Variables críticas:**
```env
# PostgreSQL
POSTGRES_PASSWORD=tu_password_seguro_aqui

# OpenAI
OPENAI_API_KEY=sk-tu-key-aqui
OPENAI_MODEL=gpt-4-turbo-preview

# Chatwoot
CHATWOOT_API_KEY=tu-chatwoot-key
CHATWOOT_BASE_URL=https://app.chatwoot.com
CHATWOOT_ACCOUNT_ID=1

# Dominios
FRONTEND_URL=https://iaclub.pro
BACKEND_URL=https://api.iaclub.pro
```

---

## 🐳 PASO 2: Desplegar en EasyPanel

### 2.1 Crear nuevo proyecto

1. Entra a tu panel de EasyPanel
2. Clic en **"New Project"**
3. Nombre: `chatbot-iaclub`

### 2.2 Importar docker-compose.yml

1. En el proyecto, ve a **"Services"**
2. Clic en **"Add Service"** → **"Docker Compose"**
3. Pega el contenido de `docker-compose.yml`
4. Clic en **"Create"**

### 2.3 Configurar variables de entorno

En EasyPanel, ve a cada servicio y agrega las variables:

**Backend:**
- `DATABASE_URL=postgresql://chatbot_user:PASSWORD@postgres:5432/chatbot_db`
- `REDIS_URL=redis://redis:6379/0`
- `OPENAI_API_KEY=sk-...`
- `CHATWOOT_API_KEY=...`
- `CHATWOOT_BASE_URL=https://app.chatwoot.com`
- `CHATWOOT_ACCOUNT_ID=1`

**Frontend:**
- `VITE_API_URL=https://api.iaclub.pro`

### 2.4 Configurar dominios

1. **Backend (api.iaclub.pro):**
   - Ve al servicio `backend`
   - En "Domains", agrega: `api.iaclub.pro`
   - Puerto: `8000`
   - Activa SSL (Let's Encrypt automático)

2. **Frontend (iaclub.pro):**
   - Ve al servicio `frontend`
   - En "Domains", agrega: `iaclub.pro` y `www.iaclub.pro`
   - Puerto: `80`
   - Activa SSL

---

## 🗄️ PASO 3: Inicializar Base de Datos

### 3.1 Espera a que los contenedores estén arriba

Verifica en EasyPanel que todos los servicios estén "Running".

### 3.2 Ejecuta las migraciones

En EasyPanel, ve al servicio `backend` → "Terminal" y ejecuta:

```bash
alembic upgrade head
```

O desde tu computadora (si tienes acceso SSH):

```bash
docker-compose exec backend alembic upgrade head
```

---

## ⚙️ PASO 4: Configurar Chatwoot Webhook

### 4.1 En Chatwoot

1. Ve a **Settings** → **Webhooks**
2. Clic en **"Add Webhook"**
3. **URL:** `https://api.iaclub.pro/webhook/chatwoot`
4. **Events:** Selecciona `message_created`
5. Guarda

### 4.2 Probar webhook

Envía un mensaje de prueba desde Chatwoot y verifica los logs en EasyPanel (servicio backend).

---

## ✅ PASO 5: Verificar Funcionamiento

### 5.1 Verificar servicios

1. **Backend Health:** `https://api.iaclub.pro/health`
2. **Frontend:** `https://iaclub.pro`
3. **API Docs:** `https://api.iaclub.pro/docs` (solo si DEBUG=true)

### 5.2 Crear primer conocimiento

1. Ve a `https://iaclub.pro`
2. Navega a **Base de Conocimientos** → **Agregar**
3. Crea un conocimiento de prueba
4. Guarda

### 5.3 Probar el bot

1. Ve a **Probar Bot** en el panel
2. Escribe una pregunta relacionada con el conocimiento creado
3. El bot debería responder usando ese conocimiento

---

## 🔄 PASO 6: Agregar Conocimientos Iniciales

### Opción A: Manual

Usar el panel admin en `iaclub.pro` para agregar:
- Conocimientos
- FAQs
- Documentos

### Opción B: Subir documentos

1. Ve a **Documentos** → **Subir**
2. Sube un PDF/DOCX con información de tu negocio
3. El sistema extraerá automáticamente y creará conocimientos

---

## 📊 Monitoreo

### Ver logs en EasyPanel

1. Ve a cada servicio
2. Pestaña **"Logs"**
3. Filtra por errores si hay problemas

### Métricas

En el Dashboard del panel admin verás:
- Total de conversaciones
- Conocimientos usados
- Rating promedio
- Tiempo de respuesta

---

## 🐛 Troubleshooting

### Backend no arranca

```bash
# Ver logs
docker-compose logs backend

# Verificar base de datos
docker-compose exec postgres psql -U chatbot_user -d chatbot_db -c "SELECT 1;"
```

### Frontend muestra error de conexión

1. Verifica que `VITE_API_URL` apunte a `https://api.iaclub.pro`
2. Verifica CORS en backend (`.env.local`)

### Bot no responde en Chatwoot

1. Verifica que el webhook esté configurado correctamente
2. Revisa logs del backend: `docker-compose logs backend -f`
3. Verifica que las API keys de Chatwoot sean correctas

---

## 🔒 Seguridad Post-Deployment

1. Cambia todas las contraseñas por defecto
2. Desactiva DEBUG en producción
3. Configura backups automáticos de PostgreSQL
4. Limita acceso al panel admin (opcional: agregar autenticación)

---

## 🎉 ¡Listo!

Tu chatbot inteligente ahora está funcionando en:
- **Panel Admin:** https://iaclub.pro
- **API:** https://api.iaclub.pro
- **Chatwoot:** Respuestas automáticas activas

---

## 📞 Soporte

Si tienes problemas:
1. Revisa logs en EasyPanel
2. Verifica que todas las variables de entorno estén configuradas
3. Confirma que los dominios estén apuntando correctamente

**¡Disfruta tu chatbot con IA!** 🤖✨
