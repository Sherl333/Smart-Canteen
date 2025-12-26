from pydantic import BaseModel
from typing import List

class CustomerCreate(BaseModel):
    company_name: str
    contact_person: str
    phone: str
    email: str

    model_config = {  
        "json_schema_extra": {
            "example": {
                "company_name": "Acme Corp",
                "contact_person": "John Doe",
                "phone": "123-456-7890",
                "email": "john.doe@acmecorp.com"
            }
        }
    }

class ItemCreate(BaseModel):
    name: str
    price: float
    stock_quantity: int
    low_stock_threshold: int

    model_config = {  
        "json_schema_extra": {
            "example": {
                "name": "laddoo",
                "price": 10.0,
                "stock_quantity": 100,
                "low_stock_threshold": 10
            }
        }
    }

class SaleItemCreate(BaseModel):
    item_id: int
    quantity: int

    model_config = {  
        "json_schema_extra": {
            "example": {
                "item_id": 1,
                "quantity": 5
            }
        }
    }

class SaleCreate(BaseModel):
    customer_id: int
    items: List[SaleItemCreate]

    model_config = {  
        "json_schema_extra": {
            "example": {
                "customer_id": 1,
                "items": [  
                    {
                        "item_id": 1,
                        "quantity": 5
                    }
                ]
            }
        }
    }