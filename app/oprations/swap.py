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
from sqlalchemy import and_, or_
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbSwap, DbToken, DbUser
from app.schemas.index import Exchange


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

def show_swap_minimal(currency_from: str, currency_to: str, amount:str, db: Session = Depends(get_db)):
    url = 'http://13.234.52.167:2352/api/v1/swap/minimal/'
    url_1 = 'http://13.234.52.167:2352/api/v1/swap/estimated/'
    body_1 = {
        "currency_from": currency_from,
        "currency_to": currency_to,
        "amount": amount
    }
    body = {
        "currency_from": currency_from,
        "currency_to": currency_to
    }
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, json=body, headers=headers)
    res = response.json()

    response_1 = requests.get(url_1, json=body_1, headers=headers)
    res_1 = response_1.json()
    data = {
        "min_amount": res["min_amount"],
        "estimated_amount": res_1["estimated_amount"]
    }

    return data

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

def create_swap(request: Exchange ,db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.address_to, DbUser.user_hash_id == request.user_hash_id)).first()
    url_amount = 'http://13.234.52.167:2352/api/v1/swap/minimal/'
    body_amount = {
        "currency_from": request.currency_from,
        "currency_to": request.currency_to
    }
    headers_amount = {'Content-type': 'application/json'}
    response_amount = requests.get(url_amount, json=body_amount, headers=headers_amount)
    res_amount = response_amount.json()
    if user and float(res_amount['min_amount']) <= float(request.amount_from):
        url = 'http://13.234.52.167:2352/api/v1/swap/exchange/create/'
        body = {
            "currency_from": request.currency_from,
            "currency_to": request.currency_to,
            "address_to": request.address_to,
            "amount_from": request.amount_from
        }
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, json=body, headers=headers)
        res = response.json()

        url= 'http://13.234.52.167:2352/api/v1/tron/wallet/send'
        body = {"from_account": request.address_to,
                "to_account": res["address_from"],
                "amount": float(res["expected_amount"])*1000000,
                "privateKey": user.user_privateKey                    # type: ignore
            }
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()

        new_trans = DbSwap(
                transaction_tx_from = res["tx_from"],
                transaction_tx_to = res["tx_to"],
                transaction_tx_id = res["id"],
                transaction_amount_from = res["amount_from"],
                transaction_amount_to = res["amount_to"],
                transaction_status = res["status"],
                trans_to_account = res["address_to"],
                trans_from_account = res["address_from"],
                trans_user_id = request.user_hash_id,
                trans_currency_from = res["currency_from"],
                trans_currency_to = res["currency_to"],
                transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta'))
        )
        db.add(new_trans)
        db.commit()
        trans = db.query(DbSwap).filter(DbSwap.transaction_id == new_trans.transaction_id).first()
        return [res, wallet_details, trans]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"insufficient amount")

def show_swap_trans(user_hash_id: str, user_address: str, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == user_address, DbUser.user_hash_id == user_hash_id)).first()
    trans = db.query(DbSwap).filter(DbSwap.trans_user_id == user_hash_id).all()
    data = []
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                                    detail=f"user not found")
    else:
        for trax in trans:
            if not trax.transaction_status == "finished":
                url = 'http://13.234.52.167:2352/api/v1/swap/exchange/id/'
                body = {
                    "exchange_id": trax.transaction_tx_id
                }
                headers = {'Content-type': 'application/json'}
                response = requests.get(url, json=body, headers=headers)
                res = response.json()
                db.query(DbSwap).filter(DbSwap.transaction_id == trax.transaction_id).update({"transaction_status": f'{res["status"]}', "transaction_tx_from": f'{res["tx_from"]}', "transaction_tx_to": f'{res["tx_to"]}'}, synchronize_session='evaluate')
                db.commit()
                trans_1 = db.query(DbSwap).filter(DbSwap.trans_user_id == user_hash_id).all()
                return trans_1
            else:    
                trans_2 = db.query(DbSwap).filter(DbSwap.trans_user_id == user_hash_id).all()
                return trans_2
