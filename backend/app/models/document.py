from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from app.utils.database import Base
import enum


class DocumentStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class DocumentType(str, enum.Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    CSV = "csv"


class Document(Base):
    """Documentos subidos que se procesan"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Archivo
    filename = Column(String(300), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(Enum(DocumentType), nullable=False)
    file_size = Column(Integer)
    
    # Contenido extraído
    extracted_text = Column(Text)
    num_pages = Column(Integer)
    
    # Estado
    status = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING, index=True)
    error_message = Column(Text)
    
    # Procesamiento
    knowledge_items_created = Column(Integer, default=0)
    
    # Metadata
    description = Column(Text)
    category = Column(String(100))
    
    # Timestamps
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    processed_at = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<Document {self.id}: {self.filename}>"
