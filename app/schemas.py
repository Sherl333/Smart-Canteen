from pydantic import BaseModel
from typing import List

class CustomerCreate(BaseModel):
    company_name: str
    contact_person: str
    phone: str
    email: str

class ItemCreate(BaseModel):
    name: str
    price: float
    stock_quantity: int
    low_stock_threshold: int

class SaleItemCreate(BaseModel):
    item_id: int
    quantity: int

class SaleCreate(BaseModel):
    customer_id: int
    items: List[SaleItemCreate]