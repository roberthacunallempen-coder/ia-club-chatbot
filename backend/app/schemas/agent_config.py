"""
Agent Configuration Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AgentConfigBase(BaseModel):
    agent_type: str = Field(..., description="Agent type: sales, design, order_tracking, support, general")
    agent_name: str = Field(..., description="Display name for the agent")
    role_description: str = Field(..., description="Brief role description")
    instructions: str = Field(..., description="Detailed instructions for the agent")
    temperature: int = Field(70, ge=0, le=100, description="Temperature 0-100")
    max_tokens: int = Field(500, ge=100, le=2000, description="Max tokens per response")
    is_active: bool = Field(True, description="Whether agent is active")


class AgentConfigCreate(AgentConfigBase):
    pass


class AgentConfigUpdate(BaseModel):
    agent_name: Optional[str] = None
    role_description: Optional[str] = None
    instructions: Optional[str] = None
    temperature: Optional[int] = Field(None, ge=0, le=100)
    max_tokens: Optional[int] = Field(None, ge=100, le=2000)
    is_active: Optional[bool] = None


class AgentConfig(AgentConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
