from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import shutil
from pathlib import Path

from app.utils.database import get_db
from app.models.message_template import MessageTemplate
from app.schemas.message_template import (
    MessageTemplateCreate,
    MessageTemplateUpdate,
    MessageTemplateResponse,
    MessageTemplateList,
    SendTemplateRequest
)
from app.services.chatwoot_service import chatwoot_service
from app.config import get_settings

router = APIRouter(prefix="/api/templates", tags=["Message Templates"])
settings = get_settings()


@router.get("", response_model=MessageTemplateList)
@router.get("/", response_model=MessageTemplateList)
async def list_templates(
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all message templates with optional filters
    """
    query = db.query(MessageTemplate)
    
    if category:
        query = query.filter(MessageTemplate.category == category)
    
    if is_active is not None:
        query = query.filter(MessageTemplate.is_active == is_active)
    
    total = query.count()
    templates = query.offset(skip).limit(limit).all()
    
    return MessageTemplateList(templates=templates, total=total)


@router.get("/{template_id}", response_model=MessageTemplateResponse)
async def get_template(template_id: int, db: Session = Depends(get_db)):
    """
    Get a specific message template by ID
    """
    template = db.query(MessageTemplate).filter(MessageTemplate.id == template_id).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with id {template_id} not found"
        )
    
    return template


@router.post("", response_model=MessageTemplateResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=MessageTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template: MessageTemplateCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new message template
    """
    # Check if name already exists
    existing = db.query(MessageTemplate).filter(MessageTemplate.name == template.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Template with name '{template.name}' already exists"
        )
    
    # Convert messages to dict format for JSON storage
    messages_data = [msg.model_dump() for msg in template.messages]
    
    db_template = MessageTemplate(
        name=template.name,
        description=template.description,
        messages=messages_data,
        category=template.category,
        trigger_keywords=template.trigger_keywords,
        is_active=template.is_active
    )
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    
    return db_template


@router.put("/{template_id}", response_model=MessageTemplateResponse)
async def update_template(
    template_id: int,
    template_update: MessageTemplateUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing message template
    """
    db_template = db.query(MessageTemplate).filter(MessageTemplate.id == template_id).first()
    
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with id {template_id} not found"
        )
    
    # Check name uniqueness if updating name
    if template_update.name and template_update.name != db_template.name:
        existing = db.query(MessageTemplate).filter(MessageTemplate.name == template_update.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Template with name '{template_update.name}' already exists"
            )
    
    # Update fields
    update_data = template_update.model_dump(exclude_unset=True)
    
    # Convert messages to dict format if provided
    if 'messages' in update_data and update_data['messages']:
        update_data['messages'] = [msg.model_dump() for msg in template_update.messages]
    
    for field, value in update_data.items():
        setattr(db_template, field, value)
    
    db.commit()
    db.refresh(db_template)
    
    return db_template


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(template_id: int, db: Session = Depends(get_db)):
    """
    Delete a message template
    """
    db_template = db.query(MessageTemplate).filter(MessageTemplate.id == template_id).first()
    
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with id {template_id} not found"
        )
    
    db.delete(db_template)
    db.commit()
    
    return None


@router.post("/send", status_code=status.HTTP_200_OK)
async def send_template(
    request: SendTemplateRequest,
    db: Session = Depends(get_db)
):
    """
    Send a template sequence to a Chatwoot conversation
    """
    # Get the template
    template = db.query(MessageTemplate).filter(MessageTemplate.id == request.template_id).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with id {request.template_id} not found"
        )
    
    if not template.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Template '{template.name}' is not active"
        )
    
    try:
        # Send the message sequence
        sent_messages = await chatwoot_service.send_template_sequence(
            conversation_id=request.conversation_id,
            messages=template.messages,
            variables=request.variables or {}
        )
        
        return {
            "success": True,
            "template_name": template.name,
            "messages_sent": len(sent_messages),
            "conversation_id": request.conversation_id
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending template: {str(e)}"
        )


@router.post("/upload-file", status_code=status.HTTP_201_CREATED)
async def upload_template_file(
    file: UploadFile = File(...),
    category: str = Form("general")
):
    """
    Upload a file (image, PDF, etc.) to be used in templates
    Returns the file path to use in template configuration
    """
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = Path(settings.upload_dir) / "templates" / category
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = upload_dir / file.filename
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "success": True,
            "filename": file.filename,
            "file_path": str(file_path),
            "category": category
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )


@router.get("/categories/list", response_model=List[str])
async def list_categories(db: Session = Depends(get_db)):
    """
    Get list of all template categories
    """
    categories = db.query(MessageTemplate.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]
