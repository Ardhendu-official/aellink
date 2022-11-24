import json
import random
import secrets
import time
import urllib.request
import uuid
from datetime import datetime, timedelta
from operator import or_
from typing import List

import pytz
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbToken, DbTrxTransaction, DbUser
from app.schemas.index import ImportWallet, User, liveprice, sendTron


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_new_wallet(request: User, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
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
    mnemonic_key = ismnemonickey(request.m_key_or_p_key)             # type: ignore
    if mnemonic_key["status"] == True:
        list = db.query(DbUser).filter(DbUser.user_mnemonic_key == request.m_key_or_p_key).first()
        if not list:                 # type: ignore
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
    if user:    # type: ignore
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
    url= 'http://13.234.52.167:2352/api/v1/tron//wallet/send'
    body = {"from_account": request.from_account,
            "to_account": request.to_account,
            "amount": request.amount,
            "privateKey": user.user_privateKey                    # type: ignore
        }           
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
  
    amount = wallet_details['transaction']['raw_data']['contract'][0]['parameter']['value']['amount']
    new_trans = DbTrxTransaction(
            transaction_tx_id = wallet_details['txid'],
            transaction_amount = amount/1000000,
            trans_from_account = request.from_account,
            trans_to_account = request.to_account,
            trans_user_id = request.user_hash_id,
            transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta')),
        )
    db.add(new_trans)
    db.commit()
    trans = db.query(DbTrxTransaction).filter(DbTrxTransaction.transaction_id == new_trans.transaction_id).first()
    return trans


# def get_details(hash: str):
# data = str(wallet_details['txid'])
# data = "f5e7505f87631a0b4c4714d13825a66368ad2bb8df65d2179cea9414c7df78ed"
# url_trx = str('https://apilist.tronscan.org/api/transaction-info?hash=' + str(wallet_details['transaction']['txID']))  
# hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36', 'Content-type': 'application/json', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive'}           # type: ignore
# response_trx = get_details(str(wallet_details['transaction']['txID']))  # type: ignore
# trx_details = response_trx
#     url_trx_bal = str('https://apilist.tronscan.org/api/transaction-info?hash=' + hash)  
#     hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36', 'Content-type': 'application/json', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive'}           # type: ignore
#     try: 
#         response_trx = requests.get(url_trx_bal, headers=hdr).json()  # type: ignore
#         print(jsonable_encoder(response_trx))
#         print('lol')
#     except:
#         response_trx = {}
#         print('bal')
#     return response_trx

def show_all_transaction(address: str , db: Session = Depends(get_db)):
    trans = db.query(DbTrxTransaction).filter(or_(DbTrxTransaction.trans_from_account == address, DbTrxTransaction.trans_to_account == address)).order_by(
        DbTrxTransaction.transaction_date_time.desc()).all()
    if not trans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no transaction detalis found")
    else: 
        return trans

def show_send_transaction(address: str , db: Session = Depends(get_db)):
    trans = db.query(DbTrxTransaction).filter(DbTrxTransaction.trans_from_account == address).order_by(
        DbTrxTransaction.transaction_date_time.desc()).all()
    if not trans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no transaction detalis found")
    else: 
        return trans

def show_receive_transaction(address: str , db: Session = Depends(get_db)):
    trans = db.query(DbTrxTransaction).filter(DbTrxTransaction.trans_to_account == address).order_by(
        DbTrxTransaction.transaction_date_time.desc()).all()
    if not trans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no transaction detalis found")
    else: 
        return trans

def ismnemonickey(mkey):  # type: ignore
    url= "http://13.234.52.167:2352/api/v1/tron/isphase"
    body = {"phase": mkey}
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    return wallet_details
