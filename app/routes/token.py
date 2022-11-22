from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbToken
from app.oprations.index import create_new_token, show_token
from app.schemas.index import Assets

token = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@token.post('/token/add', status_code=status.HTTP_201_CREATED)
def createToken(request: Assets, db: Session = Depends(get_db)):
    return create_new_token(request,db)  # type: ignore

@token.get('/token/show', status_code=status.HTTP_200_OK)
def showToken(db: Session = Depends(get_db)):
    return show_token(db)  