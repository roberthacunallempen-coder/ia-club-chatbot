from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.document import DocumentStatus, DocumentType


class DocumentBase(BaseModel):
    description: Optional[str] = None
    category: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class Document(DocumentBase):
    id: int
    filename: str
    file_type: DocumentType
    file_size: int
    status: DocumentStatus
    error_message: Optional[str]
    extracted_text: Optional[str]
    num_pages: Optional[int]
    knowledge_items_created: int
    uploaded_at: datetime
    processed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class DocumentList(BaseModel):
    items: List[Document]
    total: int
