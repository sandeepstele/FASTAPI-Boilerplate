from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    name: str
    slug: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    sku: str
    brand_id: Optional[str] = None
    category_ids: List[str] = []
    tags: List[str] = []
    price: float
    compare_at_price: Optional[float] = None
    cost_price: Optional[float] = None
    weight: Optional[float] = None
    dimensions: Dict[str, float] = {}
    inventory_quantity: int
    inventory_status: str
    low_stock_threshold: Optional[int] = None
    track_inventory: bool = True
    allow_backorder: bool = False
    status: str
    is_featured: bool = False
    sort_order: Optional[int] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    attributes: List[Dict[str, str]] = []
    variants: List[Dict[str, Any]] = []
    images: List[Dict[str, Any]] = []
    additional_data: Dict[str, Any] = {}


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    class Config:
        orm_mode = True
