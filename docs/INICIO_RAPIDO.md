# 🚀 Inicio Rápido del Sistema

## 📋 Opciones de Inicio

### 1️⃣ **START_BACKEND.bat** (Recomendado para desarrollo)
Inicia **SOLO el backend** del sistema.

```
✓ Backend API: http://localhost:8000
✓ Documentación: http://localhost:8000/docs
✓ Sin ngrok (para desarrollo local)
```

**Cuándo usar:**
- Desarrollo y pruebas locales
- Configurar plantillas de mensajes
- Probar el API
- No necesitas integración con Chatwoot

**Cómo usar:**
1. Doble clic en `START_BACKEND.bat`
2. Espera a que inicie el servidor
3. Abre http://localhost:8000/docs

---

### 2️⃣ **START_CHATBOT.bat** (Completo con opciones)
Inicia el sistema con un menú de opciones.

```
Opción 1: Solo backend (para desarrollo)
Opción 2: Backend + ngrok (para Chatwoot)
```

**Cuándo usar:**
- Cuando quieres elegir el modo de inicio
- Integración con Chatwoot (opción 2)
- URLs públicas con ngrok

---

## ⚡ Inicio Más Rápido

### Para desarrollo local:
```bash
# Opción A: Usar el .bat
START_BACKEND.bat

# Opción B: Desde terminal
cd backend
python -m uvicorn app.main:app --reload
```

### Para integración con Chatwoot:
```bash
START_CHATBOT.bat
# Selecciona opción 2
```

---

## 🔧 Verificar que todo funciona

### 1. Backend corriendo:
```bash
# Debe responder con JSON
http://localhost:8000/
```

### 2. Documentación API:
```bash
# Debe abrir Swagger UI
http://localhost:8000/docs
```

### 3. Health Check:
```bash
# Debe mostrar status: ok
http://localhost:8000/health
```

---

## 📚 Acceder a Módulos

### Plantillas de Mensajes (NUEVO):
```
GET  http://localhost:8000/templates
POST http://localhost:8000/templates
```
Documentación: Ver `GUIA_PLANTILLAS_MENSAJES.md`

### Base de Conocimientos:
```
GET  http://localhost:8000/knowledge
POST http://localhost:8000/knowledge
```

### FAQs:
```
GET  http://localhost:8000/faqs
POST http://localhost:8000/faqs
```

### Flujos:
```
GET  http://localhost:8000/flows
POST http://localhost:8000/flows
```

---

## 🐛 Problemas Comunes

### "Python no encontrado"
**Solución:**
1. Instala Python 3.10 o superior
2. Verifica: `python --version`
3. O usa el venv: `backend\venv\Scripts\python.exe`

### "ModuleNotFoundError"
**Solución:**
```bash
cd backend
pip install -r requirements.txt
# O instalar las básicas:
pip install fastapi uvicorn sqlalchemy pydantic
```

### "Puerto 8000 en uso"
**Solución:**
```bash
# Matar proceso en puerto 8000
netstat -ano | findstr :8000
taskkill /PID <numero_pid> /F
```

### "Error de base de datos"
**Solución:**
```bash
cd backend
alembic upgrade head
```

---

## 📱 Próximos Pasos

1. ✅ Backend iniciado
2. ✅ Crear plantillas en http://localhost:8000/docs
3. ✅ Ver guía completa: `GUIA_PLANTILLAS_MENSAJES.md`
4. 🔜 Iniciar frontend (si tienes)
5. 🔜 Configurar Chatwoot (si usas)

---

## 💡 Comandos Útiles

### Ver logs del backend:
Los logs se muestran en la ventana de PowerShell

### Reiniciar el servidor:
Presiona Ctrl+C y vuelve a ejecutar el .bat

### Detener todo:
Cierra la ventana de PowerShell del backend

---

## 📖 Más Información

- **Guía de Plantillas**: `GUIA_PLANTILLAS_MENSAJES.md`
- **Guía de Flujos**: `GUIA_FLUJOS.md`
- **Configuración**: `CONFIGURACION_MODULOS.md`
- **API Completa**: http://localhost:8000/docs (cuando esté corriendo)

---

¡Listo para empezar! 🚀
