from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    
    # Pydantic v2: enable ORM mode
    model_config = ConfigDict(from_attributes=True)


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
    category_ids: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    price: float
    compare_at_price: Optional[float] = None
    cost_price: Optional[float] = None
    weight: Optional[float] = None
    dimensions: Dict[str, float] = Field(default_factory=dict)
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
    attributes: List[Dict[str, str]] = Field(default_factory=list)
    variants: List[Dict[str, Any]] = Field(default_factory=list)
    images: List[Dict[str, Any]] = Field(default_factory=list)
    additional_data: Dict[str, Any] = Field(default_factory=dict)


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    # Pydantic v2: enable ORM mode
    model_config = ConfigDict(from_attributes=True)
