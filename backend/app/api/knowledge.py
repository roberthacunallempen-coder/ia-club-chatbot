from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, String
from typing import List, Optional
from app.models.knowledge import Knowledge
from app.schemas.knowledge import (
    Knowledge as KnowledgeSchema,
    KnowledgeCreate,
    KnowledgeUpdate,
    KnowledgeList
)
from app.utils.database import get_db

router = APIRouter(prefix="/api/knowledge")


@router.get("", response_model=KnowledgeList)
@router.get("/", response_model=KnowledgeList)
async def list_knowledge(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List knowledge with pagination and filters"""
    query = db.query(Knowledge)
    
    if active_only:
        query = query.filter(Knowledge.is_active == True)
    
    if category:
        query = query.filter(Knowledge.category == category)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Knowledge.title.ilike(search_filter),
                Knowledge.content.ilike(search_filter),
                Knowledge.keywords.cast(String).ilike(search_filter)
            )
        )
    
    total = query.count()
    items = query.order_by(Knowledge.priority.desc(), Knowledge.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return KnowledgeList(items=items, total=total, page=page, page_size=page_size)


@router.get("/{knowledge_id}", response_model=KnowledgeSchema)
async def get_knowledge(knowledge_id: int, db: Session = Depends(get_db)):
    """Get knowledge by ID"""
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    return knowledge


@router.post("", response_model=KnowledgeSchema, status_code=201)
@router.post("/", response_model=KnowledgeSchema, status_code=201)
async def create_knowledge(knowledge_in: KnowledgeCreate, db: Session = Depends(get_db)):
    """Create new knowledge"""
    knowledge = Knowledge(**knowledge_in.dict())
    db.add(knowledge)
    db.commit()
    db.refresh(knowledge)
    return knowledge


@router.put("/{knowledge_id}", response_model=KnowledgeSchema)
async def update_knowledge(knowledge_id: int, knowledge_in: KnowledgeUpdate, db: Session = Depends(get_db)):
    """Update knowledge"""
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    
    update_data = knowledge_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(knowledge, field, value)
    
    db.commit()
    db.refresh(knowledge)
    return knowledge


@router.delete("/{knowledge_id}", status_code=204)
async def delete_knowledge(knowledge_id: int, db: Session = Depends(get_db)):
    """Delete knowledge"""
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    
    db.delete(knowledge)
    db.commit()


@router.get("/categories/list", response_model=List[str])
async def list_categories(db: Session = Depends(get_db)):
    """Get all unique categories"""
    categories = db.query(Knowledge.category).distinct().filter(Knowledge.category.isnot(None)).all()
    return sorted([cat[0] for cat in categories])
