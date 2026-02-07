from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class KnowledgeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    category: Optional[str] = Field(None, max_length=100)
    content: str = Field(..., min_length=1)
    keywords: List[str] = Field(default_factory=list)
    source: Optional[str] = Field(None, max_length=300)
    priority: int = Field(default=0, ge=0, le=100)
    is_active: bool = True


class KnowledgeCreate(KnowledgeBase):
    pass


class KnowledgeUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    keywords: Optional[List[str]] = None
    source: Optional[str] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None


class Knowledge(KnowledgeBase):
    id: int
    times_used: int
    last_used_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class KnowledgeList(BaseModel):
    items: List[Knowledge]
    total: int
    page: int
    page_size: int
