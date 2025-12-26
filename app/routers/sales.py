from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/sales", tags=["Sales"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    total_amount = 0
    sale_items = []

    for item_data in sale.items:
        item = db.query(models.Item).filter(models.Item.id == item_data.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        if item.stock_quantity < item_data.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        subtotal = item.price * item_data.quantity
        total_amount += subtotal

        item.stock_quantity -= item_data.quantity

        sale_items.append({
            "item_id": item.id,
            "quantity": item_data.quantity,
            "price_per_unit": item.price,
            "subtotal": subtotal
        })

    db_sale = models.Sale(customer_id=sale.customer_id, total_amount=total_amount)
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    for si in sale_items:
        db.add(models.SaleItem(sale_id=db_sale.id, **si))

    db.commit()
    return {"sale_id": db_sale.id, "total": total_amount}
