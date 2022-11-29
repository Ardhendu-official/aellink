import uuid
from datetime import datetime
from typing import List

import pytz
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.functions.index import Hash, HashVerify
from app.models.index import DbToken, DbTrxTransaction, DbUser
from app.schemas.index import (ImportWallet, User, liveprice, passVarify,
                               sendTron)


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
            user_password = Hash.bcrypt(request.user_password),  # type: ignore
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
            user_password = Hash.bcrypt(request.user_password),  # type: ignore
            user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
            user_privateKey = wallet_details["account"]["privateKey"],
            user_mnemonic_key = wallet_details["phase"],
            user_address = wallet_details["account"]["address"],
        )
        db.add(user)
        db.commit()
        details = db.query(DbUser).filter(DbUser.user_hash_id == user.user_hash_id).all()
    return details

def import_wallet(request: ImportWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).all()
    mnemonic_key = ismnemonickey(request.m_key_or_p_key) 
    url= "http://13.234.52.167:2352/api/v1/tron/wallet/import/phase"
    body = {"phase": request.m_key_or_p_key}
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    for u_detalis in user:
        if u_detalis.user_address == wallet_details["address"]:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"address already added") 
        else:
            if mnemonic_key["status"] == True:
                url= "http://13.234.52.167:2352/api/v1/tron/wallet/import/phase"
                body = {"phase": request.m_key_or_p_key}
                headers = {'Content-type': 'application/json'}
                response = requests.post(url,json=body,headers=headers)
                wallet_details = response.json()
            else:
                url= "http://13.234.52.167:2352/api/v1/tron/wallet/import/private"
                body = {"pkey": request.m_key_or_p_key}
                headers = {'Content-type': 'application/json'}
                response = requests.post(url,json=body,headers=headers)
                wallet_details = response.json()
    hash_id = 'AL'+uuid.uuid1().hex[:8]
    if user:
        if wallet_details:    # type: ignore
            user = DbUser(
                user_hash_id=request.user_hash_id,
                user_wallet_name = request.user_wallet_name,
                user_password = Hash.bcrypt(request.user_password),  # type: ignore
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
                user_privateKey = wallet_details["privateKey"],
                user_mnemonic_key = request.m_key_or_p_key,
                user_address =  wallet_details["address"]
            )
            db.add(user)
            db.commit()
            details_add = user = db.query(DbUser).filter(DbUser.user_id == user.user_id).first()  # type: ignore
    else:
        new_user = DbUser(
            user_hash_id=hash_id,
            user_wallet_name = request.user_wallet_name,
            user_password = Hash.bcrypt(request.user_password),  # type: ignore
            user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
            user_privateKey = wallet_details["privateKey"],
            user_mnemonic_key = request.m_key_or_p_key,
            user_address = wallet_details["address"]
        )
        db.add(new_user)
        db.commit()
        details_add = user = db.query(DbUser).filter(DbUser.user_id == new_user.user_id).first()
    return details_add                    # type: ignore
    
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
    data = []
    for u_detalis in user:
        url= "http://13.234.52.167:2352/api/v1/tron/wallet/details"
        body = {"address": u_detalis.user_address}           # type: ignore
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()
        balance = wallet_details["balance"] + wallet_details["totalFrozen"]
        dtl = {
            "user_privateKey": u_detalis.user_privateKey,
            "user_mnemonic_key": u_detalis.user_mnemonic_key,
            "user_wallet_name": u_detalis.user_wallet_name,
            "user_hash_id": u_detalis.user_hash_id,
            "user_address": u_detalis.user_address,
            "user_registration_date_time": u_detalis.user_registration_date_time,
            "token_balance": balance/1000000
        }
        data.append(dtl)
    return data

def send_trx(request: sendTron, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_address == request.from_account).first()
    if HashVerify.bcrypt_verify(request.password, user.user_password):                 # type: ignore  
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
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"worng password")

def show_all_transaction(address: str, start:str, db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        transac = {
        "transaction_tx_id": dt["hash"],
        "transaction_contract": dt["contractData"],
        "transaction_date_time": dt["timestamp"],
        "transaction_status": dt["confirmed"]
        }
        data.append(transac)
    return [reacharge_responce["total"], data]

def show_send_transaction(address: str, start:str , db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["ownerAddress"] == address:
            transac = {
            "transaction_tx_id": dt["hash"],
            "transaction_contract": dt["contractData"],
            "transaction_date_time": dt["timestamp"],
            "transaction_status": dt["confirmed"]
            }
            data.append(transac)
    return [reacharge_responce["total"], data]

def show_receive_transaction(address: str, start: str, db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["toAddress"] == address:
            transac = {
            "transaction_tx_id": dt["hash"],
            "transaction_contract": dt["contractData"],
            "transaction_date_time": dt["timestamp"],
            "transaction_status": dt["confirmed"]
            }
            data.append(transac)
    return [reacharge_responce["total"], data]

def varify_pass(request: passVarify, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_address == request.user_address).first()
    if HashVerify.bcrypt_verify(request.password, user.user_password):                 # type: ignore  
       raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"correct password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"incorrect password")






def ismnemonickey(mkey):  # type: ignore
    url= "http://13.234.52.167:2352/api/v1/tron/isphase"
    body = {"phase": mkey}
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    return wallet_details
