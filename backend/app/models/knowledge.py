from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.utils.database import Base


class Knowledge(Base):
    """Base de conocimientos que el bot usará para responder"""
    __tablename__ = "knowledge"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Contenido
    title = Column(String(300), nullable=False, index=True)
    category = Column(String(100), index=True)
    content = Column(Text, nullable=False)
    keywords = Column(JSON, default=list)
    
    # Metadata
    source = Column(String(300))
    priority = Column(Integer, default=0, index=True)
    
    # Estado
    is_active = Column(Boolean, default=True, index=True)
    
    # Estadísticas
    times_used = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Knowledge {self.id}: {self.title}>"
