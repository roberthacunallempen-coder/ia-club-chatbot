from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.utils.database import Base


class FAQ(Base):
    """Preguntas y respuestas específicas"""
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Pregunta y respuesta
    question = Column(Text, nullable=False, index=True)
    answer = Column(Text, nullable=False)
    
    # Organización
    category = Column(String(100), index=True)
    tags = Column(JSON, default=list)
    
    # Variaciones de la pregunta para mejor matching
    question_variations = Column(JSON, default=list)
    
    # Estado
    is_active = Column(Boolean, default=True, index=True)
    priority = Column(Integer, default=0, index=True)
    
    # Estadísticas
    times_used = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    not_helpful_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<FAQ {self.id}: {self.question[:50]}>"
