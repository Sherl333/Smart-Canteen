from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from sqlalchemy import func


router = APIRouter(prefix="/reports", tags=["Reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/invoice/{sale_id}")
def get_invoice(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    items = db.query(models.SaleItem).filter(models.SaleItem.sale_id == sale_id).all()

    return {
        "invoice_number": f"INV-{sale.id}",
        "customer_id": sale.customer_id,
        "items": items,
        "total": sale.total_amount
    }

@router.get("/monthly-sales")
def monthly_sales(month: int, year: int, db: Session = Depends(get_db)):
    month_str = f"{month:02d}"

    total_sales = db.query(
        func.count(models.Sale.id),
        func.sum(models.Sale.total_amount)
    ).filter(
        func.strftime("%m", models.Sale.sale_date) == month_str,
        func.strftime("%Y", models.Sale.sale_date) == str(year)
    ).first()

    return {
        "month": month,
        "year": year,
        "total_sales": total_sales[0],
        "total_revenue": total_sales[1] or 0
    }

@router.get("/total-revenue")
def total_revenue(db: Session = Depends(get_db)):
    revenue = db.query(func.sum(models.Sale.total_amount)).scalar()
    return {"total_revenue": revenue or 0}

@router.get("/top-items")
def top_selling_items(db: Session = Depends(get_db)):
    results = db.query(
        models.Item.name,
        func.sum(models.SaleItem.quantity).label("total_quantity")
    ).join(
        models.SaleItem, models.Item.id == models.SaleItem.item_id
    ).group_by(
        models.Item.name
    ).order_by(
        func.sum(models.SaleItem.quantity).desc()
    ).all()

    return [
        {"item_name": r[0], "quantity_sold": r[1]}
        for r in results
    ]

