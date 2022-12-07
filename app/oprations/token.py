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
from app.schemas.index import Assets


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_new_token(request: Assets, db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/contract?contract='+request.token_contect_id    # type: ignore
    response = requests.get(url)  # type: ignore
    data = response.json()
    new_token = DbToken(
        token_name = data["data"][0]['tokenInfo']["tokenName"],
        token_short_name= data["data"][0]['tokenInfo']["tokenAbbr"],
        token_contect_id = data["data"][0]['tokenInfo']["tokenId"],
        token_logo = data["data"][0]['tokenInfo']["tokenLogo"],
        token_type = data["data"][0]['tokenInfo']["tokenType"],
        token_decimal = data["data"][0]['tokenInfo']["tokenDecimal"],
        token_can_show = data["data"][0]['tokenInfo']["tokenCanShow"],
        token_level = data["data"][0]['tokenInfo']["tokenLevel"],
        issuer_addr = data["data"][0]['tokenInfo']["issuerAddr"],
        token_vip = data["data"][0]['tokenInfo']["vip"],
        token_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
    )
    db.add(new_token)
    db.commit()
    token = db.query(DbToken).filter(DbToken.token_id == new_token.token_id).first()
    return token

def create_user_token(request: Assets, db: Session = Depends(get_db)):
    if not request.token_contect_id == "TM4q3gujYR7JUaFrZpM8x1P7NbQd6hwJts" and not request.token_contect_id == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t":
        url = 'https://apilist.tronscan.org/api/contract?contract='+request.token_contect_id    # type: ignore
        response = requests.get(url)  # type: ignore
        data = response.json()
        new_token = DbToken(
            token_name = data["data"][0]['tokenInfo']["tokenName"],
            token_short_name= data["data"][0]['tokenInfo']["tokenAbbr"],
            token_contect_id = data["data"][0]['tokenInfo']["tokenId"],
            token_logo = data["data"][0]['tokenInfo']["tokenLogo"],
            token_type = data["data"][0]['tokenInfo']["tokenType"],
            token_decimal = data["data"][0]['tokenInfo']["tokenDecimal"],
            token_can_show = data["data"][0]['tokenInfo']["tokenCanShow"],
            token_level = data["data"][0]['tokenInfo']["tokenLevel"],
            issuer_addr = data["data"][0]['tokenInfo']["issuerAddr"],
            token_vip = data["data"][0]['tokenInfo']["vip"],
            token_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
        )
        db.add(new_token)
        db.commit()
        user = db.query(DbUser).filter(DbUser.user_address == request.address).first()
        if user.user_token_id == None:             # type: ignore
            token = str(new_token.token_id)
        else:
            token = user.user_token_id+","+str(new_token.token_id)            # type: ignore
        db.query(DbUser).filter(DbUser.user_address == request.address).update({"user_token_id": f'{token}'}, synchronize_session='evaluate')
        db.commit()
        token = db.query(DbToken).filter(DbToken.token_id == new_token.token_id).first()
        return token
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"token already added")

def show_token(address: str,  db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_address == address).first()
    data = []
    ael = {
        "token_contect_id": "TM4q3gujYR7JUaFrZpM8x1P7NbQd6hwJts",
        "token_type": "trc20",
        "issuer_addr": "TKWawHUVd9JABjaTLuQ7XNw5DnchsZMgpi",
        "token_decimal": 8,
        "token_registration_date_time": "2022-11-22T18:28:03",
        "token_short_name": "AEL",
        "token_name": "AELINCE",
        "token_logo": "https://bal-coin.vercel.app/assets/logo/ael_coin.png",
        "token_level": "0",
        "token_vip": 0,
        "token_can_show": 1,
        "token_price": 2
    }
    data.insert(0,ael)
    apikey="3968BDD4-E8D6-4FC0-BE69-8E9D06C558A1"
    url_price= "https://rest.coinapi.io/v1/exchangerate/TRX/USD?apikey="+apikey
    res = requests.get(url_price)
    price_details = res.json()
    if 'rate' in price_details:
        trx = {
            "token_contect_id": "",
            "token_short_name": "TRX",
            "token_type": "trc10",
            "token_decimal": 6,
            "token_name": "tron",
            "token_logo": "https://static.tronscan.org/production/logo/trx.png",
            "token_price": price_details['rate']
        }
        data.insert(1,trx)
    else:
        trx = {
            "token_contect_id": "",
            "token_short_name": "TRX",
            "token_type": "trc10",
            "token_decimal": 6,
            "token_name": "Tron",
            "token_logo": "https://static.tronscan.org/production/logo/trx.png",
            "token_price": 1
        }
        data.insert(1,trx)
    url_price= "https://rest.coinapi.io/v1/exchangerate/USDT/USD?apikey="+apikey
    res = requests.get(url_price)
    price_details = res.json()
    if 'rate' in price_details:
        usdt = {
            "token_contect_id": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
            "token_type": "trc20",
            "issuer_addr": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
            "token_decimal": 6,
            "token_registration_date_time": "2022-11-22T18:27:43",
            "token_short_name": "USDT",
            "token_name": "Tether USD",
            "token_logo": "https://static.tronscan.org/production/logo/usdtlogo.png",
            "token_level": "2",
            "token_vip": 1,
            "token_can_show": 1,
            "token_price": price_details['rate']
        }
        data.insert(2,usdt)
    else:
        usdt = {
            "token_contect_id": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
            "token_type": "trc20",
            "issuer_addr": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
            "token_decimal": 6,
            "token_registration_date_time": "2022-11-22T18:27:43",
            "token_short_name": "USDT",
            "token_name": "Tether USD",
            "token_logo": "https://static.tronscan.org/production/logo/usdtlogo.png",
            "token_level": "2",
            "token_vip": 1,
            "token_can_show": 1,
            "token_price": 1
        }
        data.insert(2,usdt)
    if user.user_token_id:           # type: ignore
        for tkr in user.user_token_id.split(","):                   # type: ignore
            token = db.query(DbToken).filter(DbToken.token_id == tkr).first()
            token_i = token.token_short_name               # type: ignore
            tok = token_i.upper()
            apikey="3968BDD4-E8D6-4FC0-BE69-8E9D06C558A1"
            url_price= "https://rest.coinapi.io/v1/exchangerate/"+tok+"/USD?apikey="+apikey
            res = requests.get(url_price)
            price_details = res.json()
            if 'rate' in price_details:
                token_details = {
                    "token_id": token.token_id,           # type: ignore
                    "token_contect_id": token.token_contect_id,            # type: ignore
                    "token_type": token.token_type,              # type: ignore
                    "issuer_addr": token.issuer_addr,          # type: ignore
                    "token_decimal": token.token_decimal,         # type: ignore
                    "token_registration_date_time": token.token_registration_date_time,     # type: ignore    
                    "token_short_name": token.token_short_name,                # type: ignore
                    "token_name": token.token_name,            # type: ignore
                    "token_logo": token.token_logo,          # type: ignore
                    "token_level": token.token_level,             # type: ignore
                    "token_vip": token.token_vip,                    # type: ignore
                    "token_can_show": token.token_can_show,           # type: ignore
                    "token_price": price_details['rate']
                }
            else:
                token_details = {
                    "token_id": token.token_id,           # type: ignore
                    "token_contect_id": token.token_contect_id,            # type: ignore
                    "token_type": token.token_type,              # type: ignore
                    "issuer_addr": token.issuer_addr,          # type: ignore
                    "token_decimal": token.token_decimal,         # type: ignore
                    "token_registration_date_time": token.token_registration_date_time,     # type: ignore    
                    "token_short_name": token.token_short_name,                # type: ignore
                    "token_name": token.token_name,            # type: ignore
                    "token_logo": token.token_logo,          # type: ignore
                    "token_level": token.token_level,             # type: ignore
                    "token_vip": token.token_vip,                    # type: ignore
                    "token_can_show": token.token_can_show,           # type: ignore 
                    "token_price": 1
                }
            data.append(token_details)
    return data           # type: ignore

def token_all_transaction(address: str, c_address: str, db: Session = Depends(get_db)):
    url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        data.append(dt)
    return data

def token_send_transaction(address: str, c_address:str , db: Session = Depends(get_db)):
    url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["from"] == address:
            data.append(dt)
    return data

def token_receive_transaction(address: str, c_address: str, db: Session = Depends(get_db)):
    url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["to"] == address:
            data.append(dt)
    return data

def trx_all_transaction(address: str, start:str, db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["tokenInfo"]["tokenAbbr"] == "trx":
            if not 'trigger_info' in dt:
                transac = {
                "transaction_id": dt["hash"],
                "token_info": {
                    "symbol": "TRX",
                    "address": "",
                    "decimals": dt["tokenInfo"]["tokenDecimal"],
                    "name": "Tron"
                },
                "block_timestamp": dt["timestamp"],
                "from": dt["contractData"]["owner_address"],
                "to": dt["contractData"]["to_address"],
                "type": "Transfer",
                "value": str(dt["contractData"]["amount"])
                }
                data.append(transac)
    return data

def trx_send_transaction(address: str, start:str , db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["ownerAddress"] == address and dt["tokenInfo"]["tokenAbbr"] == "trx":
            if not 'trigger_info' in dt:
                transac = transac = {
                "transaction_id": dt["hash"],
                "token_info": {
                "symbol": "TRX",
                "address": "",
                "decimals": dt["tokenInfo"]["tokenDecimal"],
                "name": "Tron"
                },
                "block_timestamp": dt["timestamp"],
                "from": dt["contractData"]["owner_address"],
                "to": dt["contractData"]["to_address"],
                "type": "Transfer",
                "value": str(dt["contractData"]["amount"])
                }
                data.append(transac)
    return data

def trx_receive_transaction(address: str, start: str, db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["toAddress"] == address and dt["tokenInfo"]["tokenAbbr"] == "trx":
            if not 'trigger_info' in dt:
                transac = transac = {
                "transaction_id": dt["hash"],
                "token_info": {
                "symbol": "TRX",
                "address": "",
                "decimals": dt["tokenInfo"]["tokenDecimal"],
                "name": "Tron"
                },
                "block_timestamp": dt["timestamp"],
                "from": dt["contractData"]["owner_address"],
                "to": dt["contractData"]["to_address"],
                "type": "Transfer",
                "value": str(dt["contractData"]["amount"])
                }
                data.append(transac)
    return data