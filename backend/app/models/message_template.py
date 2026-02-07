from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Boolean
from sqlalchemy.sql import func
from app.utils.database import Base


class MessageTemplate(Base):
    """
    Model for storing predefined message sequences
    A template contains a sequence of messages (text, images, files, etc.)
    that are sent in a specific order configured by the user
    """
    __tablename__ = "message_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    # JSON array containing the message sequence
    # Each item has: {order: int, type: str, content: str, file_url: str (optional)}
    # type can be: "text", "image", "document", "audio", "video"
    messages = Column(JSON, nullable=False)
    
    # Category or tag for organization
    category = Column(String(100), nullable=True, index=True)
    
    # Keywords that can trigger this template
    trigger_keywords = Column(JSON, nullable=True)  # Array of strings
    
    # Whether this template is active and can be used
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<MessageTemplate(id={self.id}, name={self.name})>"
