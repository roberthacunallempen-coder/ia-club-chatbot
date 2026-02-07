from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.utils.database import get_db
from app.bot.intelligent_agent import IntelligentAgent

router = APIRouter(prefix="/api/test")


class TestMessage(BaseModel):
    message: str
    conversation_history: list = []


class TestResponse(BaseModel):
    response: str
    intent: str
    agent_used: str
    confidence: float
    knowledge_used: list
    faqs_used: list
    customer_profile: str = ""
    customer_context: str = ""
    engagement_level: str = ""


@router.post("/chat", response_model=TestResponse)
async def test_chat(test_msg: TestMessage, db: Session = Depends(get_db)):
    """Test bot in real-time without Chatwoot"""
    agent = IntelligentAgent(db)
    
    result = await agent.process_message(
        message=test_msg.message,
        history=test_msg.conversation_history
    )
    
    return TestResponse(
        response=result["response"],
        intent=result.get("intent", "unknown"),
        agent_used=result.get("agent_used", "Unknown Agent"),
        confidence=result.get("confidence", 0.0),
        knowledge_used=result.get("knowledge_used", []),
        faqs_used=result.get("faqs_used", []),
        customer_profile=result.get("customer_profile") or "",
        customer_context=result.get("customer_context") or "",
        engagement_level=result.get("engagement_level") or ""
    )
