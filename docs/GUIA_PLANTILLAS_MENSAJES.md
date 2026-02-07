# 📨 Sistema de Plantillas de Mensajes Predeterminadas

## 📋 Descripción General

El módulo de **Plantillas de Mensajes** te permite crear y configurar secuencias de mensajes predeterminadas que se envían en un orden específico y controlado por ti. El bot enviará **exactamente** lo que configures, sin modificar el orden ni el contenido.

### ✨ Características Principales

- 🎯 **Control Total**: Tú decides qué se envía y en qué orden
- 📝 **Múltiples Tipos**: Texto, imágenes, PDFs, audio, video
- ⏱️ **Delays Configurables**: Añade pausas entre mensajes (0-60 segundos)
- 🔤 **Variables Dinámicas**: Usa `{variable}` para personalizar
- 🎨 **Categorización**: Organiza por categorías (bienvenida, productos, soporte, etc.)
- 🔑 **Palabras Clave**: Activación automática por keywords
- ✅ **Estado Activo/Inactivo**: Controla qué plantillas están disponibles

---

## 🏗️ Arquitectura del Sistema

### Backend (Python/FastAPI)

```
backend/app/
├── models/message_template.py         # Modelo de base de datos
├── schemas/message_template.py        # Validación Pydantic
├── api/message_templates.py           # Endpoints REST API
├── bot/template_manager.py            # Lógica de negocio
└── services/chatwoot_service.py       # Envío a Chatwoot (extendido)
```

### Frontend (React)

```
frontend/src/pages/MessageTemplates/
└── MessageTemplates.jsx               # Interfaz de gestión completa
```

### Base de Datos

```sql
message_templates
├── id (int, PK)
├── name (string, unique)              # Nombre de la plantilla
├── description (text)                 # Descripción
├── messages (json)                    # Array de mensajes ordenados
├── category (string)                  # Categoría
├── trigger_keywords (json)            # Array de palabras clave
├── is_active (boolean)                # Estado activo/inactivo
├── created_at (datetime)
└── updated_at (datetime)
```

---

## 🚀 Cómo Usar el Sistema

### 1️⃣ Crear una Plantilla

#### Desde la Interfaz Web

1. Ve a **"Plantillas de Mensajes"** en el menú lateral
2. Haz clic en **"Nueva Plantilla"**
3. Completa el formulario:
   - **Nombre**: Identificador único (ej: "Bienvenida_Nuevos_Clientes")
   - **Descripción**: Para qué sirve esta plantilla
   - **Categoría**: Organización (ej: "bienvenida", "productos", "soporte")
   - **Palabras Clave** (opcional): Para activación automática

4. **Configura los Mensajes**:
   - Haz clic en **"Añadir Mensaje"** para cada mensaje
   - Para cada mensaje configura:
     - **Orden**: Se asigna automáticamente
     - **Tipo**: Texto, Imagen, Documento, Audio, Video
     - **Contenido**: 
       - Para texto: Escribe el mensaje (usa `{variable}` para personalizar)
       - Para archivos: Sube el archivo o indica la ruta
     - **Delay**: Segundos antes de enviar (0-60)

5. Guarda la plantilla

#### Ejemplo de Configuración

**Plantilla: "Información_Curso_IA"**

```
Mensaje #1 (Texto, delay: 0s):
"¡Hola {customer_name}! 👋 Te envío la información del Curso de IA que solicitaste:"

Mensaje #2 (Imagen, delay: 2s):
Archivo: curso_ia_preview.jpg
Caption: "Aquí tienes una vista previa del contenido"

Mensaje #3 (Documento, delay: 3s):
Archivo: programa_curso_ia.pdf
Caption: "Programa completo del curso"

Mensaje #4 (Texto, delay: 5s):
"¿Te gustaría que te cuente más sobre algún módulo en particular? 🤔"
```

### 2️⃣ Enviar una Plantilla Manualmente

#### Desde la API

```bash
POST http://localhost:8000/templates/send
Content-Type: application/json

{
  "template_id": 1,
  "conversation_id": 12345,
  "variables": {
    "customer_name": "Juan",
    "curso": "IA Avanzada"
  }
}
```

#### Desde Python (Bot)

```python
from app.bot.template_manager import TemplateManager

# Enviar por nombre
result = await template_manager.send_template_by_name(
    template_name="Información_Curso_IA",
    conversation_id=12345,
    variables={"customer_name": "Juan"}
)

# Enviar por ID
result = await template_manager.send_template_by_id(
    template_id=1,
    conversation_id=12345,
    variables={"customer_name": "Juan"}
)
```

### 3️⃣ Activación Automática por Palabras Clave

Si configuras **palabras clave** en una plantilla, el bot la enviará automáticamente cuando detecte esas palabras en un mensaje del usuario.

**Ejemplo:**

Plantilla: "Info_Precios"  
Palabras clave: `["precios", "costo", "cuanto cuesta", "precio"]`

Usuario escribe: "Hola, ¿cuánto cuesta el curso?"  
Bot: ✅ Detecta "cuanto cuesta" → Envía automáticamente la plantilla "Info_Precios"

---

## 📡 API Endpoints

### Listar Plantillas
```http
GET /templates?category=bienvenida&is_active=true&skip=0&limit=100
```

### Obtener Plantilla por ID
```http
GET /templates/{template_id}
```

### Crear Plantilla
```http
POST /templates
Content-Type: application/json

{
  "name": "Mi_Plantilla",
  "description": "Descripción",
  "messages": [
    {
      "order": 0,
      "type": "text",
      "content": "Hola {name}!",
      "delay_seconds": 0
    },
    {
      "order": 1,
      "type": "image",
      "content": "Imagen de producto",
      "file_url": "/uploads/templates/producto.jpg",
      "delay_seconds": 2
    }
  ],
  "category": "ventas",
  "trigger_keywords": ["producto", "precio"],
  "is_active": true
}
```

### Actualizar Plantilla
```http
PUT /templates/{template_id}
Content-Type: application/json

{
  "name": "Nuevo_Nombre",
  "is_active": false
}
```

### Eliminar Plantilla
```http
DELETE /templates/{template_id}
```

### Enviar Plantilla
```http
POST /templates/send
Content-Type: application/json

{
  "template_id": 1,
  "conversation_id": 12345,
  "variables": {
    "customer_name": "Juan"
  }
}
```

### Subir Archivo para Plantilla
```http
POST /templates/upload-file
Content-Type: multipart/form-data

file: [archivo]
category: "productos"
```

### Listar Categorías
```http
GET /templates/categories/list
```

---

## 💡 Casos de Uso

### 1. Secuencia de Bienvenida
```
1. Texto: "¡Bienvenido a IA Club! 🎉"
2. Imagen: Logo/Banner
3. Texto: "Te cuento qué podemos hacer por ti..."
4. Documento: Catálogo de servicios PDF
```

### 2. Información de Producto
```
1. Texto: "Te envío info del {producto_nombre}"
2. Imagen: Foto del producto
3. Documento: Ficha técnica PDF
4. Texto: "¿Tienes alguna pregunta?"
```

### 3. Respuesta a Objeciones
```
1. Texto: "Entiendo tu preocupación sobre {objecion}..."
2. Video: Testimonio de cliente
3. Documento: Casos de éxito
4. Texto: "¿Te gustaría agendar una llamada?"
```

### 4. Onboarding de Cliente Nuevo
```
1. Texto: "¡Hola {nombre}! Bienvenido"
2. Texto: "Paso 1: Accede a la plataforma"
3. Imagen: Captura de pantalla
4. Documento: Guía rápida PDF
5. Texto: "¿Todo claro hasta aquí?"
```

---

## ⚙️ Configuración de Variables

Las variables se reemplazan en **mensajes de tipo texto** usando la sintaxis `{variable}`.

### Variables Comunes:
- `{customer_name}` - Nombre del cliente
- `{producto}` - Nombre del producto
- `{precio}` - Precio
- `{fecha}` - Fecha
- `{link}` - Enlaces personalizados

### Ejemplo:
```json
{
  "messages": [
    {
      "type": "text",
      "content": "Hola {customer_name}, el precio de {producto} es {precio}"
    }
  ]
}
```

Con variables:
```json
{
  "variables": {
    "customer_name": "María",
    "producto": "Curso de IA",
    "precio": "$299"
  }
}
```

Resultado: "Hola María, el precio de Curso de IA es $299"

---

## 🔧 Integración con el Bot

El sistema está integrado en el flujo principal del bot:

```python
# En intelligent_agent.py

# 1. Verificar plantillas automáticas (por keywords)
template_result = await self.template_manager.auto_send_template(
    message=message,
    conversation_id=conversation_id
)

if template_result and template_result.get("success"):
    return {
        "response": "He enviado la información que solicitaste",
        "template_sent": template_result
    }

# 2. Si no hay plantilla, continuar con flujo normal del bot
```

---

## 📝 Migración de Base de Datos

Para crear la tabla en la base de datos:

```bash
# Aplicar migración
cd backend
alembic upgrade head
```

O ejecutar manualmente:
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

CREATE INDEX idx_templates_name ON message_templates(name);
CREATE INDEX idx_templates_category ON message_templates(category);
```

---

## 🎯 Mejores Prácticas

### ✅ Hacer:
- Usar nombres descriptivos para las plantillas
- Configurar delays realistas (2-5 segundos)
- Probar las plantillas antes de activarlas
- Usar categorías para organizar
- Mantener mensajes concisos
- Añadir palabras clave relevantes

### ❌ Evitar:
- Nombres genéricos ("plantilla1", "test")
- Delays muy largos (>10 segundos)
- Demasiados mensajes en una secuencia (>5)
- Archivos muy pesados
- Duplicar palabras clave entre plantillas

---

## 🐛 Troubleshooting

### La plantilla no se envía automáticamente
- ✅ Verifica que `is_active = true`
- ✅ Revisa que las palabras clave estén configuradas
- ✅ Comprueba que las keywords coincidan con el mensaje

### Los archivos no se cargan
- ✅ Verifica que el archivo existe en la ruta indicada
- ✅ Comprueba permisos de lectura
- ✅ Revisa el tamaño del archivo (<10MB)

### Las variables no se reemplazan
- ✅ Usa la sintaxis correcta: `{variable}`
- ✅ Verifica que envías el dict `variables` en la petición
- ✅ Solo funciona en mensajes de tipo "text"

---

## 📚 Ejemplos Completos

### Ejemplo 1: Plantilla de Bienvenida Completa

```json
{
  "name": "Bienvenida_IA_Club",
  "description": "Secuencia de bienvenida para nuevos contactos",
  "category": "bienvenida",
  "trigger_keywords": ["hola", "hola!", "buenos días", "buenas tardes"],
  "is_active": true,
  "messages": [
    {
      "order": 0,
      "type": "text",
      "content": "¡Hola {customer_name}! 👋 Bienvenido a IA Club, tu comunidad de Inteligencia Artificial en español.",
      "delay_seconds": 0
    },
    {
      "order": 1,
      "type": "image",
      "content": "Nuestro logo",
      "file_url": "/uploads/templates/bienvenida/logo_iaclub.jpg",
      "delay_seconds": 2
    },
    {
      "order": 2,
      "type": "text",
      "content": "Aquí encontrarás:\n✅ Cursos de IA\n✅ Comunidad activa\n✅ Recursos exclusivos\n✅ Soporte personalizado",
      "delay_seconds": 3
    },
    {
      "order": 3,
      "type": "document",
      "content": "Catálogo de servicios",
      "file_url": "/uploads/templates/bienvenida/catalogo.pdf",
      "delay_seconds": 2
    },
    {
      "order": 4,
      "type": "text",
      "content": "¿En qué puedo ayudarte hoy? 🤔",
      "delay_seconds": 3
    }
  ]
}
```

---

## 🎓 Conclusión

Este módulo te da **control total** sobre las secuencias de mensajes del bot. Es perfecto para:
- Procesos de onboarding
- Envío de información estructurada
- Respuestas predefinidas a consultas frecuentes
- Flujos de ventas automatizados
- Soporte técnico guiado

¡Experimenta y crea las mejores experiencias para tus usuarios! 🚀
