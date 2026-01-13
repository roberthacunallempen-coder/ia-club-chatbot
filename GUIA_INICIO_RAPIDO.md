# 🚀 Guía de Inicio Rápido

## Iniciar el Sistema (LA FORMA MÁS FÁCIL)

### Opción 1: Doble clic en el archivo
1. Ve a la carpeta del proyecto
2. **Doble clic en `INICIAR_TODO.bat`**
3. ¡Listo! El sistema se inicia automáticamente

### Opción 2: Desde PowerShell
```powershell
.\INICIAR_TODO.ps1
```

### Opción 3: Desde el Explorador de Archivos
Haz clic derecho en `INICIAR_TODO.bat` → **Ejecutar como administrador**

---

## Detener el Sistema

### Forma fácil:
**Doble clic en `DETENER_TODO.bat`**

### Desde PowerShell:
```powershell
.\DETENER_TODO.ps1
```

### Forma manual:
Cierra las ventanas de PowerShell donde están corriendo Backend y Frontend

---

## URLs del Sistema

Una vez iniciado, accede a:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:5173 | Interfaz principal |
| **Test Bot** | http://localhost:5173/test-bot | Probar el bot |
| **Plantillas** | http://localhost:5173/templates | Gestionar plantillas |
| **Backend API** | http://localhost:8000 | API REST |
| **API Docs** | http://localhost:8000/docs | Documentación interactiva |

---

## Solución de Problemas

### ❌ Error: "Puerto ya en uso"
**Solución:** Ejecuta `DETENER_TODO.bat` primero, luego vuelve a iniciar

### ❌ Error: "No se puede ejecutar scripts"
**Solución:** Abre PowerShell como administrador y ejecuta:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❌ Frontend no carga
1. Verifica que Backend esté corriendo: http://localhost:8000
2. Abre la consola del navegador (F12) para ver errores
3. Reinicia con `DETENER_TODO.bat` → `INICIAR_TODO.bat`

### ❌ "ModuleNotFoundError" en Python
**Solución:** Las dependencias no están instaladas. Ejecuta:
```powershell
cd backend
pip install -r requirements.txt
```

---

## Comandos Útiles

### Ver logs del backend
Las ventanas de PowerShell muestran los logs en tiempo real

### Reiniciar solo el Backend
```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Reiniciar solo el Frontend
```powershell
cd frontend
npm run dev
```

---

## Atajos de Teclado

En las ventanas de PowerShell:
- **Ctrl + C** = Detener el servicio
- **Ctrl + Scroll** = Zoom de la terminal

En el navegador (Frontend):
- **F12** = Abrir consola de desarrollador
- **Ctrl + R** = Recargar página
- **Ctrl + Shift + R** = Recargar sin caché

---

## Primer Uso

1. **Inicia el sistema**: `INICIAR_TODO.bat`
2. **Abre el navegador**: http://localhost:5173
3. **Ve a Test Bot**: http://localhost:5173/test-bot
4. **Prueba escribiendo**: "hola" (activará la plantilla de bienvenida)

---

## Estructura de Archivos Importantes

```
📁 BOT PYTHON + CHATWOOT/
├── 🚀 INICIAR_TODO.bat          ← USAR ESTE PARA INICIAR
├── 🛑 DETENER_TODO.bat          ← USAR ESTE PARA DETENER
├── 📝 GUIA_INICIO_RAPIDO.md     ← Estás aquí
├── 📁 backend/                  ← Código Python/FastAPI
├── 📁 frontend/                 ← Código React/Vite
└── 📁 backend/uploads/          ← Archivos subidos
```

---

## Próximos Pasos

✅ Sistema iniciado
✅ Plantillas configuradas
→ Ahora puedes:
  - Crear nuevas plantillas en `/templates`
  - Probar el bot en `/test-bot`
  - Agregar contenido en `/knowledge`
  - Configurar Chatwoot en `/settings`

---

**¿Problemas?** Revisa los logs en las ventanas de PowerShell o abre un issue en el repositorio.
