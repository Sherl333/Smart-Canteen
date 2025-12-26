from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import customers, items, sales, reports

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Canteen Dashboard")

app.include_router(customers.router)
app.include_router(items.router)
app.include_router(sales.router)
app.include_router(reports.router)
