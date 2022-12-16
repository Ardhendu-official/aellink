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
from app.schemas.index import Estimated


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def show_swap_pair(asset: str, db: Session = Depends(get_db)):
    url = 'http://13.234.52.167:2352/api/v1/swap/pair/'
    body = {"name": asset}
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, json=body, headers=headers)
    res = response.json()
    acc = []
    for data in res[:7]:
        url = 'https://api.stealthex.io/api/v2/currency/'+data+'?api_key=61ade498-2c74-48fd-b737-4beebf69dbb9'
        response1 = requests.get(url)
        res1 = response1.json()
        acc.append(res1)
    return acc

def show_swap_trx(db: Session = Depends(get_db)):
    url = 'http://13.234.52.167:2352/api/v1/swap/pair/'
    body = {"name": "trx"}
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, json=body, headers=headers)
    res = response.json()
    acc = []
    for data in res[:7]:
        url = 'https://api.stealthex.io/api/v2/currency/'+data+'?api_key=61ade498-2c74-48fd-b737-4beebf69dbb9'
        response1 = requests.get(url)
        res1 = response1.json()
        acc.append(res1)
    return acc

def show_swap_usdt(db: Session = Depends(get_db)):
    url = 'http://13.234.52.167:2352/api/v1/swap/pair/'
    body = {"name": "usdttrc20"}
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, json=body, headers=headers)
    res = response.json()
    acc = []
    for data in res[:7]:
        url = 'https://api.stealthex.io/api/v2/currency/'+data+'?api_key=61ade498-2c74-48fd-b737-4beebf69dbb9'
        response1 = requests.get(url)
        res1 = response1.json()
        acc.append(res1)
    return acc

def show_swap_curency(asset: str, db: Session = Depends(get_db)):
    url = 'http://13.234.52.167:2352/api/v1/swap/curency/'
    body = {"name": asset}
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, json=body, headers=headers)
    res = response.json()
    return res

def show_swap_curency_all(db: Session = Depends(get_db)):
    url = 'http://13.234.52.167:2352/api/v1/swap/curency/all/'
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    res = response.json()
    return res

def show_swap_estimated(currency_from: str, currency_to: str, amount:str, db: Session = Depends(get_db)):
    url = 'http://13.234.52.167:2352/api/v1/swap/estimated/'
    body = {
        "currency_from": currency_from,
        "currency_to": currency_to,
        "amount": amount
    }
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, json=body, headers=headers)
    res = response.json()
    return res

def show_swap_minimal(currency_from: str, currency_to: str, db: Session = Depends(get_db)):
    url = 'http://13.234.52.167:2352/api/v1/swap/minimal/'
    body = {
        "currency_from": currency_from,
        "currency_to": currency_to
    }
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, json=body, headers=headers)
    res = response.json()
    return res

def show_swap_range(currency_from: str, currency_to: str, db: Session = Depends(get_db)):
    url = 'http://13.234.52.167:2352/api/v1/swap/range/'
    body = {
        "currency_from": currency_from,
        "currency_to": currency_to
    }
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, json=body, headers=headers)
    res = response.json()
    return res