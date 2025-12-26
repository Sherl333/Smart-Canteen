from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal
from starlette import status

router = APIRouter(prefix="/items", tags=["Items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", status_code=status.HTTP_200_OK)
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@router.get("/low-stock", status_code=status.HTTP_200_OK)
def low_stock_items(db: Session = Depends(get_db)):
    return db.query(models.Item).filter(
        models.Item.stock_quantity <= models.Item.low_stock_threshold
    ).all()
