# 🎉 MÓDULO DE PLANTILLAS DE MENSAJES COMPLETADO

## ✅ Implementación Finalizada

Se ha implementado exitosamente el **Sistema de Plantillas de Mensajes Predeterminadas** que te permite:

### 🎯 Funcionalidad Principal
- ✅ Crear secuencias de mensajes con orden específico que TÚ controlas
- ✅ Enviar texto, imágenes, PDFs, audio y video en el orden que configures
- ✅ El bot NO modifica ni cambia el orden - todo es predeterminado
- ✅ Variables dinámicas para personalización (`{nombre}`, `{producto}`, etc.)
- ✅ Delays configurables entre mensajes (0-60 segundos)
- ✅ Activación automática por palabras clave
- ✅ Categorización y organización de plantillas

---

## 📁 Archivos Creados

### Backend (Python/FastAPI)

1. **`backend/app/models/message_template.py`**
   - Modelo de base de datos para almacenar plantillas
   - Campos: name, description, messages (JSON), category, trigger_keywords, is_active

2. **`backend/app/schemas/message_template.py`**
   - Esquemas Pydantic para validación
   - MessageTemplateCreate, MessageTemplateUpdate, MessageTemplateResponse
   - Validaciones automáticas de orden secuencial

3. **`backend/app/api/message_templates.py`**
   - Endpoints REST completos (CRUD)
   - GET /templates - Listar plantillas
   - POST /templates - Crear plantilla
   - PUT /templates/{id} - Actualizar
   - DELETE /templates/{id} - Eliminar
   - POST /templates/send - Enviar a conversación
   - POST /templates/upload-file - Subir archivos

4. **`backend/app/bot/template_manager.py`**
   - Lógica de negocio para gestión de plantillas
   - `send_template_by_name()` - Enviar por nombre
   - `send_template_by_id()` - Enviar por ID
   - `auto_send_template()` - Envío automático por keywords
   - `find_template_by_keyword()` - Búsqueda por palabras clave

5. **`backend/app/services/chatwoot_service.py`** (Extendido)
   - `send_attachment()` - Enviar archivos a Chatwoot
   - `send_template_sequence()` - Enviar secuencias ordenadas
   - Soporte para delays y reemplazo de variables

6. **`backend/app/bot/intelligent_agent.py`** (Integrado)
   - Integración con el flujo principal del bot
   - Verificación automática de plantillas por keywords
   - Prioridad sobre respuestas generadas por IA

7. **`backend/alembic/versions/add_message_templates.py`**
   - Migración de base de datos
   - Crea tabla `message_templates` con índices

### Frontend (React)

8. **`frontend/src/pages/MessageTemplates/MessageTemplates.jsx`**
   - Interfaz completa de gestión
   - Crear/Editar/Eliminar plantillas
   - Configurar mensajes con drag & drop (orden)
   - Subir archivos directamente
   - Filtros por categoría
   - Preview de plantillas

9. **`frontend/src/App.jsx`** (Actualizado)
   - Nueva ruta `/templates`

10. **`frontend/src/components/Layout/Layout.jsx`** (Actualizado)
    - Nuevo ítem de menú "Plantillas de Mensajes"

### Documentación

11. **`GUIA_PLANTILLAS_MENSAJES.md`**
    - Documentación completa del sistema
    - Ejemplos de uso
    - API endpoints
    - Casos de uso
    - Mejores prácticas
    - Troubleshooting

12. **`backend/ejemplo_plantillas.py`**
    - Script de demostración
    - Crea 3 plantillas de ejemplo
    - Muestra cómo usar la API
    - Incluye ejemplos reales

13. **`README.md`** (Actualizado)
    - Mención del nuevo módulo
    - Enlaces a documentación

---

## 🚀 Cómo Empezar a Usar

### 1. Aplicar Migración de Base de Datos

```bash
cd backend
alembic upgrade head
```

O manualmente:
```sql
CREATE TABLE message_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE,
    description TEXT,
    messages JSONB NOT NULL,
    category VARCHAR(100),
    trigger_keywords JSONB,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### 2. Ejecutar el Script de Ejemplo

```bash
cd backend
python ejemplo_plantillas.py
```

Esto creará 3 plantillas de demostración:
- **Bienvenida_Demo** (keywords: hola, buenos días)
- **Info_Cursos_Demo** (keywords: cursos, formación)
- **Info_Precios_Demo** (keywords: precio, costo)

### 3. Acceder a la Interfaz Web

1. Inicia el servidor:
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn app.main:app --reload

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. Abre el navegador: `http://localhost:5173/templates`

3. ¡Empieza a crear tus plantillas! 🎉

### 4. Probar el Bot con Keywords

Escribe en el chat:
- "hola" → Recibirás la plantilla de bienvenida
- "cursos" → Recibirás info de cursos
- "precio" → Recibirás info de precios

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Crear Plantilla desde la UI

1. Ve a **Plantillas de Mensajes**
2. Clic en **Nueva Plantilla**
3. Completa:
   - Nombre: "Onboarding_Nuevos"
   - Categoría: "bienvenida"
   - Keywords: ["empezar", "comenzar", "inicio"]

4. Añade mensajes:
   ```
   Mensaje 1 (Texto, 0s):
   "¡Bienvenido {nombre}! Vamos a configurar tu cuenta paso a paso 🚀"

   Mensaje 2 (Imagen, 2s):
   [Sube una imagen de bienvenida]

   Mensaje 3 (Documento, 3s):
   [Sube un PDF con instrucciones]

   Mensaje 4 (Texto, 5s):
   "¿Todo listo para empezar? 😊"
   ```

5. Guarda y activa la plantilla

### Ejemplo 2: Enviar Plantilla por API

```python
import httpx

async def enviar_plantilla():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/templates/send",
            json={
                "template_id": 1,
                "conversation_id": 12345,
                "variables": {
                    "nombre": "María",
                    "producto": "Curso de IA"
                }
            }
        )
        print(response.json())
```

### Ejemplo 3: Integración con Bot

El bot automáticamente:
1. Detecta keywords en mensajes del usuario
2. Busca plantillas activas con esas keywords
3. Envía la plantilla automáticamente
4. El usuario recibe los mensajes en orden

```
Usuario: "Hola, cuanto cuesta el curso?"
Bot: 
  [Detecta "hola" → Envía plantilla de bienvenida]
  [Detecta "cuanto cuesta" → Envía plantilla de precios]
```

---

## 🎨 Casos de Uso Reales

### 1. E-commerce
```
Plantilla: "Info_Producto_X"
- Texto: Descripción del producto
- Imagen: Foto del producto
- Documento: Ficha técnica PDF
- Texto: "¿Quieres comprarlo?"
```

### 2. Soporte Técnico
```
Plantilla: "Solución_Problema_Y"
- Texto: "Veo que tienes este problema..."
- Video: Tutorial paso a paso
- Documento: Manual de usuario
- Texto: "¿Se resolvió tu problema?"
```

### 3. Onboarding
```
Plantilla: "Bienvenida_Cliente_Nuevo"
- Texto: Bienvenida personalizada
- Imagen: Banner de bienvenida
- Documento: Guía de inicio rápido
- Documento: Contrato o términos
- Texto: Siguiente paso
```

### 4. Marketing
```
Plantilla: "Promoción_Black_Friday"
- Imagen: Banner de promoción
- Texto: Detalles de la oferta
- Documento: Catálogo PDF
- Texto: CTA con urgencia
```

---

## 📊 Estructura de Datos

### Plantilla JSON

```json
{
  "id": 1,
  "name": "Mi_Plantilla",
  "description": "Descripción de la plantilla",
  "category": "ventas",
  "trigger_keywords": ["keyword1", "keyword2"],
  "is_active": true,
  "messages": [
    {
      "order": 0,
      "type": "text",
      "content": "Hola {nombre}!",
      "delay_seconds": 0
    },
    {
      "order": 1,
      "type": "image",
      "content": "Imagen de producto",
      "file_url": "/uploads/templates/imagen.jpg",
      "delay_seconds": 2
    },
    {
      "order": 2,
      "type": "document",
      "content": "Catálogo PDF",
      "file_url": "/uploads/templates/catalogo.pdf",
      "delay_seconds": 3
    }
  ],
  "created_at": "2026-01-12T10:00:00Z",
  "updated_at": null
}
```

---

## 🔧 Configuración Avanzada

### Variables Personalizadas

Puedes usar cualquier variable en los textos:

```python
variables = {
    "nombre": "Juan",
    "producto": "Curso de IA",
    "precio": "$299",
    "descuento": "20%",
    "fecha_limite": "31 de enero"
}
```

Texto: "Hola {nombre}, el {producto} está en {descuento} de descuento hasta el {fecha_limite}!"

### Delays Estratégicos

```python
messages = [
    {"order": 0, "type": "text", "content": "Pregunta", "delay_seconds": 0},
    {"order": 1, "type": "text", "content": "Pensando...", "delay_seconds": 2},
    {"order": 2, "type": "image", "content": "Respuesta visual", "delay_seconds": 3},
    {"order": 3, "type": "text", "content": "Explicación", "delay_seconds": 2}
]
```

---

## ✅ Checklist de Implementación

- [x] Modelo de base de datos creado
- [x] Schemas de validación implementados
- [x] API REST completa (CRUD)
- [x] Servicio de Chatwoot extendido (envío de archivos)
- [x] Template Manager con lógica de negocio
- [x] Integración con IntelligentAgent (bot)
- [x] Interfaz React completa y funcional
- [x] Sistema de upload de archivos
- [x] Activación automática por keywords
- [x] Soporte para variables dinámicas
- [x] Sistema de delays configurables
- [x] Categorización de plantillas
- [x] Filtros y búsqueda en UI
- [x] Migración de base de datos
- [x] Documentación completa
- [x] Script de ejemplo funcional
- [x] README actualizado

---

## 🎓 Próximos Pasos Sugeridos

### Mejoras Opcionales:

1. **Analytics de Plantillas**
   - Tracking de cuántas veces se envía cada plantilla
   - Tasa de respuesta después de enviar plantilla
   - Plantillas más efectivas

2. **Plantillas Condicionales**
   - Enviar diferentes mensajes según perfil del usuario
   - A/B testing de plantillas

3. **Plantillas Programadas**
   - Envío automático en horarios específicos
   - Seguimientos automáticos

4. **Editor Visual Avanzado**
   - Drag & drop más sofisticado
   - Preview en tiempo real
   - Plantillas prediseñadas

5. **Integración con WhatsApp Business**
   - Usar plantillas aprobadas de WhatsApp
   - Envío masivo

---

## 🐛 Troubleshooting

### Problema: "Template not found"
**Solución**: Verifica que la plantilla esté activa (`is_active = true`)

### Problema: Las keywords no activan la plantilla
**Solución**: 
- Verifica que las keywords estén en minúsculas
- Comprueba que no haya espacios extra
- Asegúrate de que la plantilla esté activa

### Problema: Los archivos no se envían
**Solución**:
- Verifica que el archivo existe en la ruta especificada
- Comprueba permisos de lectura
- Asegúrate de que el archivo no supere 10MB

### Problema: Las variables no se reemplazan
**Solución**:
- Usa la sintaxis correcta: `{variable}` (con llaves)
- Envía el diccionario `variables` en la petición
- Solo funciona en mensajes de tipo "text"

---

## 📞 Soporte

Si tienes dudas o problemas:
1. Revisa la [Guía Completa](./GUIA_PLANTILLAS_MENSAJES.md)
2. Ejecuta el script de ejemplo: `python ejemplo_plantillas.py`
3. Verifica logs del backend para errores

---

## 🎉 ¡Listo para Usar!

El módulo está completamente funcional y listo para producción. 

**¿Qué puedes hacer ahora?**
1. ✅ Crear tus primeras plantillas desde la UI
2. ✅ Configurar keywords para activación automática
3. ✅ Subir imágenes y PDFs para tus mensajes
4. ✅ Probar el envío automático en el chat
5. ✅ Integrar con tus flujos de negocio

**¡Empieza a crear experiencias increíbles para tus usuarios! 🚀**
