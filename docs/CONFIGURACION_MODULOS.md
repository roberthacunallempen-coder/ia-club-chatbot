# 🎯 GUÍA DE CONFIGURACIÓN - MÓDULOS DEL BOT

## 📚 MÓDULOS CREADOS (TODOS EDITABLES)

### 1. **response_templates.py** - Templates de Respuestas
**Ubicación:** `backend/app/bot/response_templates.py`

**Qué puedes editar:**
- ✅ CTAs (Call to Actions) para cada tipo de agente
- ✅ Mensajes de social proof
- ✅ Mensajes de urgencia
- ✅ Variaciones de saludos
- ✅ Introducciones de precios
- ✅ Formato de precios MEGAPACK y VIP

**Ejemplo de edición:**
```python
# Agregar nuevo CTA
CTAS_VENTAS.append("¿Quieres aprovechar esta oferta exclusiva?")

# Cambiar precios
PRECIOS_MEGAPACK = """
**PLANES MEGAPACK** 💰
1. **1 mes**: 💰 **35 soles** (nuevo precio)
...
"""
```

---

### 2. **customer_profiler.py** - Perfiles de Cliente
**Ubicación:** `backend/app/bot/customer_profiler.py`

**Qué puedes editar:**
- ✅ Palabras clave por perfil (académico, creativo, desarrollador, empresario)
- ✅ IAs recomendadas por perfil
- ✅ Pitch personalizado por perfil
- ✅ Beneficios destacados

**Ejemplo de edición:**
```python
# Agregar nuevo perfil
KEYWORDS["influencer"] = [
    "redes sociales", "followers", "contenido viral", "engagement"
]

IAS_POR_PERFIL["influencer"] = {
    "principales": ["Sora 2", "CapCut PRO", "Midjourney"],
    "destacar": "🌟 **Para influencers**: Crea contenido viral...",
    "beneficios": [...]
}
```

---

### 3. **objection_handler.py** - Manejo de Objeciones
**Ubicación:** `backend/app/bot/objection_handler.py`

**Qué puedes editar:**
- ✅ Tipos de objeciones y palabras clave
- ✅ Múltiples respuestas por objeción (usa variaciones aleatorias)
- ✅ Agregar nuevas objeciones en runtime

**Ejemplo de edición:**
```python
# Agregar nueva objeción
OBJECTIONS["no_tiempo"] = {
    "keywords": ["no tengo tiempo", "muy ocupado", "sin tiempo"],
    "respuestas": [
        "¡Perfecto! Las IAs te ahorran tiempo...",
        "Justamente por eso necesitas IA..."
    ]
}

# O en runtime:
objection_handler.add_custom_objection(
    "no_tiempo",
    ["no tengo tiempo", "ocupado"],
    ["Respuesta 1", "Respuesta 2"]
)
```

---

### 4. **customer_context.py** - Contexto del Cliente
**Ubicación:** `backend/app/bot/customer_context.py`

**Qué rastrea automáticamente:**
- ✅ Nombre del cliente
- ✅ Email y teléfono
- ✅ Presupuesto mencionado
- ✅ Intereses detectados
- ✅ Objeciones mencionadas
- ✅ Productos de interés
- ✅ Nivel de engagement (low, medium, high)

**Funciones útiles:**
```python
# En intelligent_agent.py
customer_ctx.should_push_for_sale()  # True si debe presionar para venta
customer_ctx.should_offer_discount()  # True si debe ofrecer descuento
customer_ctx.get_summary()  # Resumen del cliente
```

---

## 🔧 CÓMO EDITAR CADA MÓDULO

### Opción 1: Editar directamente los archivos .py
1. Abre el archivo correspondiente en VS Code
2. Modifica las listas, diccionarios o mensajes
3. Guarda el archivo
4. El bot se recarga automáticamente (modo --reload)

### Opción 2: Editar desde Python (runtime)
```python
from app.bot.response_templates import templates
from app.bot.objection_handler import objection_handler

# Agregar nuevo CTA
templates.CTAS_VENTAS.append("¿Listo para comenzar?")

# Agregar nueva objeción
objection_handler.add_custom_objection(...)
```

---

## 🎨 EJEMPLOS DE PERSONALIZACIÓN

### Cambiar el tono del bot (más formal)
**Archivo:** `response_templates.py`
```python
SALUDOS_INICIALES = [
    "Buenas tardes, soy su asistente de IA Club",
    "Bienvenido a IA Club, ¿en qué puedo ayudarle?",
]

CTAS_VENTAS = [
    "¿Le gustaría proceder con la compra?",
    "¿Podría proporcionarme su información de contacto?",
]
```

### Agregar descuentos temporales
**Archivo:** `response_templates.py`
```python
URGENCIA = [
    "🔥 BLACK FRIDAY: 20% descuento - Solo hoy",
    "⚡ FLASH SALE: 2x1 en plan de 3 meses",
]
```

### Personalizar por industria
**Archivo:** `customer_profiler.py`
```python
# Agregar perfil "abogado"
KEYWORDS["abogado"] = [
    "legal", "abogado", "jurídico", "ley", "demanda"
]

IAS_POR_PERFIL["abogado"] = {
    "principales": ["ChatGPT Plus", "Claude", "Perplexity"],
    "destacar": "⚖️ **Para abogados**: Análisis legal, redacción de documentos...",
}
```

---

## 📊 MONITOREO Y MÉTRICAS

El sistema ahora retorna información extendida:

```json
{
    "response": "...",
    "intent": "sales",
    "agent_used": "Sales Agent",
    "confidence": 0.95,
    "customer_profile": "academico",
    "customer_context": "Cliente: Juan | Perfil: academico | Engagement: high",
    "engagement_level": "high"
}
```

Puedes usar esto para:
- Identificar clientes hot (engagement: high)
- Personalizar follow-ups
- Analizar qué perfiles convierten más

---

## 🚀 MEJORAS IMPLEMENTADAS

### ✅ Variaciones de Respuestas
- Cada respuesta usa variaciones aleatorias
- Evita que el bot suene repetitivo
- Saludos, CTAs y mensajes de precio varían

### ✅ CTAs Siempre Presentes
- Todas las respuestas de ventas terminan con pregunta de acción
- CTAs específicos por tipo de agente
- Guían al cliente hacia la compra

### ✅ Detección de Objeciones
- Detecta y responde objeciones antes que el agente principal
- Múltiples respuestas por objeción
- Registra objeciones en el contexto

### ✅ Perfilado de Clientes
- Detecta automáticamente: académico, creativo, desarrollador, empresario
- Personaliza respuestas según perfil
- Recomienda IAs específicas

### ✅ Contexto Persistente
- Recuerda nombre, intereses, presupuesto
- Detecta nivel de engagement
- Decide cuándo presionar para venta

### ✅ Social Proof Automático
- Agrega testimonios y pruebas sociales
- Link al grupo de WhatsApp
- Mensajes de urgencia cuando aplica

---

## 🎯 PRÓXIMOS PASOS RECOMENDADOS

1. **Probar el bot** en http://localhost:5173/test-bot
2. **Ver los logs** del backend para ver perfiles y objeciones detectadas
3. **Personalizar mensajes** según tu estilo
4. **Agregar más objeciones** según las que encuentres
5. **Ajustar CTAs** para mejorar conversión

---

## 💡 TIPS PRO

### Tip 1: A/B Testing
Agrega 2-3 variaciones de cada mensaje y analiza cuál convierte mejor

### Tip 2: Actualización sin reiniciar
Los cambios en listas y diccionarios se aplican en caliente (no necesitas reiniciar)

### Tip 3: Logs detallados
Revisa la terminal del backend para ver:
- Perfiles detectados
- Objeciones manejadas
- Nivel de engagement
- Contexto del cliente

### Tip 4: Personalización extrema
Usa el `customer_context` para crear respuestas ultra-personalizadas:
```python
if customer_ctx.context["name"]:
    response = f"¡Perfecto, {customer_ctx.context['name']}! ..."
```

---

## 📞 SOPORTE

Si necesitas ayuda para configurar algo específico:
1. Revisa los archivos .py - están bien comentados
2. Prueba en test-bot y revisa logs
3. Modifica incrementalmente y prueba

**¡Tu bot ahora es 10x más profesional y efectivo!** 🚀
