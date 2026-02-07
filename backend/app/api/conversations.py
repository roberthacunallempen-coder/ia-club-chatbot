from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.conversation import Conversation
from app.schemas.conversation import Conversation as ConversationSchema, ConversationList, ConversationStats
from app.utils.database import get_db

router = APIRouter(prefix="/api/conversations")


@router.get("", response_model=ConversationList)
@router.get("/", response_model=ConversationList)
async def list_conversations(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List conversations"""
    total = db.query(Conversation).count()
    conversations = db.query(Conversation).order_by(desc(Conversation.started_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    return ConversationList(items=conversations, total=total, page=page, page_size=page_size)


@router.get("/stats", response_model=ConversationStats)
async def get_stats(db: Session = Depends(get_db)):
    """Get conversation statistics"""
    total_conversations = db.query(func.count(Conversation.id)).scalar()
    total_messages = db.query(func.sum(Conversation.total_messages)).scalar() or 0
    
    avg_rating = db.query(func.avg(Conversation.customer_rating)).filter(Conversation.customer_rating.isnot(None)).scalar() or 0
    
    helpful_count = db.query(func.count(Conversation.id)).filter(Conversation.was_helpful == True).scalar()
    helpful_percentage = (helpful_count / total_conversations * 100) if total_conversations > 0 else 0
    
    human_escalations = db.query(func.count(Conversation.id)).filter(Conversation.needed_human_agent == True).scalar()
    human_escalation_rate = (human_escalations / total_conversations * 100) if total_conversations > 0 else 0
    
    avg_response_time = db.query(func.avg(Conversation.avg_response_time)).scalar() or 0
    
    return ConversationStats(
        total_conversations=total_conversations,
        total_messages=int(total_messages),
        avg_rating=round(avg_rating, 2),
        helpful_percentage=round(helpful_percentage, 2),
        human_escalation_rate=round(human_escalation_rate, 2),
        avg_response_time=round(avg_response_time, 2),
        top_knowledge_used=[],
        top_faqs_used=[]
    )


@router.get("/{conversation_id}", response_model=ConversationSchema)
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """Get conversation by ID"""
    conversation = db.query(Conversation).filter(Conversation.chatwoot_conversation_id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation
