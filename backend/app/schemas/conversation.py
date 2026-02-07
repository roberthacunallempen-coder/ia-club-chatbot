from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ConversationBase(BaseModel):
    chatwoot_conversation_id: int
    customer_name: Optional[str]
    customer_email: Optional[str]


class Conversation(ConversationBase):
    id: int
    total_messages: int
    bot_messages: int
    human_messages: int
    knowledge_ids_used: List[int]
    faq_ids_used: List[int]
    customer_rating: Optional[int]
    was_helpful: Optional[bool]
    needed_human_agent: bool
    feedback_text: Optional[str]
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    avg_response_time: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationList(BaseModel):
    items: List[Conversation]
    total: int
    page: int
    page_size: int


class ConversationStats(BaseModel):
    total_conversations: int
    total_messages: int
    avg_rating: float
    helpful_percentage: float
    human_escalation_rate: float
    avg_response_time: float
    top_knowledge_used: List[dict]
    top_faqs_used: List[dict]
