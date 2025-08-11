from fastapi import FastAPI
from .database import Base, engine
from .routers import notes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(notes.router, prefix="/notes", tags=["notes"])
