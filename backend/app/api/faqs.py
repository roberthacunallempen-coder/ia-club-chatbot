from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.faq import FAQ
from app.schemas.faq import FAQ as FAQSchema, FAQCreate, FAQUpdate, FAQList
from app.utils.database import get_db

router = APIRouter(prefix="/api/faqs")


@router.get("", response_model=FAQList)
@router.get("/", response_model=FAQList)
async def list_faqs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List FAQs with filters"""
    query = db.query(FAQ)
    
    if active_only:
        query = query.filter(FAQ.is_active == True)
    
    if category:
        query = query.filter(FAQ.category == category)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(or_(FAQ.question.ilike(search_filter), FAQ.answer.ilike(search_filter)))
    
    total = query.count()
    items = query.order_by(FAQ.priority.desc(), FAQ.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return FAQList(items=items, total=total, page=page, page_size=page_size)


@router.get("/{faq_id}", response_model=FAQSchema)
async def get_faq(faq_id: int, db: Session = Depends(get_db)):
    """Get FAQ by ID"""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return faq


@router.post("", response_model=FAQSchema, status_code=201)
@router.post("/", response_model=FAQSchema, status_code=201)
async def create_faq(faq_in: FAQCreate, db: Session = Depends(get_db)):
    """Create new FAQ"""
    faq = FAQ(**faq_in.dict())
    db.add(faq)
    db.commit()
    db.refresh(faq)
    return faq


@router.put("/{faq_id}", response_model=FAQSchema)
async def update_faq(faq_id: int, faq_in: FAQUpdate, db: Session = Depends(get_db)):
    """Update FAQ"""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    update_data = faq_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(faq, field, value)
    
    db.commit()
    db.refresh(faq)
    return faq


@router.delete("/{faq_id}", status_code=204)
async def delete_faq(faq_id: int, db: Session = Depends(get_db)):
    """Delete FAQ"""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    db.delete(faq)
    db.commit()


@router.post("/{faq_id}/feedback")
async def faq_feedback(faq_id: int, helpful: bool, db: Session = Depends(get_db)):
    """Register FAQ feedback"""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    if helpful:
        faq.helpful_count += 1
    else:
        faq.not_helpful_count += 1
    
    db.commit()
    return {"helpful_count": faq.helpful_count, "not_helpful_count": faq.not_helpful_count}
