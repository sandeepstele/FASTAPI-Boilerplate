from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, JSON
from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(Text)
    short_description = Column(Text)
    sku = Column(String, unique=True, index=True)
    brand_id = Column(String)
    category_ids = Column(JSON)
    tags = Column(JSON)
    price = Column(Float)
    compare_at_price = Column(Float)
    cost_price = Column(Float)
    weight = Column(Float)
    dimensions = Column(JSON)
    inventory_quantity = Column(Integer)
    inventory_status = Column(String)
    low_stock_threshold = Column(Integer)
    track_inventory = Column(Boolean)
    allow_backorder = Column(Boolean)
    status = Column(String)
    is_featured = Column(Boolean)
    sort_order = Column(Integer)
    meta_title = Column(String)
    meta_description = Column(String)
    attributes = Column(JSON)
    variants = Column(JSON)
    images = Column(JSON)
    additional_data = Column(JSON)
