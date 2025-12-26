from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/items", tags=["Items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/")
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@router.get("/low-stock")
def low_stock_items(db: Session = Depends(get_db)):
    return db.query(models.Item).filter(
        models.Item.stock_quantity <= models.Item.low_stock_threshold
    ).all()
