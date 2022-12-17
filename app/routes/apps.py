from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.oprations.index import show_app

apps = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@apps.get('/app/details', status_code=status.HTTP_200_OK)
def showBanner(db: Session = Depends(get_db)):
    return show_app(db)  