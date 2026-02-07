from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.settings import Settings
from app.schemas.settings import SettingsCreate, SettingsUpdate, Settings as SettingResponse
from typing import List

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/{key}", response_model=SettingResponse)
def get_setting(key: str, db: Session = Depends(get_db)):
    """Get a specific setting by key"""
    setting = db.query(Settings).filter(Settings.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.get("", response_model=List[SettingResponse])
@router.get("/", response_model=List[SettingResponse])
def get_all_settings(
    category: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all settings, optionally filtered by category"""
    query = db.query(Settings)
    
    if category:
        query = query.filter(Settings.category == category)
    
    settings = query.offset(skip).limit(limit).all()
    return settings


@router.post("", response_model=SettingResponse)
@router.post("/", response_model=SettingResponse)
def create_or_update_setting(setting_data: SettingsCreate, db: Session = Depends(get_db)):
    """Create a new setting or update if exists"""
    # Check if setting exists
    existing = db.query(Settings).filter(Settings.key == setting_data.key).first()
    
    if existing:
        # Update existing
        for field, value in setting_data.dict(exclude_unset=True).items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new
        new_setting = Settings(**setting_data.dict())
        db.add(new_setting)
        db.commit()
        db.refresh(new_setting)
        return new_setting


@router.put("/{key}", response_model=SettingResponse)
def update_setting(key: str, setting_data: SettingsUpdate, db: Session = Depends(get_db)):
    """Update an existing setting"""
    setting = db.query(Settings).filter(Settings.key == key).first()
    
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    for field, value in setting_data.dict(exclude_unset=True).items():
        setattr(setting, field, value)
    
    db.commit()
    db.refresh(setting)
    return setting


@router.delete("/{key}")
def delete_setting(key: str, db: Session = Depends(get_db)):
    """Delete a setting"""
    setting = db.query(Settings).filter(Settings.key == key).first()
    
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    db.delete(setting)
    db.commit()
    
    return {"message": "Setting deleted successfully"}
