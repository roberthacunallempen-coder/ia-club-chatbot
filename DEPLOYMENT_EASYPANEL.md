# 🚀 GUÍA DE DEPLOYMENT EN EASYPANEL

## 📋 PRE-REQUISITOS

1. **Servidor VPS** con Ubuntu 20.04+ (DigitalOcean, Linode, Vultr, etc.)
2. **Dominio** apuntando al servidor (A record)
3. **Easypanel instalado** en el servidor
4. **Cuenta de OpenAI** con API key
5. **Cuenta de Chatwoot** (opcional pero recomendado)

---

## 🔧 PASO 1: INSTALAR EASYPANEL

SSH a tu servidor y ejecuta:

```bash
curl -sSL https://get.easypanel.io | sh
```

Esto instala:
- Docker
- Docker Compose
- Easypanel Dashboard

Accede a Easypanel en: `http://tu-ip:3000`

---

## 📦 PASO 2: PREPARAR VARIABLES DE ENTORNO

### 2.1 Generar claves secretas

En tu computadora local, ejecuta:

```bash
# PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

O usa este sitio: https://www.random.org/strings/

Guarda 2 claves diferentes para:
- `SECRET_KEY`
- `JWT_SECRET_KEY`

### 2.2 Configurar variables

Crea un archivo `.env` con estos valores:

```env
# Database
POSTGRES_PASSWORD=un-password-muy-seguro-aqui
DATABASE_URL=postgresql://chatbot_user:un-password-muy-seguro-aqui@postgres:5432/chatbot_db

# OpenAI
OPENAI_API_KEY=sk-tu-api-key-de-openai
OPENAI_MODEL=gpt-4o-mini

# Chatwoot
CHATWOOT_URL=https://app.chatwoot.com
CHATWOOT_ACCESS_TOKEN=tu-token-aqui
CHATWOOT_ACCOUNT_ID=123
CHATWOOT_INBOX_ID=456
CHATWOOT_WEBHOOK_SECRET=webhook-secret-aleatorio

# Security
SECRET_KEY=la-clave-aleatoria-que-generaste-1
JWT_SECRET_KEY=la-clave-aleatoria-que-generaste-2
ADMIN_USERNAME=admin
ADMIN_PASSWORD=un-password-seguro-para-admin

# App
ENVIRONMENT=production
ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com

# Rate Limiting
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=500

# Frontend
VITE_API_URL=https://api.tudominio.com
```

---

## 🎯 PASO 3: DEPLOYMENT EN EASYPANEL

### 3.1 Crear Proyecto

1. En Easypanel, clic en **"New Project"**
2. Nombre: `ia-club-chatbot`
3. Clic en **"Create"**

### 3.2 Agregar PostgreSQL

1. Clic en **"Add Service"** → **"Database"** → **"PostgreSQL"**
2. Nombre: `postgres`
3. Version: `16`
4. Username: `chatbot_user`
5. Password: (el que pusiste en `POSTGRES_PASSWORD`)
6. Database: `chatbot_db`
7. Clic en **"Create"**

### 3.3 Agregar Redis

1. Clic en **"Add Service"** → **"Database"** → **"Redis"**
2. Nombre: `redis`
3. Version: `7`
4. Clic en **"Create"**

### 3.4 Agregar Backend

1. Clic en **"Add Service"** → **"App"** → **"From Source Code"**
2. Nombre: `backend`
3. **Repository:**
   - Git URL: URL de tu repositorio GitHub
   - Branch: `main`
   - Build Path: `/backend`
4. **Build Settings:**
   - Build Command: (dejar vacío, usa Dockerfile)
   - Dockerfile Path: `backend/Dockerfile`
5. **Deploy Settings:**
   - Port: `8000`
6. **Environment Variables:** (copiar todas las del archivo .env)
7. **Domains:**
   - Agregar: `api.tudominio.com`
   - Enable SSL: ✅
8. Clic en **"Create"**

### 3.5 Agregar Frontend

1. Clic en **"Add Service"** → **"App"** → **"From Source Code"**
2. Nombre: `frontend`
3. **Repository:** (mismo que backend)
   - Build Path: `/frontend`
4. **Build Settings:**
   - Dockerfile Path: `frontend/Dockerfile`
5. **Deploy Settings:**
   - Port: `80`
6. **Environment Variables:**
   ```
   VITE_API_URL=https://api.tudominio.com
   ```
7. **Domains:**
   - Agregar: `tudominio.com`
   - Agregar: `www.tudominio.com`
   - Enable SSL: ✅
8. Clic en **"Create"**

---

## 🔐 PASO 4: CONFIGURAR DNS

En tu proveedor de dominio (GoDaddy, Namecheap, etc.):

```
Tipo    Nombre    Valor           TTL
A       @         IP-DEL-SERVIDOR 300
A       www       IP-DEL-SERVIDOR 300
A       api       IP-DEL-SERVIDOR 300
```

Espera 5-15 minutos para propagación DNS.

---

## ✅ PASO 5: VERIFICAR DEPLOYMENT

### 5.1 Verificar Backend

Abre: `https://api.tudominio.com`

Deberías ver:
```json
{
  "app": "IA Club Chatbot",
  "version": "1.0.0",
  "status": "running",
  "environment": "production"
}
```

### 5.2 Verificar Frontend

Abre: `https://tudominio.com`

Deberías ver el dashboard del chatbot.

### 5.3 Verificar Database

En Easypanel, ve a PostgreSQL → **Logs**

Deberías ver:
```
database system is ready to accept connections
```

---

## 🔗 PASO 6: CONFIGURAR CHATWOOT

### 6.1 Obtener Tokens de Chatwoot

1. Login a Chatwoot: https://app.chatwoot.com
2. Ve a **Settings** → **Integrations** → **API**
3. Clic en **"Create API Key"**
4. Copia el **Access Token**

### 6.2 Encontrar IDs

En Chatwoot, abre:
- **Account ID:** URL → `/app/accounts/[ESTE-ES-TU-ID]/...`
- **Inbox ID:** Ve a Inboxes → Clic en tu inbox → URL tiene el ID

### 6.3 Configurar Webhook

1. En Chatwoot: **Settings** → **Webhooks**
2. Clic en **"Add Webhook"**
3. **URL:** `https://api.tudominio.com/webhook/chatwoot`
4. **Events:** Selecciona:
   - `message_created`
   - `conversation_created`
   - `conversation_status_changed`
5. Clic en **"Save"**

### 6.4 Actualizar Variables en Easypanel

1. Ve al servicio `backend`
2. Clic en **"Environment"**
3. Actualiza:
   ```
   CHATWOOT_ACCESS_TOKEN=tu-token-real
   CHATWOOT_ACCOUNT_ID=123
   CHATWOOT_INBOX_ID=456
   ```
4. Clic en **"Save & Redeploy"**

---

## 📊 PASO 7: MONITOREO

### 7.1 Verificar Logs

En Easypanel:
- Backend → **Logs**
- Frontend → **Logs**
- PostgreSQL → **Logs**
- Redis → **Logs**

### 7.2 Setup Monitoring (Opcional)

**UptimeRobot** (Gratis):
1. Crear cuenta: https://uptimerobot.com
2. Add Monitor:
   - URL: `https://api.tudominio.com/health`
   - Type: HTTP(s)
   - Interval: 5 minutes
3. Recibirás alertas si el sitio cae

---

## 🔄 PASO 8: BACKUPS

### 8.1 Backup Manual de Database

En Easypanel, en el servicio PostgreSQL:

```bash
# Dentro del contenedor
pg_dump -U chatbot_user chatbot_db > backup.sql
```

### 8.2 Backup Automático

Easypanel Pro incluye backups automáticos de PostgreSQL.

O usa este script (ejecutar con cron):

```bash
#!/bin/bash
docker exec postgres pg_dump -U chatbot_user chatbot_db | gzip > backup-$(date +%Y%m%d).sql.gz
```

---

## 🚨 TROUBLESHOOTING

### Backend no inicia

**Check logs:**
```bash
docker logs backend
```

**Común:**
- Variables de entorno incorrectas
- Database no conecta
- OpenAI API key inválida

### Frontend no carga

**Check:**
1. `VITE_API_URL` apunta al backend correcto
2. CORS permite tu dominio frontend
3. SSL funcionando

### Chatwoot no responde

**Check:**
1. Webhook configurado correctamente
2. Access token válido
3. Account ID e Inbox ID correctos
4. Logs del backend para errores

---

## 📈 OPTIMIZACIONES POST-DEPLOYMENT

### 1. Configurar CDN (Opcional)

Cloudflare gratis:
1. Agregar dominio a Cloudflare
2. Cambiar nameservers
3. Enable "Proxied" (naranja)
4. SSL/TLS → Full (strict)

### 2. Configurar Limpieza de Logs

En Easypanel → Settings → Logs:
- Retention: 7 días
- Max size: 100MB

### 3. Escalar Resources

Si tienes mucho tráfico:
- Easypanel → Backend → Resources
- Memory: 512MB → 1GB
- CPU: 0.5 → 1.0

---

## 💰 COSTOS MENSUALES

| Item | Costo |
|------|-------|
| VPS (2GB RAM) | $6-12 |
| Dominio | ~$1 |
| OpenAI API | Variable* |
| Easypanel | Gratis |
| PostgreSQL | Incluido |
| Redis | Incluido |
| SSL | Gratis |

**Total:** $7-13/mes + uso de OpenAI

*Con respuestas concisas (~150 tokens) y 1000 mensajes/día: ~$15-30/mes

---

## ✅ CHECKLIST FINAL

- [ ] Easypanel instalado
- [ ] Dominio apuntando al servidor
- [ ] PostgreSQL creado
- [ ] Redis creado
- [ ] Backend deployado
- [ ] Frontend deployado
- [ ] SSL activado (candado verde)
- [ ] Variables de entorno configuradas
- [ ] Chatwoot webhook configurado
- [ ] Backups configurados
- [ ] Monitoring activo
- [ ] Test completo del chatbot

---

## 🎉 ¡LISTO!

Tu chatbot está en producción. Accede a:

- **Frontend:** https://tudominio.com
- **Backend API:** https://api.tudominio.com
- **Admin Panel:** https://tudominio.com/settings
- **Test Bot:** https://tudominio.com/test-bot

**Login admin:**
- Usuario: (el que pusiste en `ADMIN_USERNAME`)
- Password: (el que pusiste en `ADMIN_PASSWORD`)

---

## 📞 SOPORTE

Si tienes problemas:
1. Check logs en Easypanel
2. Verifica variables de entorno
3. Prueba endpoints manualmente
4. Revisa documentación de Easypanel

¡Disfruta tu chatbot en producción! 🚀
