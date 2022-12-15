from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbToken
from app.oprations.index import (show_swap_curency, show_swap_curency_all,
                                 show_swap_estimated, show_swap_minimal,
                                 show_swap_pair, show_swap_range)
from app.schemas.index import Estimated

swap = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@swap.get('/swap/pair/{asset}', status_code=status.HTTP_200_OK)
def showSwappair(asset: str, db: Session = Depends(get_db)):
    return show_swap_pair(asset, db)

@swap.get('/swap/curency/{asset}', status_code=status.HTTP_200_OK)
def showSwapcurency(asset: str, db: Session = Depends(get_db)):
    return show_swap_curency(asset, db)

@swap.get('/swap/curency/all', status_code=status.HTTP_200_OK)
def showSwapcurencyAll(db: Session = Depends(get_db)):
    return show_swap_curency_all(db)

@swap.get('/swap/estimated/{currency_from}/{currency_to}/{amount}', status_code=status.HTTP_200_OK)
def showSwapEstimated(currency_from: str, currency_to: str, amount:str, db: Session = Depends(get_db)):
    return show_swap_estimated(currency_from, currency_to, amount, db)

@swap.get('/swap/minimal/{currency_from}/{currency_to}', status_code=status.HTTP_200_OK)
def showSwapMinimal(currency_from: str, currency_to: str, db: Session = Depends(get_db)):
    return show_swap_minimal(currency_from, currency_to, db)

@swap.get('/swap/range/{currency_from}/{currency_to}', status_code=status.HTTP_200_OK)
def showSwapRange(currency_from: str, currency_to: str, db: Session = Depends(get_db)):
    return show_swap_range(currency_from, currency_to, db)