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
from app.models.index import DbToken, DbUser
from app.schemas.index import ImportWallet, User, liveprice, sendTron


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_new_wallet(request: User, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
    token1 = db.query(DbToken).filter(DbToken.token_short_name == "AEL").first()
    token2 = db.query(DbToken).filter(DbToken.token_short_name == "USDT").first()
    url= "http://13.234.52.167:2352/api/v1/tron/account"
    response = requests.post(url)
    wallet_details = response.json()
    hash_id = 'AL'+uuid.uuid1().hex[:8]
    if user:
        new_user = DbUser(
            user_hash_id= request.user_hash_id,
            user_wallet_name = request.user_wallet_name,
            user_password = request.user_password,
            user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
            user_privateKey = wallet_details["account"]["privateKey"],
            user_mnemonic_key = wallet_details["phase"],
            user_address = wallet_details["account"]["address"]
        )
        db.add(new_user)
        db.commit()
        details = db.query(DbUser).filter(DbUser.user_hash_id == new_user.user_hash_id).all()
    else:
        user = DbUser(
            user_hash_id= hash_id,
            user_wallet_name = request.user_wallet_name,
            user_password = request.user_password,
            user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
            user_privateKey = wallet_details["account"]["privateKey"],
            user_mnemonic_key = wallet_details["phase"],
            user_address = wallet_details["account"]["address"],
            # user_token_id = 
        )
        db.add(user)
        db.commit()
        details = db.query(DbUser).filter(DbUser.user_hash_id == user.user_hash_id).all()
    return details

def import_wallet(request: ImportWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
    mnemonic_key = ismnemonickey(request.m_key_or_p_key)
    if mnemonic_key["status"] == True:
        list = db.query(DbUser).filter(DbUser.user_mnemonic_key == request.m_key_or_p_key).first()
        if not list:
            url= "http://13.234.52.167:2352/api/v1/tron/wallet/import/phase"
            body = {"phase": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        else:
            return "mnemonic key already added"
    else:
        list = db.query(DbUser).filter(DbUser.user_privateKey == request.m_key_or_p_key).first()
        if not list:
            url= "http://13.234.52.167:2352/api/v1/tron/wallet/import/private"
            body = {"pkey": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        else:
            return "private key already added"
    hash_id = 'AL'+uuid.uuid1().hex[:8]
    if user:
        user = DbUser(
            user_hash_id=request.user_hash_id,
            user_wallet_name = request.user_wallet_name,
            user_password = request.user_password,
            user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
            user_privateKey = wallet_details["privateKey"],
            user_mnemonic_key = request.m_key_or_p_key,
            user_address =  wallet_details["address"]
        )
        db.add(user)
        db.commit()
        details = user = db.query(DbUser).filter(DbUser.user_id == user.user_id).first()  # type: ignore
    else:
        new_user = DbUser(
            user_hash_id=hash_id,
            user_wallet_name = request.user_wallet_name,
            user_password = request.user_password,
            user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
            user_privateKey = wallet_details["privateKey"],
            user_mnemonic_key = request.m_key_or_p_key,
            user_address = wallet_details["address"]
        )
        db.add(new_user)
        db.commit()
        details = user = db.query(DbUser).filter(DbUser.user_id == new_user.user_id).first()
    return details
    
def details_wallet(request: ImportWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
    url= "http://13.234.52.167:2352/api/v1/tron/wallet/details"
    body = {"address": request.user_address}           # type: ignore
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    return wallet_details

def details_wallet_bal(request: ImportWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
    url= "http://13.234.52.167:2352/api/v1/tron/wallet/balance"
    body = {"address": request.user_address}           # type: ignore
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    return wallet_details

def show_user_wallet(hash_id: str , db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == hash_id).all()
    return user

def send_trx(request: sendTron, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_address == request.from_account).first()
    url= "http://13.234.52.167:2352/api/v1/tron//wallet/send"
    body = {"from_account": request.from_account,
            "to_account": request.to_account,
            "amount": request.amount,
            "privateKey": user.user_privateKey
        }           
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    return wallet_details




def ismnemonickey(mkey):  # type: ignore
    url= "http://13.234.52.167:2352/api/v1/tron/isphase"
    body = {"phase": mkey}
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    return wallet_details
