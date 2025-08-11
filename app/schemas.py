from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    date: datetime
    action_items: List[str] = Field(default_factory=list)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    date: Optional[datetime] = None
    action_items: Optional[List[str]] = None


class Note(NoteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
