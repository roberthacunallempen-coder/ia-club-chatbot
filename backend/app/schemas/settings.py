from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class SettingsBase(BaseModel):
    key: str
    value: Optional[str] = None
    value_json: Optional[Any] = None
    category: Optional[str] = None
    description: Optional[str] = None
    is_secret: bool = False


class SettingsCreate(SettingsBase):
    pass


class SettingsUpdate(BaseModel):
    value: Optional[str] = None
    value_json: Optional[Any] = None
    description: Optional[str] = None


class Settings(SettingsBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
