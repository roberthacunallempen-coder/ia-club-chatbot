from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from datetime import datetime


class MessageItem(BaseModel):
    """Individual message in a template sequence"""
    order: int = Field(..., ge=0, description="Order in the sequence (0-based)")
    type: Literal["text", "image", "document", "audio", "video"] = Field(
        ..., description="Type of message"
    )
    content: str = Field(..., min_length=1, description="Text content or file name")
    file_url: Optional[str] = Field(None, description="URL or path to the file (for non-text messages)")
    delay_seconds: Optional[int] = Field(
        0, ge=0, le=60, 
        description="Delay in seconds before sending this message (0-60)"
    )
    
    @field_validator('file_url')
    @classmethod
    def validate_file_url(cls, v, info):
        """Validate that file_url is provided for non-text messages"""
        if info.data.get('type') != 'text' and not v:
            raise ValueError(f"file_url is required for {info.data.get('type')} messages")
        return v


class MessageTemplateBase(BaseModel):
    """Base schema for MessageTemplate"""
    name: str = Field(..., min_length=1, max_length=200, description="Template name")
    description: Optional[str] = Field(None, description="Template description")
    messages: List[MessageItem] = Field(
        ..., min_length=1, description="Sequence of messages"
    )
    category: Optional[str] = Field(None, max_length=100, description="Template category")
    trigger_keywords: Optional[List[str]] = Field(
        None, description="Keywords that trigger this template"
    )
    is_active: bool = Field(True, description="Whether template is active")
    
    @field_validator('messages')
    @classmethod
    def validate_messages_order(cls, v):
        """Validate that message orders are sequential"""
        if not v:
            raise ValueError("At least one message is required")
        
        orders = [msg.order for msg in v]
        if len(orders) != len(set(orders)):
            raise ValueError("Message orders must be unique")
        
        if sorted(orders) != list(range(len(orders))):
            raise ValueError("Message orders must be sequential starting from 0")
        
        return v


class MessageTemplateCreate(MessageTemplateBase):
    """Schema for creating a new template"""
    pass


class MessageTemplateUpdate(BaseModel):
    """Schema for updating a template"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    messages: Optional[List[MessageItem]] = Field(None, min_length=1)
    category: Optional[str] = Field(None, max_length=100)
    trigger_keywords: Optional[List[str]] = None
    is_active: Optional[bool] = None
    
    @field_validator('messages')
    @classmethod
    def validate_messages_order(cls, v):
        """Validate that message orders are sequential"""
        if v is not None:
            orders = [msg.order for msg in v]
            if len(orders) != len(set(orders)):
                raise ValueError("Message orders must be unique")
            
            if sorted(orders) != list(range(len(orders))):
                raise ValueError("Message orders must be sequential starting from 0")
        
        return v


class MessageTemplateResponse(MessageTemplateBase):
    """Schema for template responses"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class MessageTemplateList(BaseModel):
    """Schema for listing templates"""
    templates: List[MessageTemplateResponse]
    total: int


class SendTemplateRequest(BaseModel):
    """Schema for sending a template to a conversation"""
    template_id: int = Field(..., description="ID of the template to send")
    conversation_id: int = Field(..., description="Chatwoot conversation ID")
    variables: Optional[dict] = Field(
        None, 
        description="Variables to replace in text messages (e.g., {name} -> value)"
    )
