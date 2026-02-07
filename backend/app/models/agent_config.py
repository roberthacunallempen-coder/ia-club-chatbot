"""
Agent Configuration Model
Stores customization for each specialized agent
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.utils.database import Base


class AgentConfig(Base):
    """Agent configuration and customization"""
    __tablename__ = "agent_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_type = Column(String(50), unique=True, nullable=False, index=True)  # sales, design, etc
    agent_name = Column(String(100), nullable=False)
    role_description = Column(String(200), nullable=False)
    instructions = Column(Text, nullable=False)
    temperature = Column(Integer, default=70)  # 0-100, will be divided by 100
    max_tokens = Column(Integer, default=500)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<AgentConfig {self.agent_type}: {self.agent_name}>"
