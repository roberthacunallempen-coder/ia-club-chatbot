"""
Intent Classification System
Classifies user messages to route to specialized agents
"""
from typing import Dict, List
from openai import AsyncOpenAI
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class IntentClassifier:
    """Classifies user intents for agent routing"""
    
    INTENTS = {
        "sales": "Consultas sobre ventas, productos, precios, cotizaciones",
        "design": "Ayuda con diseño, personalización, colores, estilos",
        "order_tracking": "Seguimiento de pedidos, estado de órdenes",
        "support": "Problemas técnicos, quejas, devoluciones",
        "general": "Saludos, información general, otras consultas"
    }
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def classify(
        self,
        message: str,
        conversation_history: List[Dict] = None
    ) -> Dict:
        """
        Classify user intent from message
        
        Returns:
            {
                "intent": "sales",
                "confidence": 0.95,
                "reasoning": "User asking about prices"
            }
        """
        try:
            # Build context from history
            context = ""
            if conversation_history:
                recent_messages = conversation_history[-3:]  # Last 3 messages
                context = "\n".join([
                    f"{'User' if msg.get('role') == 'user' else 'Bot'}: {msg.get('content', '')}"
                    for msg in recent_messages
                ])
            
            # Build classification prompt
            intents_list = "\n".join([
                f"- {key}: {desc}" 
                for key, desc in self.INTENTS.items()
            ])
            
            prompt = f"""You are an intent classifier for IA Club, a club that sells AI packages and services.

Available intents:
{intents_list}

Previous conversation context:
{context if context else 'No previous context'}

Current user message: "{message}"

Classify the intent of the current message. Respond in JSON format:
{{
    "intent": "intent_name",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}"""

            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "You are an intent classification assistant. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Validate intent
            if result.get("intent") not in self.INTENTS:
                result["intent"] = "general"
            
            logger.info(f"Intent classified: {result['intent']} (confidence: {result.get('confidence', 0)})")
            return result
            
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            return {
                "intent": "general",
                "confidence": 0.5,
                "reasoning": "Error in classification, defaulting to general"
            }
