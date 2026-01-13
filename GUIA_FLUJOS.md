# 🔄 Sistema de Flujos Conversacionales

## 📖 Descripción

El sistema de flujos permite crear conversaciones estructuradas que guían a los clientes paso a paso hacia un objetivo específico. Cada flujo tiene múltiples pasos con validación, opciones de respuesta y ramificaciones condicionales.

---

## 🎯 Flujos Incluidos

### 1. **Onboarding** (`onboarding`)
Flujo de bienvenida para nuevos usuarios que guía desde el primer contacto hasta la selección de plan.

**Pasos:**
1. **Bienvenida** → Saludo y pregunta inicial
2. **Selección de Camino** → Usuario elige entre ver opciones, conocer más, o hablar con asesor
3. **Detección de Perfil** → Identifica si es académico, creativo, desarrollador o empresario
4. **Presentación de Planes** → Muestra Básico, Premium o MegaPack según perfil
5. **Confirmación de Plan** → Valida la selección
6. **Captura de Nombre** → Solicita nombre del cliente
7. **Captura de Email** → Solicita email (valida formato)
8. **Captura de WhatsApp** → Solicita número de WhatsApp
9. **Métodos de Pago** → Informa sobre PayPal, transferencia, cripto
10. **Despedida** → Confirmación y próximos pasos

**Cuándo Usar:**
- Cliente nuevo que nunca ha interactuado
- Usuario que pregunta "¿qué es IA Club?"
- Iniciar manualmente desde UI de flujos

---

### 2. **Recuperación** (`recovery`)
Flujo para reactivar clientes que abandonaron el proceso de compra.

**Pasos:**
1. **Inicio** → Detecta abandono y pregunta motivo
2. **Manejo de Objeciones** → Responde según objeción (precio, tiempo, duda)
3. **Oferta Especial** → Presenta descuento temporal
4. **Confirmación de Interés** → Valida si desea continuar
5. **Captura de Contacto** → Solicita email/WhatsApp si no lo tiene
6. **Próximos Pasos** → Envía detalles de pago y cierre

**Cuándo Usar:**
- Cliente que dejó conversación sin comprar
- Usuario que dijo "lo pensaré" hace días
- Manualmente al detectar carritos abandonados

---

## 🛠️ Arquitectura Técnica

### Backend (`backend/app/bot/conversation_flows.py`)

**Clases Principales:**

```python
class FlowState(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class FlowStep:
    """Un paso individual del flujo"""
    step_id: str                    # ID único del paso
    message: str                     # Mensaje que muestra
    next_steps: dict[str, str]       # Opciones → siguiente paso
    validation: Optional[Callable]   # Función de validación
    
class ConversationFlow:
    """Flujo completo de conversación"""
    flow_id: str
    name: str
    description: str
    entry_point: str                # Primer paso
    steps: dict[str, FlowStep]      # Todos los pasos
    state: FlowState
    context: dict                   # Datos capturados
    
    def start() -> str              # Inicia el flujo
    def process_input(user_input: str) -> str  # Procesa respuesta
    def get_progress() -> dict      # Retorna progreso actual
```

**Factory de Flujos:**

```python
class IAClubFlows:
    @staticmethod
    def create_onboarding_flow() -> ConversationFlow
    
    @staticmethod
    def create_recovery_flow() -> ConversationFlow
```

**Gestor Global:**

```python
class FlowManager:
    active_flows: dict[int, ConversationFlow]  # conversation_id → flow
    
    def start_flow(conversation_id: int, flow_id: str) -> dict
    def process_message(conversation_id: int, message: str) -> dict
    def has_active_flow(conversation_id: int) -> bool
    def abandon_flow(conversation_id: int) -> None
```

---

### API Endpoints (`backend/app/api/flows.py`)

```python
POST /api/flows/start
Body: {
    "flow_id": "onboarding",
    "conversation_id": 1
}
Response: {
    "message": "¡Hola! 👋 ...",
    "flow_id": "onboarding",
    "flow_started": true
}

POST /api/flows/message
Body: {
    "conversation_id": 1,
    "message": "Soy estudiante"
}
Response: {
    "response": "¡Perfecto para académicos! ...",
    "flow_completed": false
}

GET /api/flows/active/{conversation_id}
Response: {
    "flow_id": "onboarding",
    "current_step": "plan_selection",
    "progress": {"nombre": "Juan", "perfil": "academico"}
}

DELETE /api/flows/abandon/{conversation_id}
Response: {"message": "Flujo abandonado"}

GET /api/flows/available
Response: {
    "flows": [
        {"id": "onboarding", "name": "Onboarding", "description": "..."},
        {"id": "recovery", "name": "Recuperación", "description": "..."}
    ]
}
```

---

### Frontend (`frontend/src/pages/Flows/FlowsManager.jsx`)

**Componente React:**
- Lista de flujos disponibles
- Botón para iniciar cada flujo
- Información del flujo activo
- Botón para abandonar flujo
- Guías y tips de uso

**Navegación:**
- URL: `http://localhost:5173/flows`
- Menú lateral: "Flujos" con icono GitBranch

---

## 📋 Integración con Bot

El sistema de flujos se integra en `intelligent_agent.py` con **máxima prioridad**:

```python
async def process_message(conversation_id: int, message: str) -> dict:
    # 1. VERIFICAR SI HAY FLUJO ACTIVO (PRIORIDAD #1)
    if flow_manager.has_active_flow(conversation_id):
        flow_response = flow_manager.process_message(conversation_id, message)
        return flow_response
    
    # 2. Si no hay flujo, continuar con lógica normal
    intent = classify_intent(message)
    agent = get_agent(intent)
    # ... resto del flujo normal
```

**Ventajas:**
✅ Flujos tienen control total sobre la conversación
✅ No interfieren otros agentes durante el flujo
✅ Captura datos de forma estructurada
✅ Fácil de abandonar si cliente quiere salir

---

## 🚀 Cómo Usar

### Opción 1: Inicio Automático (Recomendado)

Modifica `intelligent_agent.py` para iniciar flujo con nuevos usuarios:

```python
async def process_message(conversation_id: int, message: str) -> dict:
    # Verificar si es primera interacción
    conversation = db.query(Conversation).filter_by(id=conversation_id).first()
    
    if not conversation or conversation.message_count == 1:
        # Iniciar flujo de onboarding automáticamente
        return flow_manager.start_flow(conversation_id, "onboarding")
    
    # ... resto del código
```

### Opción 2: Inicio Manual desde UI

1. Ve a `http://localhost:5173/flows`
2. Haz clic en "Iniciar Flujo" en el flujo deseado
3. Ve a `http://localhost:5173/test-bot`
4. Interactúa con el chat (el flujo ya está activo)

### Opción 3: Inicio desde API

```bash
curl -X POST http://localhost:8000/api/flows/start \
  -H "Content-Type: application/json" \
  -d '{
    "flow_id": "onboarding",
    "conversation_id": 123
  }'
```

---

## ✏️ Personalización

### Crear un Nuevo Flujo

Edita `backend/app/bot/conversation_flows.py`:

```python
@staticmethod
def create_upsell_vip_flow() -> ConversationFlow:
    """Flujo de upsell a plan VIP"""
    
    steps = {
        "welcome": FlowStep(
            step_id="welcome",
            message="¡Hola! Veo que ya eres usuario Premium. ¿Te gustaría conocer el plan VIP? 🚀",
            next_steps={
                "si": "benefits",
                "no": "end",
                "mas_info": "benefits"
            }
        ),
        "benefits": FlowStep(
            step_id="benefits",
            message="El plan VIP incluye:\n✅ Todas las IAs ilimitadas\n✅ Acceso prioritario\n✅ 2 cuentas adicionales\n✅ Soporte 24/7\n\n¿Te interesa?",
            next_steps={
                "si": "discount",
                "no": "objection",
                "precio": "price_info"
            }
        ),
        # ... más pasos
    }
    
    return ConversationFlow(
        flow_id="upsell_vip",
        name="Upsell VIP",
        description="Convierte usuarios Premium a VIP",
        entry_point="welcome",
        steps=steps
    )
```

Luego agrégalo al FlowManager:

```python
class FlowManager:
    def __init__(self):
        self.available_flows = {
            "onboarding": IAClubFlows.create_onboarding_flow,
            "recovery": IAClubFlows.create_recovery_flow,
            "upsell_vip": IAClubFlows.create_upsell_vip_flow,  # NUEVO
        }
```

### Modificar Flujo Existente

Encuentra el método del flujo (ej: `create_onboarding_flow`) y edita:

**Cambiar mensaje de bienvenida:**
```python
"welcome": FlowStep(
    step_id="welcome",
    message="¡Tu nuevo mensaje aquí! 🎉",  # ← EDITAR AQUÍ
    next_steps={
        "ver_opciones": "path_selection",
        "conocer_mas": "learn_more"
    }
)
```

**Agregar nuevo paso:**
```python
"nuevo_paso": FlowStep(
    step_id="nuevo_paso",
    message="¿Prefieres pago mensual o anual?",
    next_steps={
        "mensual": "payment_methods",
        "anual": "annual_discount"
    }
)
```

**Agregar validación:**
```python
def validate_email(email: str) -> bool:
    import re
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

"email_capture": FlowStep(
    step_id="email_capture",
    message="Por favor, ingresa tu email:",
    next_steps={"*": "whatsapp_capture"},
    validation=validate_email  # ← VALIDACIÓN
)
```

---

## 📊 Métricas y Análisis

### Ver Progreso de Flujo Activo

```bash
GET http://localhost:8000/api/flows/active/123
```

Retorna:
```json
{
  "flow_id": "onboarding",
  "current_step": "plan_selection",
  "progress": {
    "nombre": "Juan Pérez",
    "perfil": "academico",
    "plan": "premium"
  }
}
```

### Datos Capturados

Los flujos guardan automáticamente:
- `nombre`: Nombre del cliente
- `email`: Email capturado
- `whatsapp`: Número de WhatsApp
- `perfil`: Tipo de cliente (académico, creativo, etc.)
- `plan`: Plan seleccionado (básico, premium, megapack)
- `objeciones`: Objeciones mencionadas

**Acceder a datos:**
```python
flow = flow_manager.active_flows.get(conversation_id)
nombre = flow.context.get("nombre")
email = flow.context.get("email")
plan = flow.context.get("plan")
```

---

## 🔧 Troubleshooting

### Problema: Flujo no se inicia
**Causa:** conversation_id no válido o flujo ya activo
**Solución:**
```python
# Verificar si hay flujo activo
if flow_manager.has_active_flow(conversation_id):
    flow_manager.abandon_flow(conversation_id)

# Luego iniciar nuevo flujo
flow_manager.start_flow(conversation_id, "onboarding")
```

### Problema: Usuario quiere salir del flujo
**Solución:** Detectar palabras clave en `process_input`:
```python
exit_keywords = ["salir", "cancelar", "no gracias", "adiós"]
if any(keyword in user_input.lower() for keyword in exit_keywords):
    self.state = FlowState.ABANDONED
    return "Entendido, saliendo del flujo. ¿En qué más puedo ayudarte?"
```

### Problema: Validación falla constantemente
**Causa:** Formato de validación muy estricto
**Solución:** Hacer validación más flexible:
```python
def validate_whatsapp(phone: str) -> bool:
    # Acepta múltiples formatos
    clean = re.sub(r'[^\d+]', '', phone)
    return len(clean) >= 10  # Mínimo 10 dígitos
```

---

## 💡 Mejores Prácticas

### ✅ DO's

1. **Usa validación suave:** Acepta múltiples variaciones de respuesta
2. **Captura incremental:** Guarda datos en cada paso (no esperes al final)
3. **Salidas claras:** Permite que el usuario abandone en cualquier momento
4. **Mensajes cortos:** Máximo 2-3 líneas por mensaje
5. **Opciones visibles:** Muestra las opciones disponibles al usuario

### ❌ DON'Ts

1. **No hagas flujos muy largos:** Máximo 10-12 pasos
2. **No valides todo:** Solo valida datos críticos (email, teléfono)
3. **No repitas preguntas:** Si ya tienes un dato, no lo vuelvas a pedir
4. **No ignores objeciones:** Siempre maneja "no sé", "luego", etc.
5. **No olvides contexto:** Usa datos de pasos anteriores

---

## 📈 Casos de Uso Recomendados

| Caso de Uso | Flujo Recomendado | Trigger |
|-------------|-------------------|---------|
| Nuevo usuario llega al chat | Onboarding | Automático al primer mensaje |
| Cliente abandonó hace 3 días | Recovery | Manual o trigger temporal |
| Usuario Premium >30 días | Upsell VIP | Manual o evento temporal |
| Cliente solicita cotización | Quote Builder | Keyword "cotizar" |
| Soporte técnico necesario | Support Triage | Intent = "support" |

---

## 🔐 Seguridad

- **No guardes contraseñas** en el contexto del flujo
- **Valida emails y teléfonos** antes de enviar a base de datos
- **Limpia inputs** de caracteres especiales
- **No expongas datos sensibles** en logs

---

## 🎓 Tutorial Completo

### Ejemplo: Crear flujo de cotización

```python
@staticmethod
def create_quote_flow() -> ConversationFlow:
    steps = {
        "start": FlowStep(
            step_id="start",
            message="¿Qué servicio necesitas cotizar? 1) Plan básico 2) Plan premium 3) Plan empresarial",
            next_steps={
                "1": "basic_quote",
                "basico": "basic_quote",
                "2": "premium_quote",
                "premium": "premium_quote",
                "3": "enterprise_quote",
                "empresarial": "enterprise_quote"
            }
        ),
        "basic_quote": FlowStep(
            step_id="basic_quote",
            message="Plan Básico: $19.90/mes\n✅ 5 IAs\n✅ 1000 consultas/mes\n\n¿Deseas continuar?",
            next_steps={
                "si": "capture_email",
                "no": "end"
            }
        ),
        "capture_email": FlowStep(
            step_id="capture_email",
            message="Por favor, ingresa tu email para enviarte la cotización:",
            next_steps={"*": "send_quote"},
            validation=lambda e: "@" in e and "." in e
        ),
        "send_quote": FlowStep(
            step_id="send_quote",
            message="¡Listo! Te enviaremos la cotización a tu email. 📧\n\nCódigo de descuento: FIRST10 (10% off)",
            next_steps={"*": "END"}
        )
    }
    
    return ConversationFlow(
        flow_id="quote",
        name="Cotización",
        description="Genera cotización personalizada",
        entry_point="start",
        steps=steps
    )
```

---

## 📞 Soporte

Para dudas sobre flujos:
1. Revisa `CONFIGURACION_MODULOS.md` para configuración general
2. Revisa `backend/app/bot/conversation_flows.py` para código
3. Prueba en `http://localhost:5173/test-bot`
4. Usa `http://localhost:5173/flows` para gestión visual

**Archivos clave:**
- Backend: `backend/app/bot/conversation_flows.py`
- API: `backend/app/api/flows.py`
- Frontend: `frontend/src/pages/Flows/FlowsManager.jsx`
- Integración: `backend/app/bot/intelligent_agent.py`

---

## 🚦 Estado del Sistema

✅ Flujos implementados: Onboarding, Recovery
✅ API completa y funcional
✅ UI de gestión creada
✅ Integración con bot principal
✅ Validaciones activas
✅ Captura de contexto
✅ Documentación completa

**Siguiente paso:** Reiniciar sistema y probar flujos en acción 🎉
