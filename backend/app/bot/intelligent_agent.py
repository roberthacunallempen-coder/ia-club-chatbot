from sqlalchemy.orm import Session
from app.bot.knowledge_retriever import KnowledgeRetriever
from app.bot.intent_classifier import IntentClassifier
from app.bot.specialized_agents import get_agent
from app.services.openai_service import openai_service
from app.bot.response_templates import templates
from app.bot.customer_profiler import profiler
from app.bot.objection_handler import objection_handler
from app.bot.customer_context import context_manager
from app.bot.conversation_flows import flow_manager
from app.bot.template_manager import TemplateManager
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class IntelligentAgent:
    """
    Multi-agent intelligent system with intent classification
    Routes messages to specialized agents based on intent
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.retriever = KnowledgeRetriever(db)
        self.classifier = IntentClassifier()
        self.template_manager = TemplateManager(db)
    
    async def process_message(
        self,
        message: str,
        history: List[Dict] = None,
        conversation_id: int = None
    ) -> Dict:
        """
        Process user message with multi-agent routing
        
        Flow:
        1. Classify intent
        2. Search relevant knowledge
        3. Route to specialized agent
        4. Generate response
        5. Return with metadata
        
        Args:
            message: User's message
            history: Conversation history
            conversation_id: Optional conversation ID
        
        Returns:
            dict with response, intent, agent_used, knowledge_used, confidence
        """
        try:
            logger.info(f"Processing message: {message[:100]}...")
            
            # === NUEVO: Verificar plantillas automáticas por palabras clave ===
            # Primero verificar si hay una plantilla que coincida
            template_match = self.template_manager.find_template_by_keyword(message)
            
            if template_match:
                logger.info(f"Template matched: {template_match.name}")
                
                # Construir respuesta con los mensajes de la plantilla
                template_messages = []
                for msg in sorted(template_match.messages, key=lambda x: x.get('order', 0)):
                    if msg['type'] == 'text':
                        content = msg['content']
                        # Reemplazar variables básicas
                        content = content.replace('{customer_name}', 'Cliente')
                        template_messages.append(content)
                    else:
                        template_messages.append(f"[{msg['type'].upper()}: {msg.get('content', 'archivo')}]")
                
                response_text = "\n\n".join(template_messages)
                
                return {
                    "response": response_text,
                    "intent": "template",
                    "agent_used": f"Template: {template_match.name}",
                    "confidence": 1.0,
                    "knowledge_used": [],
                    "faqs_used": [],
                    "conversation_id": conversation_id,
                    "template_used": template_match.name
                }
            
            # === NUEVO: Verificar si hay un flujo activo ===
            if flow_manager.has_active_flow(conversation_id or 0):
                flow_result = flow_manager.process_message(conversation_id or 0, message)
                if flow_result:
                    logger.info(f"Flow response generated")
                    return {
                        "response": flow_result["message"],
                        "intent": "flow",
                        "agent_used": "Flow Manager",
                        "confidence": 1.0,
                        "knowledge_used": [],
                        "faqs_used": [],
                        "conversation_id": conversation_id,
                        "in_flow": True,
                        "flow_completed": flow_result.get("completed", False)
                    }
            
            # === NUEVO: Gestión de contexto del cliente ===
            customer_ctx = context_manager.get_context(conversation_id or 0)
            customer_ctx.update_from_message(message)
            
            # === NUEVO: Detectar y manejar objeciones primero ===
            objection_response = objection_handler.handle_objection(message)
            if objection_response:
                logger.info(f"Objection detected and handled")
                objection_data = objection_handler.detect_objection(message)
                customer_ctx.add_objection(objection_data["type"])
                return {
                    "response": objection_response,
                    "intent": "sales",
                    "agent_used": "Objection Handler (Sales)",
                    "confidence": objection_data["confidence"],
                    "knowledge_used": [],
                    "faqs_used": [],
                    "conversation_id": conversation_id,
                    "customer_context": customer_ctx.get_summary()
                }
            
            # === NUEVO: Detectar perfil del cliente ===
            profile_data = profiler.detect_profile(message, history)
            if profile_data["profile"] != "general":
                customer_ctx.set_profile(profile_data["profile"])
                logger.info(f"Customer profile: {profile_data['profile']} (confidence: {profile_data['confidence']})")
            
            # 1. Classify intent
            intent_result = await self.classifier.classify(message, history)
            intent = intent_result["intent"]
            confidence = intent_result.get("confidence", 0.5)
            
            logger.info(f"Intent: {intent} (confidence: {confidence})")
            
            # 2. Search relevant knowledge
            knowledge_items = await self.retriever.search_knowledge(message, limit=5)
            faqs = await self.retriever.search_faqs(message, limit=3)
            
            # Build knowledge context
            knowledge_texts = [
                f"{k.title}: {k.content}" for k in knowledge_items
            ] + [
                f"FAQ - {f.question}: {f.answer}" for f in faqs
            ]
            
            # 3. Get specialized agent for intent
            agent = get_agent(intent)
            
            # 4. Build enhanced context for agent
            context = {
                "history": history or [],
                "intent": intent,
                "confidence": confidence,
                "customer_profile": profile_data,
                "customer_context": customer_ctx.get_context(),
                "should_push_sale": customer_ctx.should_push_for_sale(),
                "customer_summary": customer_ctx.get_summary()
            }
            
            # 5. Generate response using specialized agent
            response = await agent.respond(
                message=message,
                context=context,
                knowledge=knowledge_texts
            )
            
            # === NUEVO: Mejorar respuesta con templates si es ventas ===
            if intent == "sales":
                # Agregar perfil personalizado si se detectó
                if profile_data["profile"] != "general" and profile_data["confidence"] > 0.5:
                    personalized_pitch = profiler.get_personalized_pitch(profile_data["profile"])
                    if personalized_pitch and personalized_pitch not in response:
                        response = f"{response}\n\n{personalized_pitch}"
                
                # Agregar social proof si no está ya
                if "grupo" not in response.lower() and "whatsapp" not in response.lower():
                    response = templates.add_social_proof_to_response(response)
                
                # Asegurar CTA si no tiene
                if "?" not in response[-100:]:  # Si no hay pregunta en los últimos 100 chars
                    response = templates.add_cta_to_response(response, "ventas")
            
            # 6. Update usage statistics
            knowledge_ids = [k.id for k in knowledge_items]
            faq_ids = [f.id for f in faqs]
            await self.retriever.update_usage_stats(knowledge_ids, faq_ids)
            
            logger.info(
                f"Response generated by {agent.name} - "
                f"Knowledge: {len(knowledge_items)}, FAQs: {len(faqs)}, "
                f"Profile: {profile_data.get('profile', 'none')}, "
                f"Customer: {customer_ctx.get_summary()}"
            )
            
            return {
                "response": response,
                "intent": intent,
                "agent_used": agent.name,
                "confidence": confidence,
                "knowledge_used": [
                    {"id": k.id, "title": k.title, "category": k.category}
                    for k in knowledge_items
                ],
                "faqs_used": [
                    {"id": f.id, "question": f.question, "category": f.category}
                    for f in faqs
                ],
                "conversation_id": conversation_id,
                "customer_profile": profile_data.get("profile"),
                "customer_context": customer_ctx.get_summary(),
                "engagement_level": customer_ctx.context["engagement_level"]
            }
        
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return {
                "response": "Lo siento, estoy teniendo problemas técnicos en este momento. ¿Podrías intentar de nuevo?",
                "intent": "error",
                "agent_used": "Error Handler",
                "confidence": 0.0,
                "knowledge_used": [],
                "faqs_used": [],
                "conversation_id": conversation_id,
                "customer_profile": None,
                "customer_context": None,
                "engagement_level": None,
                "error": str(e)
            }
