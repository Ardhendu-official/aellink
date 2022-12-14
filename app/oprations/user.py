import json
import uuid
from datetime import datetime
from typing import List

import pytz
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.functions.index import Hash, HashVerify
from app.models.index import (DbAdmin, DbFeesTransaction, DbToken,
                              DbTrxTransaction, DbUser)
from app.schemas.index import (ImportWallet, User, WalletDetails, deleteWallet,
                               liveprice, passChange, passVarify, sendTron,
                               updateWallet)


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
            user_address = wallet_details["account"]["address"],
            user_show = "true"
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
            user_show = "true"
        )
        db.add(user)
        db.commit()
        details = db.query(DbUser).filter(DbUser.user_hash_id == user.user_hash_id).all()
    return details

def import_wallet(request: ImportWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).all()
    mnemonic_key = ismnemonickey(request.m_key_or_p_key) 
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
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),  # type: ignore
                user_privateKey = wallet_details["privateKey"],
                user_mnemonic_key = request.m_key_or_p_key,
                user_address =  wallet_details["address"],
                user_show = "true"
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
            user_privateKey = wallet_details["privateKey"],   # type: ignore
            user_mnemonic_key = request.m_key_or_p_key, 
            user_address = wallet_details["address"],   # type: ignore
            user_show = "true"
        )
        db.add(new_user)
        db.commit()
        details_add = user = db.query(DbUser).filter(DbUser.user_id == new_user.user_id).first()
    return details_add                    # type: ignore
    
def details_wallet(request: WalletDetails, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
    url= "http://13.234.52.167:2352/api/v1/tron/wallet/details"
    body = {"address": request.user_address}           # type: ignore
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    data = []
    for value in wallet_details['tokens']:
        token_id = value['tokenAbbr']
        token = token_id.upper()
        if token == "AEL":
            price_details = {
                "asset_id_base": "AEL",
                "asset_id_quote": "USD",
                "rate": 2.00
            }
        else:
            apikey="3968BDD4-E8D6-4FC0-BE69-8E9D06C558A1"
            url_price= "https://rest.coinapi.io/v1/exchangerate/"+token+"/USD?apikey="+apikey
            res = requests.get(url_price)
            price_details = res.json()
            if 'rate' in price_details:
                price_details = {
                    "time": price_details['time'],
                    "asset_id_base": token,
                    "asset_id_quote": "USD",
                    "rate": price_details['rate']
                }
            else:
                price_details = {
                    "time": "2022-12-05T17:18:56.0000000Z",
                    "asset_id_base": token,
                    "asset_id_quote": "USD",
                    "rate": 1
                }
        data.append(price_details)
    return [wallet_details, data]

def details_wallet_bal(request: ImportWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
    url= "http://13.234.52.167:2352/api/v1/tron/wallet/balance"
    body = {"address": request.user_address}           # type: ignore
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    data = []
    for amount in wallet_details['details']:                   
        bal = int(amount['balance']) / 10** amount['tokenDecimal']
        value = {
            "address": request.user_address,            # type: ignore
            "token": amount['tokenAbbr'],
            "token_amount": bal                               
        }
        data.append(value)
    return data

def show_user_wallet(hash_id: str , db: Session = Depends(get_db)):
    # user = db.query(DbUser).filter(DbUser.user_hash_id == hash_id).all()
    user = db.query(DbUser).filter(and_(DbUser.user_hash_id == hash_id, DbUser.user_show == "true")).all()
    data = []
    if user:
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
                "token_balance": balance/1000000, 
                "user_show": u_detalis.user_show
            }
            data.append(dtl)
        return data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user not found")

def send_trx(request: sendTron, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.from_account, DbUser.user_hash_id == request.user_hash_id)).first()
    if user and request.amount >= 10000:
        url= 'http://13.234.52.167:2352/api/v1/tron/wallet/send'
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
        body_fee = {
            "from_account": request.from_account,
            "to_account": "TKWawHUVd9JABjaTLuQ7XNw5DnchsZMgpi",
            "amount": request.amount * 0.01/100,
            "privateKey": user.user_privateKey                    # type: ignore
            }
        res = requests.post(url,json=body_fee,headers=headers)
        fees_details = res.json()
        amount_fee = fees_details['transaction']['raw_data']['contract'][0]['parameter']['value']['amount']
        new_fee_trans = DbFeesTransaction(
                transaction_tx_id = fees_details['txid'],
                transaction_amount = amount_fee/1000000,
                trans_from_account = request.from_account,
                trans_user_id = request.user_hash_id,
                transaction_status = fees_details['result'],
                transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta')),
            )
        db.add(new_fee_trans)
        db.commit()
        amo = db.query(DbAdmin).first()
        amo_amount = amo.admin_comission + amount_fee/1000000                     # type: ignore
        db.query(DbAdmin).update({"admin_comission": f'{amo_amount}'}, synchronize_session='evaluate')
        db.commit()
        trans_fee = db.query(DbFeesTransaction).filter(DbFeesTransaction.transaction_id == new_fee_trans.transaction_id).first()
        trans = db.query(DbTrxTransaction).filter(DbTrxTransaction.transaction_id == new_trans.transaction_id).first()
        return [trans, trans_fee]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"amount is to low")

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
        "transaction_status": dt["confirmed"],
        "token_decimal": dt["tokenInfo"]["tokenDecimal"]

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
            "transaction_status": dt["confirmed"],
            "token_decimal": dt["tokenInfo"]["tokenDecimal"]
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
            "transaction_status": dt["confirmed"],
            "token_decimal": dt["tokenInfo"]["tokenDecimal"]
            }
            data.append(transac)
    return [reacharge_responce["total"], data]

def show_note_transaction(address: str, start:str , db: Session = Depends(get_db)):
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
            "transaction_status": dt["confirmed"],
            "token_decimal": dt["tokenInfo"]["tokenDecimal"],
            "transaction_state": "send"
            }
        elif dt["toAddress"] == address:
            transac = {
            "transaction_tx_id": dt["hash"],
            "transaction_contract": dt["contractData"],
            "transaction_date_time": dt["timestamp"],
            "transaction_status": dt["confirmed"],
            "token_decimal": dt["tokenInfo"]["tokenDecimal"],
            "transaction_state": "receive"
            }
        data.append(transac)   # type: ignore
    return [reacharge_responce["total"], data]    

def varify_pass(request: passVarify, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"user not found")
    else:
        if HashVerify.bcrypt_verify(request.password, user.user_password):                 # type: ignore  
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"correct password")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"incorrect password")

def change_pass(request: passChange, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"user not found")
    else:
        if HashVerify.bcrypt_verify(request.password, user.user_password):                 # type: ignore  
            password = Hash.bcrypt(request.new_password)  # type: ignore
            db.query(DbUser).filter(DbUser.user_address == request.user_address).update({"user_password": f'{password}'}, synchronize_session='evaluate')
            db.commit()
            return {"msg": "password update done"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"incorrect password")

def wallet_update(request: updateWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"user not found")
    else:    
        db.query(DbUser).filter(DbUser.user_address == request.user_address).update({"user_wallet_name": f'{request.user_wallet_name}'}, synchronize_session='evaluate')
        db.commit()
        user = db.query(DbUser).filter(DbUser.user_address == request.user_address).first()
        return {"msg": "update done", "detalis": user}

def backup_wallet_private(request: WalletDetails, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    private = {
        "address": user.user_address,  # type: ignore
        "private_key": user.user_privateKey      # type: ignore
    }
    return private

def backup_wallet_phase(request: WalletDetails, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    phase = {
        "address": user.user_address,  # type: ignore
        "private_key": user.user_mnemonic_key      # type: ignore
    }
    return phase

def wallet_delete(request: deleteWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"user not found")
    else:    
        db.query(DbUser).filter(DbUser.user_address == request.user_address).update({"user_show": f'{"false"}'}, synchronize_session='evaluate')
        db.commit()
        user = db.query(DbUser).filter(DbUser.user_address == request.user_address).first()
        return {"msg": "delete done", "detalis": user}









def ismnemonickey(mkey):  # type: ignore
    url= "http://13.234.52.167:2352/api/v1/tron/isphase"
    body = {"phase": mkey}
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    return wallet_details
