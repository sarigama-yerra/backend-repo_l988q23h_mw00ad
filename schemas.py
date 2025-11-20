"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (kept for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# RTU Canteen app schemas

class MenuItem(BaseModel):
    """
    Canteen menu items
    Collection name: "menuitem"
    """
    name: str = Field(..., description="Item name")
    category: str = Field(..., description="Category e.g., Beverages, Fast Food")
    price: float = Field(..., ge=0, description="Price in INR")
    description: Optional[str] = Field(None, description="Short description")
    image_url: Optional[str] = Field(None, description="Image URL")
    is_available: bool = Field(True, description="Whether item is available 24x7")

class OrderItem(BaseModel):
    item_id: str = Field(..., description="Menu item id")
    name: str
    qty: int = Field(..., ge=1)
    price: float = Field(..., ge=0)

class Order(BaseModel):
    """
    Orders placed by students staying in RTU hostels
    Collection name: "order"
    """
    customer_name: str
    phone: str
    hostel: str = Field(..., description="Hostel name")
    room: str = Field(..., description="Room number")
    delivery_instructions: Optional[str] = None
    items: List[OrderItem]
    total_amount: float = Field(..., ge=0)
    status: str = Field("pending", description="pending | confirmed | out_for_delivery | delivered | cancelled")
