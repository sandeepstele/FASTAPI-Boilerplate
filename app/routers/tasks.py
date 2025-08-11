from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter()


@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[schemas.Task])
def read_tasks(db: Session = Depends(database.get_db)):
    return db.query(models.Task).all()
