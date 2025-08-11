from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..services.ai import generate_action_items, generate_note_fields

router = APIRouter()


@router.post("/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(database.get_db)):
    payload = note.model_dump()
    if (not payload.get("action_items")) and payload.get("description"):
        # Auto-generate action items if not provided
        try:
            ai_items = generate_action_items(payload["description"])
            payload["action_items"] = ai_items
        except Exception:
            # Fail open: if AI fails, proceed without auto items
            payload["action_items"] = payload.get("action_items") or []
    db_note = models.Note(**payload)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.get("/", response_model=List[schemas.Note])
def read_notes(db: Session = Depends(database.get_db)):
    return db.query(models.Note).all()


@router.get("/{note_id}", response_model=schemas.Note)
def read_note(note_id: int, db: Session = Depends(database.get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=schemas.Note)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(database.get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    for key, value in note.model_dump(exclude_unset=True).items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.post("/ai-action-items", response_model=List[str])
def ai_action_items(description: str):
    if not description or not description.strip():
        raise HTTPException(status_code=400, detail="Description is required")
    try:
        return generate_action_items(description)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Failed to generate action items") from exc


@router.post("/ai-note", response_model=schemas.Note, tags=["ai"])
def ai_create_note(payload: schemas.AINoteCreateRequest, db: Session = Depends(database.get_db)):
    if not payload.description or not payload.description.strip():
        raise HTTPException(status_code=400, detail="Description is required")
    try:
        inferred = generate_note_fields(payload.description)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Failed to infer note fields") from exc

    # Coerce to NoteCreate via Pydantic to validate types/formats
    try:
        # If model returns empty date, default to now in UTC-compatible ISO string
        from datetime import datetime, timezone

        if not inferred.get("date"):
            inferred["date"] = datetime.now(timezone.utc).isoformat()

        note_create = schemas.NoteCreate(
            title=inferred.get("title") or "Untitled",
            description=payload.description,
            status=inferred.get("status") or "open",
            date=inferred.get("date"),
            action_items=inferred.get("action_items") or [],
        )
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid fields inferred from description")

    db_note = models.Note(**note_create.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(database.get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"detail": "Note deleted"}
