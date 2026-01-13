"""
Sistema de Flujos Conversacionales - MODULAR Y CONFIGURABLE
Define secuencias de conversación estructuradas para guiar al cliente
"""
from typing import Dict, List, Optional, Callable
from enum import Enum


class FlowState(Enum):
    """Estados posibles en un flujo"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class FlowStep:
    """Un paso individual en un flujo"""
    
    def __init__(
        self,
        step_id: str,
        message: str,
        next_steps: Dict[str, str] = None,  # {opcion: next_step_id}
        validation: Callable = None,
        metadata: Dict = None
    ):
        self.step_id = step_id
        self.message = message
        self.next_steps = next_steps or {}
        self.validation = validation
        self.metadata = metadata or {}
    
    def get_message(self, context: Dict = None) -> str:
        """Genera el mensaje del paso, puede usar contexto"""
        if context:
            try:
                return self.message.format(**context)
            except:
                return self.message
        return self.message
    
    def validate_input(self, user_input: str) -> bool:
        """Valida el input del usuario para este paso"""
        if self.validation:
            return self.validation(user_input)
        return True
    
    def get_next_step(self, user_input: str) -> Optional[str]:
        """Determina el siguiente paso basado en el input"""
        # Buscar coincidencias en next_steps
        user_lower = user_input.lower()
        for option, next_step in self.next_steps.items():
            if option.lower() in user_lower:
                return next_step
        
        # Si hay un next_step por defecto
        if "default" in self.next_steps:
            return self.next_steps["default"]
        
        return None


class ConversationFlow:
    """Define un flujo conversacional completo"""
    
    def __init__(
        self,
        flow_id: str,
        name: str,
        description: str,
        entry_point: str,
        steps: List[FlowStep]
    ):
        self.flow_id = flow_id
        self.name = name
        self.description = description
        self.entry_point = entry_point
        self.steps = {step.step_id: step for step in steps}
        
        # Estado del flujo para un usuario
        self.state = FlowState.NOT_STARTED
        self.current_step_id = entry_point
        self.context = {}
        self.history = []
    
    def start(self) -> str:
        """Inicia el flujo y retorna el primer mensaje"""
        self.state = FlowState.IN_PROGRESS
        self.current_step_id = self.entry_point
        self.history.append(self.entry_point)
        
        current_step = self.steps[self.current_step_id]
        return current_step.get_message(self.context)
    
    def process_input(self, user_input: str) -> Dict:
        """
        Procesa el input del usuario y avanza en el flujo
        
        Returns:
            {
                "message": "...",
                "completed": False,
                "current_step": "step_id",
                "options": [...],
                "requires_input": True
            }
        """
        if self.state != FlowState.IN_PROGRESS:
            return {
                "message": "El flujo no está activo.",
                "completed": True,
                "error": "Flow not in progress"
            }
        
        current_step = self.steps[self.current_step_id]
        
        # Validar input
        if not current_step.validate_input(user_input):
            return {
                "message": "❌ Respuesta no válida. Por favor, intenta de nuevo.",
                "completed": False,
                "current_step": self.current_step_id,
                "requires_input": True
            }
        
        # Guardar en contexto si es necesario
        if current_step.metadata.get("save_to_context"):
            key = current_step.metadata["save_to_context"]
            self.context[key] = user_input
        
        # Determinar siguiente paso
        next_step_id = current_step.get_next_step(user_input)
        
        if not next_step_id:
            # Fin del flujo
            self.state = FlowState.COMPLETED
            return {
                "message": "✅ ¡Flujo completado! Gracias.",
                "completed": True,
                "context": self.context
            }
        
        # Avanzar al siguiente paso
        self.current_step_id = next_step_id
        self.history.append(next_step_id)
        
        next_step = self.steps[next_step_id]
        
        return {
            "message": next_step.get_message(self.context),
            "completed": False,
            "current_step": next_step_id,
            "requires_input": not next_step.metadata.get("auto_advance", False)
        }
    
    def get_progress(self) -> Dict:
        """Retorna el progreso del flujo"""
        return {
            "flow_id": self.flow_id,
            "state": self.state.value,
            "current_step": self.current_step_id,
            "steps_completed": len(self.history),
            "total_steps": len(self.steps),
            "context": self.context
        }
    
    def abandon(self):
        """Marca el flujo como abandonado"""
        self.state = FlowState.ABANDONED


# ==========================================
# FLUJOS PREDEFINIDOS PARA IA CLUB
# ==========================================

class IAClubFlows:
    """Flujos conversacionales predefinidos para IA Club"""
    
    @staticmethod
    def create_onboarding_flow() -> ConversationFlow:
        """Flujo de bienvenida y onboarding"""
        
        steps = [
            FlowStep(
                step_id="welcome",
                message="""¡Bienvenido a IA Club! 🤖✨

Soy Tío IA, tu asistente personal. Estoy aquí para ayudarte a descubrir el poder de la inteligencia artificial.

**¿Cuál es tu principal objetivo?**

1️⃣ Crear contenido (videos, imágenes, diseño)
2️⃣ Trabajo académico (tesis, investigación)
3️⃣ Desarrollo y programación
4️⃣ Mejorar productividad empresarial

Escribe el número de tu opción (1-4) 👇""",
                next_steps={
                    "1": "creative_path",
                    "2": "academic_path",
                    "3": "developer_path",
                    "4": "business_path",
                    "crear": "creative_path",
                    "contenido": "creative_path",
                    "académico": "academic_path",
                    "tesis": "academic_path",
                    "desarrollo": "developer_path",
                    "programación": "developer_path",
                    "empresa": "business_path",
                    "productividad": "business_path"
                },
                metadata={"save_to_context": "objetivo"}
            ),
            
            FlowStep(
                step_id="creative_path",
                message="""🎨 ¡Perfecto para creativos!

El **MEGAPACK** incluye las mejores IAs para creación de contenido:

🎥 **Sora 2** - Videos con sonido
🎬 **Veo 3.1 Ultra** - Video cinematográfico
🖼️ **Midjourney** - Diseño de imágenes
✂️ **CapCut PRO** - Edición profesional

**Precio:** Solo 30 soles/mes (40+ IAs incluidas)

**¿Te interesa probarlo?**
✅ Sí, quiero el MEGAPACK
⏰ Más tarde
❓ Tengo dudas

Responde con "sí", "más tarde" o "dudas" 👇""",
                next_steps={
                    "sí": "plan_selection",
                    "si": "plan_selection",
                    "quiero": "plan_selection",
                    "interesa": "plan_selection",
                    "más tarde": "followup_reminder",
                    "luego": "followup_reminder",
                    "dudas": "objection_handler",
                    "pregunta": "objection_handler"
                }
            ),
            
            FlowStep(
                step_id="academic_path",
                message="""🎓 ¡Ideal para académicos!

El **MEGAPACK** te ayuda con:

📚 **ChatGPT Plus** - Análisis y redacción
🤖 **Claude** - Investigación profunda
🔍 **Perplexity** - Búsqueda académica
✍️ **Jasper** - Redacción profesional

**Precio:** Solo 30 soles/mes (40+ IAs incluidas)

**¿Te gustaría empezar?**
✅ Sí, quiero el MEGAPACK
⏰ Más tarde
❓ Tengo dudas""",
                next_steps={
                    "sí": "plan_selection",
                    "si": "plan_selection",
                    "quiero": "plan_selection",
                    "más tarde": "followup_reminder",
                    "dudas": "objection_handler"
                }
            ),
            
            FlowStep(
                step_id="developer_path",
                message="""💻 ¡Perfecto para developers!

El **MEGAPACK** incluye:

⚡ **ChatGPT Plus** - Code generation
🤖 **Claude** - Code review y debugging
🚀 **GitHub Copilot** - Autocompletado IA
📝 **Cursor AI** - Editor con IA

**Precio:** Solo 30 soles/mes (40+ IAs incluidas)

**¿Listo para mejorar tu workflow?**
✅ Sí, quiero el MEGAPACK
⏰ Más tarde
❓ Tengo dudas""",
                next_steps={
                    "sí": "plan_selection",
                    "si": "plan_selection",
                    "más tarde": "followup_reminder",
                    "dudas": "objection_handler"
                }
            ),
            
            FlowStep(
                step_id="business_path",
                message="""💼 ¡Ideal para negocios!

El **MEGAPACK** automatiza:

📊 **ChatGPT Plus** - Análisis de datos
📧 **Jasper** - Marketing y emails
🤖 **Claude** - Atención al cliente
⚡ **Copy.ai** - Contenido rápido

**Precio:** Solo 30 soles/mes (40+ IAs incluidas)

**¿Quieres aumentar tu productividad?**
✅ Sí, quiero el MEGAPACK
⏰ Más tarde
❓ Tengo dudas""",
                next_steps={
                    "sí": "plan_selection",
                    "más tarde": "followup_reminder",
                    "dudas": "objection_handler"
                }
            ),
            
            FlowStep(
                step_id="plan_selection",
                message="""💰 **PLANES MEGAPACK**

Elige tu plan:

1️⃣ **1 mes** - 30 soles
2️⃣ **2 meses** - 50 soles (ahorro de 10 soles)
3️⃣ **3 meses** - 70 soles ⭐ (ahorro de 20 soles)

⏰ **Promoción válida hasta fin de mes**

Todos incluyen:
✅ 40+ IAs premium
✅ Uso ilimitado
✅ Cuentas personales
✅ 3 regalos extras

**¿Cuál plan prefieres? (1, 2 o 3)** 👇""",
                next_steps={
                    "1": "collect_contact",
                    "2": "collect_contact",
                    "3": "collect_contact",
                    "un mes": "collect_contact",
                    "dos meses": "collect_contact",
                    "tres meses": "collect_contact"
                },
                metadata={"save_to_context": "plan"}
            ),
            
            FlowStep(
                step_id="collect_contact",
                message="""¡Excelente elección! 🎉

Para completar tu registro, necesito tu información de contacto.

**Por favor, compárteme tu WhatsApp o email:** 📱

(Ej: 987654321 o email@ejemplo.com)""",
                next_steps={"default": "payment_info"},
                metadata={"save_to_context": "contacto"}
            ),
            
            FlowStep(
                step_id="payment_info",
                message="""✅ ¡Perfecto, {contacto}!

**PLAN SELECCIONADO:** {plan}

**PROCESO DE PAGO:**

1️⃣ Transferencia bancaria o Yape
2️⃣ Envía tu comprobante
3️⃣ Recibes tu acceso en minutos

📱 **Únete a nuestro grupo de referencias:**
https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi

Un asesor te contactará en breve para completar tu compra. 

**¿Tienes alguna pregunta antes de proceder?** 💬""",
                next_steps={"default": "end"}
            ),
            
            FlowStep(
                step_id="followup_reminder",
                message="""⏰ ¡Sin problema!

Te entiendo perfectamente. Recuerda que:

🔥 La promoción de 30 soles termina pronto
💎 Los regalos extras son solo en promoción
📱 Puedes unirte al grupo para ver referencias:
https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi

**Cuando estés listo, escríbeme y retomamos** 😊

¿Te gustaría que te recuerde en unos días?""",
                next_steps={"default": "end"}
            ),
            
            FlowStep(
                step_id="objection_handler",
                message="""❓ **¿Qué duda tienes?**

Puedo ayudarte con:

💰 Precios y planes
🔒 Seguridad y confianza
📱 Cómo funcionan las cuentas
⚡ Qué IAs incluye exactamente
🎁 Regalos y promociones

**Escribe tu duda y te ayudo** 👇""",
                next_steps={"default": "plan_selection"}
            )
        ]
        
        return ConversationFlow(
            flow_id="onboarding",
            name="Onboarding IA Club",
            description="Flujo de bienvenida y selección de plan",
            entry_point="welcome",
            steps=steps
        )
    
    @staticmethod
    def create_recovery_flow() -> ConversationFlow:
        """Flujo de recuperación de carritos abandonados"""
        
        steps = [
            FlowStep(
                step_id="start",
                message="""👋 ¡Hola! Veo que estuviste interesado en el MEGAPACK.

¿Puedo ayudarte a resolver alguna duda para que puedas unirte al club? 🤖

**Las dudas más comunes son:**
💰 Sobre el precio
🔒 Sobre la seguridad
📱 Sobre cómo funciona

**¿Cuál es tu principal preocupación?** 👇""",
                next_steps={
                    "precio": "price_objection",
                    "caro": "price_objection",
                    "seguridad": "security_objection",
                    "confianza": "security_objection",
                    "funciona": "how_it_works",
                    "default": "general_help"
                }
            ),
            
            FlowStep(
                step_id="price_objection",
                message="""💰 **Entiendo tu preocupación por el precio.**

Déjame mostrarte el valor real:

**Si compraras las IAs por separado:**
- ChatGPT Plus: $20/mes = 75 soles
- Midjourney: $30/mes = 110 soles
- Claude Pro: $20/mes = 75 soles
**Total: 260+ soles/mes**

**Con IA Club: Solo 30 soles/mes**
✅ Ahorras más del 88%
✅ 40+ IAs en lugar de 3
✅ Incluye Sora 2 (no disponible solo)

**¿Tiene más sentido ahora?** 🤔""",
                next_steps={"default": "offer_trial"}
            ),
            
            FlowStep(
                step_id="offer_trial",
                message="""🎁 **OFERTA ESPECIAL PARA TI:**

Como vi que estabas interesado, te ofrezco:

⭐ **Plan de 1 mes por 25 soles** (5 soles de descuento)
⏰ **Válido solo por 24 horas**

Es menos que una pizza 🍕 y tienes acceso completo por 30 días.

**¿Aprovechas esta oferta?**
✅ Sí, quiero aprovechar
❌ No, gracias""",
                next_steps={
                    "sí": "collect_contact_recovery",
                    "si": "collect_contact_recovery",
                    "quiero": "collect_contact_recovery",
                    "no": "final_attempt"
                }
            ),
            
            FlowStep(
                step_id="collect_contact_recovery",
                message="""🎉 ¡Excelente decisión!

**Tu descuento:** 5 soles OFF
**Precio final:** 25 soles por 1 mes

Por favor, compárteme tu WhatsApp para procesar tu pedido especial: 📱""",
                next_steps={"default": "end"},
                metadata={"save_to_context": "contacto"}
            ),
            
            FlowStep(
                step_id="final_attempt",
                message="""😊 Lo entiendo perfectamente.

Antes de que te vayas, déjame ofrecerte algo:

📱 **Únete a nuestro grupo de referencias GRATIS:**
https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi

Ahí puedes:
✅ Ver testimonios reales
✅ Hablar con miembros activos
✅ Resolver todas tus dudas
✅ Sin compromiso

**¿Te parece?** 🤝""",
                next_steps={"default": "end"}
            )
        ]
        
        return ConversationFlow(
            flow_id="recovery",
            name="Recuperación de Abandono",
            description="Recupera clientes que abandonaron el proceso",
            entry_point="start",
            steps=steps
        )


class FlowManager:
    """Gestor de flujos activos por conversación"""
    
    def __init__(self):
        self.active_flows = {}  # conversation_id -> ConversationFlow
        
        # Registro de flujos disponibles
        self.available_flows = {
            "onboarding": IAClubFlows.create_onboarding_flow,
            "recovery": IAClubFlows.create_recovery_flow
        }
    
    def start_flow(self, conversation_id: int, flow_id: str) -> Dict:
        """Inicia un flujo para una conversación"""
        if flow_id not in self.available_flows:
            return {"error": f"Flow {flow_id} not found"}
        
        # Crear instancia del flujo
        flow = self.available_flows[flow_id]()
        self.active_flows[conversation_id] = flow
        
        # Iniciar el flujo
        message = flow.start()
        
        return {
            "message": message,
            "flow_id": flow_id,
            "flow_started": True,
            "progress": flow.get_progress()
        }
    
    def process_message(self, conversation_id: int, message: str) -> Optional[Dict]:
        """Procesa un mensaje en el contexto de un flujo activo"""
        if conversation_id not in self.active_flows:
            return None
        
        flow = self.active_flows[conversation_id]
        result = flow.process_input(message)
        
        # Si el flujo se completó o abandonó, limpiarlo
        if result.get("completed") or flow.state == FlowState.ABANDONED:
            del self.active_flows[conversation_id]
        
        return result
    
    def has_active_flow(self, conversation_id: int) -> bool:
        """Verifica si hay un flujo activo para una conversación"""
        return conversation_id in self.active_flows
    
    def get_active_flow(self, conversation_id: int) -> Optional[ConversationFlow]:
        """Obtiene el flujo activo de una conversación"""
        return self.active_flows.get(conversation_id)
    
    def abandon_flow(self, conversation_id: int):
        """Abandona el flujo activo"""
        if conversation_id in self.active_flows:
            self.active_flows[conversation_id].abandon()
            del self.active_flows[conversation_id]


# Instancia global
flow_manager = FlowManager()
