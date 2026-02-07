"""
Specialized Agents for different intents
Each agent has specific knowledge and capabilities
"""
from typing import Dict, List
from openai import AsyncOpenAI
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class BaseAgent:
    """Base class for specialized agents"""
    
    def __init__(self, name: str, role: str, instructions: str):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def respond(
        self,
        message: str,
        context: Dict = None,
        knowledge: List[str] = None
    ) -> str:
        """Generate response using agent's specialization"""
        
        # Build knowledge context
        knowledge_context = ""
        if knowledge:
            knowledge_context = "\n\nKnowledge Base:\n" + "\n".join([
                f"- {k}" for k in knowledge[:5]  # Top 5 relevant items
            ])
        
        # Build conversation context
        conversation_context = ""
        if context and context.get("history"):
            recent = context["history"][-3:]
            conversation_context = "\n".join([
                f"{'User' if msg.get('role') == 'user' else 'Assistant'}: {msg.get('content', '')}"
                for msg in recent
            ])
        
        # Obtener configuración de longitud de respuestas
        from app.models.settings import Settings
        response_style_setting = self.db.query(Settings).filter_by(key="response_style").first()
        response_style = response_style_setting.value if response_style_setting else "concisa"
        
        # Configurar instrucciones de longitud según el estilo
        style_instructions = {
            "concisa": "IMPORTANTE: Sé MUY BREVE y DIRECTO. Máximo 2-3 oraciones. Ve al grano.",
            "normal": "Sé claro y conciso. Respuestas de longitud media.",
            "detallada": "Proporciona respuestas completas y detalladas cuando sea necesario."
        }
        
        length_instruction = style_instructions.get(response_style, style_instructions["concisa"])
        
        system_prompt = f"""{self.instructions}

You are {self.name}, specialized in {self.role}.

Company: IA Club - Club de inteligencias artificiales que vende paquetes de IA
Product: MEGAPACK - Más de 40 IAs premium (ChatGPT Plus, Claude, Sora 2, Veo 3.1, Midjourney, etc.)
{knowledge_context}

Previous conversation:
{conversation_context if conversation_context else 'Starting new conversation'}

{length_instruction}

Respond naturally, helpfully, and stay within your specialization. If the question is outside your area, politely redirect to appropriate support."""

        # Obtener max_tokens según configuración
        max_tokens_setting = self.db.query(Settings).filter_by(key="max_response_tokens").first()
        max_tokens = int(max_tokens_setting.value) if max_tokens_setting else 150
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Agent {self.name} error: {e}")
            return "Lo siento, tuve un problema al procesar tu solicitud. ¿Puedes reformular tu pregunta?"


class SalesAgent(BaseAgent):
    """Agent specialized in sales, products, pricing"""
    
    def __init__(self):
        super().__init__(
            name="Sales Agent",
            role="sales and product inquiries",
            instructions="""You are a sales specialist for IA Club. 
            
Your expertise:
- MEGAPACK: 40+ premium IAs in one package
- Pricing and plans (1, 2, 3 months)
- VIP services (VIP 1, VIP 2, VIP 3)
- Featured AIs: ChatGPT Plus, Claude, Sora 2, Veo 3.1 Ultra, Midjourney
- Personal accounts, unlimited usage

Always be friendly, professional, and help customers find the best solution for their needs.
Provide clear pricing when available, suggest options, and guide toward purchase."""
        )


class DesignAgent(BaseAgent):
    """Agent specialized in design and customization"""
    
    def __init__(self):
        super().__init__(
            name="Design Agent",
            role="creative AI assistance",
            instructions="""You are a creative AI specialist for IA Club.

Your expertise:
- Video generation AIs: Sora 2, Veo 3.1 Ultra, Kling AI
- Image generation AIs: Midjourney, DALL-E
- Video and audio editors: CapCut PRO, Runway, Higgsfield
- Creative project assistance
- AI recommendations based on customer needs

Help customers leverage the creative AIs in the MEGAPACK. Be enthusiastic and explain each AI's capabilities clearly."""
        )


class OrderTrackingAgent(BaseAgent):
    """Agent specialized in order tracking and status"""
    
    def __init__(self):
        super().__init__(
            name="Order Tracking Agent",
            role="order status and delivery tracking",
            instructions="""You are an order management specialist for IA Club.

Your expertise:
- Login/access delivery process for MEGAPACK
- Delivery times (fast, usually same day)
- Personal account activation
- Order tracking
- Payment confirmation

Be reassuring, provide clear timelines, and keep customers informed about their order progress."""
        )


class SupportAgent(BaseAgent):
    """Agent specialized in support and problem resolution"""
    
    def __init__(self):
        super().__init__(
            name="Support Agent",
            role="technical support and issue resolution",
            instructions="""You are a customer support specialist for IA Club.

Your expertise:
- Technical issues with AI access
- Account functionality questions
- Login or credential problems
- AI feature questions
- Complaint handling and problem solving

Be empathetic, solution-oriented, and professional. Always try to resolve issues or escalate appropriately."""
        )


class GeneralAgent(BaseAgent):
    """General purpose agent for misc queries"""
    
    def __init__(self):
        super().__init__(
            name="General Agent",
            role="general assistance",
            instructions="""You are a general assistant for IA Club.

Your role:
- Answer general questions about the company
- Provide basic information
- Route complex queries to specialists
- Handle greetings and small talk

Be friendly, helpful, and guide users to the right specialist when needed."""
        )


# Agent factory
AGENT_MAP = {
    "sales": SalesAgent,
    "design": DesignAgent,
    "order_tracking": OrderTrackingAgent,
    "support": SupportAgent,
    "general": GeneralAgent
}


def get_agent(intent: str) -> BaseAgent:
    """Get appropriate agent for intent"""
    agent_class = AGENT_MAP.get(intent, GeneralAgent)
    return agent_class()
