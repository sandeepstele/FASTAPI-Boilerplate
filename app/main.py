from fastapi import FastAPI
from .database import Base, engine
from .routers import tasks, products

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(products.router, prefix="/products", tags=["products"])
