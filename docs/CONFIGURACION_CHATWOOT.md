# 🔗 Guía de Conexión con Chatwoot

## 📋 Pasos para Conectar tu Bot con Chatwoot

### 1️⃣ Obtener Credenciales de Chatwoot

**a) Inicia sesión en Chatwoot:**
- Ve a tu instancia de Chatwoot: `https://app.chatwoot.com` (o tu dominio personalizado)
- Inicia sesión con tu cuenta

**b) Obtén tu API Key:**
1. Haz clic en tu **avatar/perfil** (esquina superior derecha)
2. Selecciona **"Profile Settings"**
3. Ve a la pestaña **"Access Token"**
4. Copia tu **Personal Access Token** (se ve como: `abc123xyz...`)

**c) Obtén tu Account ID:**
1. En el panel de Chatwoot, mira la URL
2. Se verá algo como: `https://app.chatwoot.com/app/accounts/12345/...`
3. El número después de `/accounts/` es tu **Account ID** (ejemplo: `12345`)

**d) Obtén la URL base:**
- Si usas Chatwoot Cloud: `https://app.chatwoot.com`
- Si tienes instancia propia: `https://tu-dominio.com`

---

### 2️⃣ Configurar Variables de Entorno

**Edita el archivo `.env.local`:**

```bash
cd "C:\Users\Guerr\Music\BOT PYTHON + CHATWOOT\backend"
notepad .env.local
```

**Actualiza estas líneas:**

```env
# CHATWOOT
CHATWOOT_API_KEY=TU_TOKEN_AQUI              # 👈 Token de Access Token
CHATWOOT_BASE_URL=https://app.chatwoot.com  # 👈 URL de tu Chatwoot
CHATWOOT_ACCOUNT_ID=12345                   # 👈 Tu Account ID
```

**Ejemplo completo:**
```env
CHATWOOT_API_KEY=abc123xyz789...
CHATWOOT_BASE_URL=https://app.chatwoot.com
CHATWOOT_ACCOUNT_ID=12345
```

---

### 3️⃣ Crear Inbox en Chatwoot

**a) Crear un nuevo Inbox:**
1. En Chatwoot, ve a **Settings** → **Inboxes**
2. Haz clic en **"Add Inbox"**
3. Selecciona **"API"** (o "Website" si prefieres widget web)
4. Dale un nombre: `IA Club Bot` o el que prefieras
5. Guarda el inbox

**b) Obtener Inbox ID (opcional):**
- Una vez creado, ve a la configuración del inbox
- En la URL verás algo como: `/app/accounts/123/settings/inboxes/456`
- El último número (`456`) es tu Inbox ID

---

### 4️⃣ Configurar Webhook en Chatwoot

**a) Ve a Webhooks:**
1. En Chatwoot: **Settings** → **Integrations** → **Webhooks**
2. Haz clic en **"Add Webhook"**

**b) Configuración del Webhook:**

**URL del Webhook:**
```
https://TU-DOMINIO.COM/webhook/chatwoot
```

**Para desarrollo local (con ngrok o similar):**
```
https://tu-subdominio.ngrok.io/webhook/chatwoot
```

**Eventos a suscribir:**
- ✅ `message_created` (OBLIGATORIO)
- ✅ `conversation_created` (recomendado)
- ✅ `conversation_updated` (opcional)

**c) Guarda el webhook**

---

### 5️⃣ Exponer tu API (Para Desarrollo Local)

Si estás en desarrollo local, necesitas exponer tu API para que Chatwoot pueda enviar webhooks:

**Opción A: Usar ngrok (Recomendado)**

1. **Descarga ngrok:**
   - https://ngrok.com/download
   - Crea cuenta gratuita

2. **Instala y ejecuta:**
   ```bash
   ngrok http 8000
   ```

3. **Copia la URL pública:**
   ```
   Forwarding: https://abc123.ngrok.io -> http://localhost:8000
   ```

4. **Usa esta URL en Chatwoot:**
   ```
   https://abc123.ngrok.io/webhook/chatwoot
   ```

**Opción B: Usar Cloudflare Tunnel**
```bash
cloudflared tunnel --url http://localhost:8000
```

**Opción C: Desplegar en servidor (Producción)**
- Sigue la guía en `DEPLOYMENT_GUIDE.md`

---

### 6️⃣ Verificar la Conexión

**a) Reinicia tu bot:**
```bash
.\STOP_CHATBOT.bat
.\START_CHATBOT.bat
```

**b) Verifica que las variables se cargaron:**
```bash
cd backend
.\venv\Scripts\python.exe -c "from app.config import settings; print('API Key:', settings.chatwoot_api_key[:10] + '...'); print('Base URL:', settings.chatwoot_base_url); print('Account ID:', settings.chatwoot_account_id)"
```

**c) Prueba el webhook manualmente:**

Ve a: `http://localhost:8000/docs`

Busca el endpoint: `POST /webhook/chatwoot`

Prueba con este payload:
```json
{
  "event": "message_created",
  "message_type": "incoming",
  "conversation": {
    "id": 123
  },
  "content": "Hola, quiero información sobre los planes",
  "sender": {
    "name": "Cliente Test",
    "email": "test@example.com"
  }
}
```

---

### 7️⃣ Enviar Mensaje de Prueba desde Chatwoot

**a) Crea una conversación de prueba:**
1. En Chatwoot, ve a **Conversations**
2. Haz clic en **"New Conversation"**
3. Selecciona el inbox que creaste
4. Envía un mensaje como cliente

**b) El bot debería responder automáticamente:**
- Verás la respuesta en la conversación de Chatwoot
- En los logs del backend verás: `Processing message from conversation...`

---

## 🔍 Troubleshooting

### Problema 1: "Webhook not receiving messages"

**Verifica:**
```bash
# En backend, revisa logs
tail -f logs/app.log

# O en Windows PowerShell
Get-Content -Path "logs\app.log" -Wait
```

**Soluciones:**
- ✅ Verifica que la URL del webhook sea accesible desde internet
- ✅ Prueba la URL manualmente: `curl https://tu-url.com/webhook/chatwoot`
- ✅ Verifica que los eventos correctos estén suscritos (`message_created`)

### Problema 2: "Bot not responding"

**Verifica variables de entorno:**
```python
python -c "from app.config import settings; print(settings.chatwoot_api_key)"
```

**Verifica que OpenAI funcione:**
```python
python -c "from app.services.openai_service import openai_service; print('OK' if openai_service else 'ERROR')"
```

### Problema 3: "403 Forbidden en Chatwoot"

**Causa:** API Key incorrecta

**Solución:**
1. Regenera tu Personal Access Token en Chatwoot
2. Actualiza `.env.local` con el nuevo token
3. Reinicia el bot

### Problema 4: "404 Not Found"

**Causa:** Account ID incorrecto

**Solución:**
1. Verifica el Account ID en la URL de Chatwoot
2. Actualiza `CHATWOOT_ACCOUNT_ID` en `.env.local`

---

## 📊 Verificar que Todo Funciona

### Checklist Final:

- [ ] ✅ Variables de entorno configuradas (API Key, Base URL, Account ID)
- [ ] ✅ Inbox creado en Chatwoot
- [ ] ✅ Webhook configurado con URL correcta
- [ ] ✅ Webhook suscrito a `message_created`
- [ ] ✅ Backend corriendo sin errores
- [ ] ✅ URL del webhook accesible desde internet (ngrok/cloudflare/servidor)
- [ ] ✅ Mensaje de prueba enviado y respondido

---

## 🎯 Flujo Completo de una Conversación

```
1. Cliente envía mensaje en Chatwoot
   ↓
2. Chatwoot envía webhook a tu API
   POST https://tu-api.com/webhook/chatwoot
   ↓
3. Tu bot (IntelligentAgent) procesa el mensaje
   - Clasifica intención
   - Busca conocimiento relevante
   - Detecta perfil del cliente
   - Maneja objeciones si hay
   - Verifica si hay flujo activo
   ↓
4. Bot genera respuesta personalizada
   ↓
5. Bot envía respuesta a Chatwoot API
   POST https://app.chatwoot.com/api/v1/accounts/{id}/conversations/{id}/messages
   ↓
6. Cliente ve la respuesta en tiempo real
```

---

## 🚀 Comandos Útiles

**Ver logs en tiempo real:**
```powershell
Get-Content -Path "backend\logs\app.log" -Wait -Tail 50
```

**Probar webhook localmente:**
```powershell
curl -X POST http://localhost:8000/webhook/chatwoot `
  -H "Content-Type: application/json" `
  -d '{"event":"message_created","message_type":"incoming","conversation":{"id":123},"content":"Hola","sender":{"name":"Test"}}'
```

**Verificar que Chatwoot API funciona:**
```powershell
curl -H "api_access_token: TU_TOKEN" https://app.chatwoot.com/api/v1/accounts/TU_ACCOUNT_ID/conversations
```

---

## 📚 Recursos Adicionales

- **Documentación Chatwoot API:** https://www.chatwoot.com/developers/api/
- **Webhooks de Chatwoot:** https://www.chatwoot.com/docs/product/channels/api/webhooks
- **ngrok:** https://ngrok.com/docs
- **Documentación del Bot:** Ver `MEJORAS_IMPLEMENTADAS.md` y `CONFIGURACION_MODULOS.md`

---

## 💡 Tips Pro

1. **Para producción:** Usa un dominio propio con SSL (no ngrok gratuito)
2. **Logs:** Activa logs detallados para debugging
3. **Rate limits:** Chatwoot tiene límites de API, implementa caché si tienes mucho tráfico
4. **Múltiples inboxes:** Puedes crear varios inboxes (web, WhatsApp, etc.) todos apuntando al mismo webhook
5. **Automatización:** El bot responde solo a mensajes `incoming`, no a mensajes de agentes

---

## 🔐 Seguridad

**Variables sensibles:**
- ✅ Nunca subas `.env.local` a Git (ya está en `.gitignore`)
- ✅ Usa variables de entorno en producción
- ✅ Rota tus tokens periódicamente
- ✅ Usa HTTPS siempre (obligatorio para webhooks)

**Webhook security (opcional pero recomendado):**
```python
# Agregar validación de firma en webhook.py
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

---

¡Ya estás listo para conectar tu bot con Chatwoot! 🎉

Si tienes dudas, revisa los logs o contacta soporte.
