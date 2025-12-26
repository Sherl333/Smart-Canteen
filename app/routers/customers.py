from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/customers", tags=["Customers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/")
def get_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()
