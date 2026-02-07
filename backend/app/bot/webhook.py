from typing import List, Dict, Optional
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.bot.intelligent_agent import IntelligentAgent
from app.services.chatwoot_service import chatwoot_service
from app.models.conversation import Conversation
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/webhook/chatwoot")
async def chatwoot_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Webhook endpoint to receive messages from Chatwoot
    
    Chatwoot sends webhooks for various events.
    We only process incoming messages (from customers).
    """
    try:
        data = await request.json()
        
        event = data.get('event')
        logger.info(f"Webhook received: {event}")
        
        # Only process incoming messages
        if event != 'message_created':
            return {"status": "ignored", "reason": "not message_created event"}
        
        message_type = data.get('message_type')
        if message_type != 'incoming':
            return {"status": "ignored", "reason": "not incoming message"}
        
        # Extract data
        conversation_id = data.get('conversation', {}).get('id')
        user_message = data.get('content', '')
        sender = data.get('sender', {})
        
        if not conversation_id or not user_message:
            logger.warning("Missing conversation_id or message content")
            return {"status": "error", "reason": "missing data"}
        
        logger.info(f"Processing message from conversation {conversation_id}")
        
        # Get or create conversation record
        conversation = db.query(Conversation).filter(
            Conversation.chatwoot_conversation_id == conversation_id
        ).first()
        
        if not conversation:
            conversation = Conversation(
                chatwoot_conversation_id=conversation_id,
                customer_name=sender.get('name'),
                customer_email=sender.get('email'),
                started_at=datetime.now(),
                total_messages=0,
                bot_messages=0,
                human_messages=0
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Get conversation history from Chatwoot
        history = await get_conversation_history(conversation_id)
        
        # Process with intelligent agent
        agent = IntelligentAgent(db)
        result = await agent.process_message(
            message=user_message,
            history=history,
            conversation_id=conversation_id
        )
        
        # Send response back to Chatwoot
        await chatwoot_service.send_message(
            conversation_id=conversation_id,
            content=result["response"]
        )
        
        # Update conversation statistics
        conversation.total_messages += 2  # User message + Bot response
        conversation.bot_messages += 1
        
        # Track knowledge usage
        knowledge_ids = [k["id"] for k in result["knowledge_used"]]
        faq_ids = [f["id"] for f in result["faqs_used"]]
        
        conversation.knowledge_ids_used = list(set(
            (conversation.knowledge_ids_used or []) + knowledge_ids
        ))
        conversation.faq_ids_used = list(set(
            (conversation.faq_ids_used or []) + faq_ids
        ))
        
        db.commit()
        
        logger.info(f"Response sent to conversation {conversation_id} (confidence: {result['confidence']})")
        
        return {
            "status": "success",
            "conversation_id": conversation_id,
            "confidence": result["confidence"],
            "knowledge_used": len(result["knowledge_used"]),
            "faqs_used": len(result["faqs_used"])
        }
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        
        # Try to send error message to user
        try:
            if conversation_id:
                await chatwoot_service.send_message(
                    conversation_id=conversation_id,
                    content="Disculpa, estoy teniendo problemas técnicos. Un agente humano te atenderá pronto."
                )
        except:
            pass
        
        raise HTTPException(status_code=500, detail=str(e))


async def get_conversation_history(conversation_id: int) -> List[Dict]:
    """
    Get conversation history from Chatwoot
    
    Args:
        conversation_id: Chatwoot conversation ID
    
    Returns:
        List of message dicts with 'role' and 'content'
    """
    try:
        messages = await chatwoot_service.get_messages(conversation_id)
        
        history = []
        
        # Convert Chatwoot messages to our format
        for msg in messages[-20:]:  # Last 20 messages
            # message_type: 0=incoming (user), 1=outgoing (bot/agent)
            message_type = msg.get('message_type')
            content = msg.get('content', '').strip()
            
            if not content:
                continue
            
            role = "user" if message_type == 0 else "assistant"
            
            history.append({
                "role": role,
                "content": content
            })
        
        logger.info(f"Retrieved {len(history)} messages from conversation {conversation_id}")
        return history
    
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        return []


@router.get("/webhook/health")
async def webhook_health():
    """Health check endpoint for webhook"""
    return {"status": "ok", "webhook": "chatwoot"}
