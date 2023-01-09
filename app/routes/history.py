from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbHistory
from app.oprations.index import create_new_history, show_history
from app.schemas.index import History

history = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@history.post('/history/add', status_code=status.HTTP_201_CREATED)
def createHistory(request: History, db: Session = Depends(get_db)):
    return create_new_history(request,db)  # type: ignore

@history.get('/history/show/{user_hash_id}', status_code=status.HTTP_200_OK)
def showHistory(user_hash_id: str, db: Session = Depends(get_db)):
    return show_history(user_hash_id, db)  