# 🚀 GUÍA DE DESPLIEGUE EN EASY PANEL

## 📋 Pre-requisitos
- Cuenta en Easy Panel (donde ya tienes Chatwoot)
- Repositorio Git (GitHub, GitLab, etc.) con tu código
- Credenciales de OpenAI API

---

## 🔧 OPCIÓN 1: Desplegar Backend Solo (Recomendado)

### Paso 1: Preparar variables de entorno
Crea un archivo `.env.production` con:

```env
# Application
APP_NAME=IA Club - Tío IA
ENVIRONMENT=production
DEBUG=false

# Database (Easy Panel proveerá PostgreSQL)
DATABASE_URL=postgresql://user:password@postgres:5432/chatbot_db

# Redis (Easy Panel proveerá Redis)
REDIS_URL=redis://redis:6379/0

# OpenAI
OPENAI_API_KEY=tu-api-key-aqui
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=800

# Chatwoot
CHATWOOT_API_KEY=jNJLqH8cfYt1rUbsfsGjGeSm
CHATWOOT_BASE_URL=https://iaclub-chatwoot.ql7mr3.easypanel.host
CHATWOOT_ACCOUNT_ID=2

# CORS
CORS_ORIGINS=["*"]

# Security
SECRET_KEY=genera-una-clave-secreta-aqui-con-openssl
API_KEY_HEADER=X-API-Key

# Upload
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE=10485760
```

### Paso 2: Subir código a Git

```bash
# Inicializar repositorio Git (si no lo has hecho)
cd "C:\Users\Guerr\Music\BOT PYTHON + CHATWOOT"
git init
git add .
git commit -m "Initial commit - IA Club Bot"

# Crear repositorio en GitHub/GitLab y subir
git remote add origin https://github.com/tu-usuario/iaclub-bot.git
git branch -M main
git push -u origin main
```

### Paso 3: Crear aplicación en Easy Panel

1. **Ingresa a Easy Panel:**
   - URL: Tu panel de Easy Panel (donde tienes Chatwoot)

2. **Crear nueva aplicación:**
   - Clic en "Apps" → "Create App"
   - Selecciona: **"From Git Repository"**

3. **Configurar repositorio:**
   - Repository URL: `https://github.com/tu-usuario/iaclub-bot.git`
   - Branch: `main`
   - Build context: `backend` (importante)

4. **Configurar build:**
   - Dockerfile path: `Dockerfile`
   - Build args: (dejar vacío)

5. **Configurar servicios adicionales:**
   
   **PostgreSQL:**
   - Clic en "Add Service" → "PostgreSQL"
   - Nombre: `postgres`
   - Database: `chatbot_db`
   - User: `chatbot_user`
   - Password: (generar una segura)
   - **Copiar la DATABASE_URL generada**

   **Redis:**
   - Clic en "Add Service" → "Redis"
   - Nombre: `redis`
   - **Copiar la REDIS_URL generada**

6. **Configurar variables de entorno:**
   En la sección "Environment Variables", agregar:
   ```
   APP_NAME=IA Club - Tío IA
   ENVIRONMENT=production
   DEBUG=false
   DATABASE_URL=<copiar de PostgreSQL>
   REDIS_URL=<copiar de Redis>
   OPENAI_API_KEY=sk-proj-...
   OPENAI_MODEL=gpt-4-turbo-preview
   OPENAI_TEMPERATURE=0.7
   OPENAI_MAX_TOKENS=800
   CHATWOOT_API_KEY=jNJLqH8cfYt1rUbsfsGjGeSm
   CHATWOOT_BASE_URL=https://iaclub-chatwoot.ql7mr3.easypanel.host
   CHATWOOT_ACCOUNT_ID=2
   CORS_ORIGINS=["*"]
   SECRET_KEY=<generar clave segura>
   ```

7. **Configurar puerto:**
   - Port: `8000`
   - Protocol: `HTTP`

8. **Configurar dominio:**
   - Agregar subdominio: `iaclub-bot.tu-dominio.com`
   - O usar el dominio de Easy Panel: `app-name.easypanel-random.app`

9. **Deploy:**
   - Clic en "Deploy"
   - Esperar que el build termine (~3-5 minutos)

### Paso 4: Inicializar base de datos

Una vez desplegado, ejecutar migraciones:

1. En Easy Panel, ir a tu app
2. Abrir "Console" o "Shell"
3. Ejecutar:
```bash
alembic upgrade head
```

### Paso 5: Cargar contenido inicial

Ejecutar scripts de carga:
```bash
python load_iaclub_content.py
python configure_iaclub_agents.py
```

### Paso 6: Actualizar webhook en Chatwoot

1. Ir a Chatwoot → Settings → Integrations → Webhooks
2. Editar webhook existente
3. Nueva URL: `https://iaclub-bot.tu-dominio.com/webhook/chatwoot`
4. Guardar

---

## 🔧 OPCIÓN 2: Desplegar con Docker Compose

Si Easy Panel soporta docker-compose:

1. **Subir proyecto completo a Git**

2. **En Easy Panel:**
   - Create App → Docker Compose
   - Repository: tu repositorio
   - Compose file: `docker-compose.yml`

3. **Modificar variables de entorno** en Easy Panel

4. **Deploy**

---

## ✅ Verificación

Una vez desplegado, verifica:

1. **Health check:**
   ```bash
   curl https://iaclub-bot.tu-dominio.com/
   # Debe retornar: {"app":"IA Club - Tío IA","version":"1.0.0","status":"running"}
   ```

2. **Documentación API:**
   - Si DEBUG=true: `https://iaclub-bot.tu-dominio.com/docs`

3. **Webhook:**
   ```bash
   curl -X POST https://iaclub-bot.tu-dominio.com/webhook/chatwoot \
     -H "Content-Type: application/json" \
     -d '{"event":"message_created","message_type":"incoming","conversation":{"id":123},"content":"test","sender":{"name":"Test"}}'
   ```

4. **Test en Chatwoot:**
   - Enviar mensaje en conversación
   - Bot debe responder automáticamente

---

## 🔄 Actualizar aplicación

Después de hacer cambios:

```bash
git add .
git commit -m "Descripción de cambios"
git push origin main
```

En Easy Panel:
- Ir a tu app → "Deployments"
- Clic en "Redeploy" o esperar auto-deploy (si está habilitado)

---

## 📊 Monitoreo

En Easy Panel puedes ver:
- **Logs:** Logs en tiempo real de tu aplicación
- **Metrics:** CPU, RAM, requests
- **Console:** Ejecutar comandos en el contenedor

---

## 🐛 Troubleshooting

### Error: "App failed to start"
- Revisar logs en Easy Panel
- Verificar variables de entorno
- Verificar que DATABASE_URL y REDIS_URL sean correctas

### Error: "Database connection failed"
- Verificar que PostgreSQL esté corriendo
- Verificar DATABASE_URL
- Ejecutar migraciones: `alembic upgrade head`

### Error: "Webhook not working"
- Verificar URL en Chatwoot
- Verificar que el dominio sea accesible públicamente
- Revisar logs del backend

### Performance lento
- Aumentar recursos (RAM/CPU) en Easy Panel
- Optimizar consultas a base de datos
- Habilitar Redis cache

---

## 💡 Recomendaciones

1. **Usa PostgreSQL** en producción (no SQLite)
2. **Habilita Redis** para mejor performance
3. **Configura backups** automáticos de la base de datos
4. **Monitorea logs** regularmente
5. **Usa HTTPS** siempre (Easy Panel lo provee automáticamente)
6. **Configura alertas** en Easy Panel para downtime
7. **Mantén SECRET_KEY seguro** y único

---

## 📝 Variables de entorno críticas

✅ Requeridas:
- `OPENAI_API_KEY`
- `CHATWOOT_API_KEY`
- `CHATWOOT_BASE_URL`
- `CHATWOOT_ACCOUNT_ID`
- `DATABASE_URL`
- `SECRET_KEY`

⚠️ Opcionales pero recomendadas:
- `REDIS_URL` (para cache)
- `CORS_ORIGINS` (para seguridad)
- `DEBUG=false` (en producción)

---

## 🎯 URLs finales

Después del despliegue:
- **API:** `https://iaclub-bot.tu-dominio.com`
- **Docs:** `https://iaclub-bot.tu-dominio.com/docs` (solo si DEBUG=true)
- **Webhook:** `https://iaclub-bot.tu-dominio.com/webhook/chatwoot`
- **Health:** `https://iaclub-bot.tu-dominio.com/health`

---

¿Necesitas ayuda con algún paso específico? 🚀
