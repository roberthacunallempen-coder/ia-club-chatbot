from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Float, Text
from sqlalchemy.sql import func
from app.utils.database import Base


class Conversation(Base):
    """Registro de conversaciones para analytics"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    chatwoot_conversation_id = Column(Integer, unique=True, nullable=False, index=True)
    
    # Info del cliente
    customer_name = Column(String(200))
    customer_email = Column(String(200))
    
    # Métricas
    total_messages = Column(Integer, default=0)
    bot_messages = Column(Integer, default=0)
    human_messages = Column(Integer, default=0)
    
    # Conocimientos usados
    knowledge_ids_used = Column(JSON, default=list)
    faq_ids_used = Column(JSON, default=list)
    
    # Feedback
    customer_rating = Column(Integer)
    was_helpful = Column(Boolean)
    needed_human_agent = Column(Boolean, default=False)
    feedback_text = Column(Text)
    
    # Tiempos
    started_at = Column(DateTime(timezone=True), index=True)
    ended_at = Column(DateTime(timezone=True))
    avg_response_time = Column(Float)
    
    # Extra data
    extra_data = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<Conversation {self.chatwoot_conversation_id}>"
