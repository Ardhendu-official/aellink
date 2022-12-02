from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbToken
from app.oprations.index import create_new_token, show_swap_list
from app.schemas.index import Assets

swap = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @swap.post('/swap', status_code=status.HTTP_201_CREATED)
# def createToken(request: Assets, db: Session = Depends(get_db)):
#     return create_new_token(request,db)  # type: ignore

@swap.get('/swap/list', status_code=status.HTTP_200_OK)
def showSwapList(db: Session = Depends(get_db)):
    return show_swap_list(db)  