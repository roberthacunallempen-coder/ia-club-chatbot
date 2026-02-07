from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks, Form
from sqlalchemy.orm import Session
from typing import Optional
from pathlib import Path
import shutil
from datetime import datetime
from app.models.document import Document, DocumentStatus, DocumentType
from app.schemas.document import Document as DocumentSchema, DocumentList
from app.utils.database import get_db
from app.services.document_parser import parse_document, create_knowledge_from_document
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/documents")

Path(settings.upload_dir).mkdir(exist_ok=True)


@router.post("/upload", response_model=DocumentSchema, status_code=201)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload document (PDF, DOCX, TXT)"""
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > settings.max_file_size:
        raise HTTPException(status_code=413, detail=f"File too large. Max {settings.max_file_size / 1024 / 1024}MB")
    
    file_extension = Path(file.filename).suffix.lower().replace(".", "")
    if file_extension not in ["pdf", "docx", "txt", "csv"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF, DOCX, TXT or CSV")
    
    file_path = Path(settings.upload_dir) / f"{datetime.now().timestamp()}_{file.filename}"
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    document = Document(
        filename=file.filename,
        file_path=str(file_path),
        file_type=file_extension,
        file_size=file_size,
        description=description,
        category=category,
        status=DocumentStatus.PENDING
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    background_tasks.add_task(process_document, document.id)
    
    return document


async def process_document(document_id: int):
    """Process document in background"""
    from app.utils.database import SessionLocal
    db = SessionLocal()
    
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return
        
        document.status = DocumentStatus.PROCESSING
        db.commit()
        
        extracted_text = await parse_document(document.file_path, document.file_type)
        document.extracted_text = extracted_text
        
        knowledge_count = await create_knowledge_from_document(
            document_id=document.id,
            text=extracted_text,
            category=document.category or "General",
            db=db
        )
        
        document.status = DocumentStatus.COMPLETED
        document.knowledge_items_created = knowledge_count
        document.processed_at = datetime.now()
        db.commit()
        
    except Exception as e:
        document.status = DocumentStatus.ERROR
        document.error_message = str(e)
        db.commit()
    finally:
        db.close()


@router.get("", response_model=DocumentList)
@router.get("/", response_model=DocumentList)
async def list_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List uploaded documents"""
    total = db.query(Document).count()
    documents = db.query(Document).order_by(Document.uploaded_at.desc()).offset(skip).limit(limit).all()
    return DocumentList(items=documents, total=total)


@router.get("/{document_id}", response_model=DocumentSchema)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """Get document by ID"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}", status_code=204)
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete document"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        Path(document.file_path).unlink()
    except:
        pass
    
    db.delete(document)
    db.commit()
