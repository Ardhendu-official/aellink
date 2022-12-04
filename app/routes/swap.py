from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbToken
from app.oprations.index import show_swap_list, show_swap_pair, show_swap_value
from app.schemas.index import Assets

swap = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@swap.get('/swap/pair/{asset}', status_code=status.HTTP_200_OK)
def showSwappair(asset: str, db: Session = Depends(get_db)):
    return show_swap_pair(asset, db)    # type: ignore

@swap.get('/swap/list', status_code=status.HTTP_200_OK)
def showSwapList(db: Session = Depends(get_db)):
    return show_swap_list(db)

@swap.get('/swap/value/{frm}/{to}', status_code=status.HTTP_200_OK)
def showSwapvalue(frm: str, to: str, db: Session = Depends(get_db)):
    return show_swap_value(frm, to, db)  