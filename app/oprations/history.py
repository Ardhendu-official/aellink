import json
import random
import secrets
import time
import uuid
from datetime import datetime, timedelta
from typing import List

import favicon
import pytz
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbHistory
from app.schemas.index import History


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_new_history(request: History, db: Session = Depends(get_db)):
    name = request.url.split("www.")[-1].split("//")[-1].split(".")[0]        #type:ignore
    image = favicon.get(request.url)
    icon = image[0][0]
    new_hist = DbHistory(
        user_hash_id = request.user_hash_id,
        name = name,
        image = icon,
        url = request.url   
    )
    db.add(new_hist)
    db.commit()
    history = db.query(DbHistory).filter(DbHistory.history_id == new_hist.history_id).first()
    return {"msg": "Done","detalis": history}

def show_history(user_hash_id: str, db: Session = Depends(get_db)):
    history = db.query(DbHistory).filter(DbHistory.user_hash_id == user_hash_id).all()
    return history
