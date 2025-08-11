import os
import logging
from fastapi import FastAPI
from .database import Base, engine
from .routers import notes

tags_metadata = [
    {
        "name": "notes",
        "description": "CRUD operations for Notes (create, list, read, update, delete).",
    },
    {
        "name": "ai",
        "description": "AI-powered helpers like auto-generating action items from a description.",
    },
]

# Basic logging setup; control with LOG_LEVEL env var (e.g., DEBUG, INFO)
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Boilerplate - Notes API",
    description=(
        "A minimal FastAPI server with Notes CRUD and AI-assisted action item generation.\n\n"
        "Use the Swagger UI below to explore the API."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url="/swagger",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "displayRequestDuration": True,
        "defaultModelsExpandDepth": -1,
    },
)

app.include_router(notes.router, prefix="/notes", tags=["notes"])
