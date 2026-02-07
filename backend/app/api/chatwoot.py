from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
import logging
import os
import hmac
import hashlib

from app.bot.intelligent_agent import IntelligentAgent
from app.utils.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

CHATWOOT_URL = os.getenv("CHATWOOT_URL", "")
CHATWOOT_ACCESS_TOKEN = os.getenv("CHATWOOT_ACCESS_TOKEN", "")
CHATWOOT_ACCOUNT_ID = int(os.getenv("CHATWOOT_ACCOUNT_ID", "0"))
CHATWOOT_INBOX_ID = int(os.getenv("CHATWOOT_INBOX_ID", "0"))
CHATWOOT_WEBHOOK_SECRET = os.getenv("CHATWOOT_WEBHOOK_SECRET", "")


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verify the webhook signature from Chatwoot"""
    if not CHATWOOT_WEBHOOK_SECRET:
        logger.warning("CHATWOOT_WEBHOOK_SECRET not configured, skipping signature verification")
        return True
    
    expected_signature = hmac.new(
        CHATWOOT_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)


@router.post("/webhook")
async def chatwoot_webhook(
    request: Request,
    x_chatwoot_signature: Optional[str] = Header(None)
):
    """
    Webhook endpoint to receive events from Chatwoot.
    Responds to incoming messages and sends intelligent responses.
    """
    try:
        # Get raw body for signature verification
        body = await request.body()
        
        # Verify signature if provided
        if x_chatwoot_signature:
            if not verify_webhook_signature(body, x_chatwoot_signature):
                logger.error("Invalid webhook signature")
                raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse JSON payload
        payload = await request.json()
        
        logger.info(f"Received Chatwoot webhook: {payload.get('event')}")
        
        # Only process message_created events from customers
        event = payload.get("event")
        if event != "message_created":
            return {"status": "ignored", "reason": "not a message_created event"}
        
        message_type = payload.get("message_type")
        if message_type != "incoming":
            return {"status": "ignored", "reason": "not an incoming message"}
        
        # Extract message data
        conversation = payload.get("conversation", {})
        conversation_id = conversation.get("id")
        inbox_id = conversation.get("inbox_id")
        
        # Only process messages from our configured inbox
        if inbox_id != CHATWOOT_INBOX_ID:
            return {"status": "ignored", "reason": f"message from different inbox {inbox_id}"}
        
        message = payload.get("content")
        sender = payload.get("sender", {})
        sender_name = sender.get("name", "Usuario")
        
        if not message:
            return {"status": "ignored", "reason": "no message content"}
        
        logger.info(f"Processing message from {sender_name} in conversation {conversation_id}: {message}")
        
        # Get conversation context from database
        db = next(get_db())
        try:
            # Generate intelligent response
            agent = IntelligentAgent(db)
            response = await agent.process_message(
                message=message,
                conversation_id=str(conversation_id)
            )
            
            # Send response back to Chatwoot
            import httpx
            async with httpx.AsyncClient() as client:
                chatwoot_response = await client.post(
                    f"{CHATWOOT_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/conversations/{conversation_id}/messages",
                    headers={
                        "api_access_token": CHATWOOT_ACCESS_TOKEN,
                        "Content-Type": "application/json"
                    },
                    json={
                        "content": response.get("response", "Lo siento, no pude procesar tu mensaje."),
                        "message_type": "outgoing",
                        "private": False
                    },
                    timeout=30.0
                )
                
                if chatwoot_response.status_code not in [200, 201]:
                    logger.error(f"Failed to send message to Chatwoot: {chatwoot_response.text}")
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to send response to Chatwoot"
                    )
            
            logger.info(f"Successfully sent response to conversation {conversation_id}")
            
            return {
                "status": "success",
                "conversation_id": conversation_id,
                "response_sent": True
            }
            
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Error processing Chatwoot webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def chatwoot_status():
    """Check Chatwoot integration status"""
    return {
        "configured": bool(CHATWOOT_URL and CHATWOOT_ACCESS_TOKEN and CHATWOOT_ACCOUNT_ID and CHATWOOT_INBOX_ID),
        "chatwoot_url": CHATWOOT_URL,
        "account_id": CHATWOOT_ACCOUNT_ID,
        "inbox_id": CHATWOOT_INBOX_ID,
        "webhook_secret_set": bool(CHATWOOT_WEBHOOK_SECRET)
    }
