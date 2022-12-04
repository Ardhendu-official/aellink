import json
import random
import secrets
import time
import uuid
from datetime import datetime, timedelta
from typing import List

import pytz
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbToken
from app.schemas.index import Assets


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def show_swap_pair(asset: str, db: Session = Depends(get_db)):
    url = 'https://list.justswap.link/justswap.json'
    response = requests.get(url)
    res = response.json()
    trx = {
      "symbol": "TRX",
      "decimals": 6,
      "name": "tron",
      "logoURI": "https://static.tronscan.org/production/logo/trx.png"
    }
    data = res["tokens"]
    data.insert(0,trx)
    ass = []
    for index, tok in enumerate(data):
        if data[index]["symbol"] == asset:
                data.pop(index)
    return data

def show_swap_list(db: Session = Depends(get_db)):
    url = 'https://list.justswap.link/justswap.json'
    response = requests.get(url)
    res = response.json()
    trx = {
      "symbol": "TRX",
      "decimals": 6,
      "name": "tron",
      "logoURI": "https://static.tronscan.org/production/logo/trx.png"
    }
    data = res["tokens"]
    data.insert(0,trx)
    return data

def show_swap_value(frm: str, to: str, db: Session = Depends(get_db)):
    apikey="3968BDD4-E8D6-4FC0-BE69-8E9D06C558A1"
    url_price= "https://rest.coinapi.io/v1/exchangerate/"+frm+"/"+to+"?apikey="+apikey
    res = requests.get(url_price)
    price_details = res.json()
    return price_details