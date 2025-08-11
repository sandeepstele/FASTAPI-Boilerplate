from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from .database import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    action_items = Column(JSON, default=list)
