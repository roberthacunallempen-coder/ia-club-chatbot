from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FAQBase(BaseModel):
    question: str = Field(..., min_length=5)
    answer: str = Field(..., min_length=10)
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    question_variations: List[str] = Field(default_factory=list)
    is_active: bool = True
    priority: int = Field(default=0, ge=0, le=100)


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    question_variations: Optional[List[str]] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None


class FAQ(FAQBase):
    id: int
    times_used: int
    helpful_count: int
    not_helpful_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class FAQList(BaseModel):
    items: List[FAQ]
    total: int
    page: int
    page_size: int
