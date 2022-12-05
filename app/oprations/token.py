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

def show_token(db: Session = Depends(get_db)):
    token = db.query(DbToken).all()
    data = []
    for value in token:                   # type: ignore
        token_i = value.token_short_name
        tok = token_i.upper()
        if tok == "AEL":
            token_details = {
                "token_id": value.token_id,
                "token_contect_id": value.token_contect_id,
                "token_type": value.token_type,
                "issuer_addr": value.issuer_addr,
                "token_decimal": value.token_decimal,
                "token_registration_date_time": value.token_registration_date_time,
                "token_short_name": value.token_short_name,
                "token_name": value.token_name,
                "token_logo": value.token_logo,
                "token_level": value.token_level,
                "token_vip": value.token_vip,  
                "token_can_show": value.token_can_show,  
                "token_price": 2
            }
        else:
            apikey="3968BDD4-E8D6-4FC0-BE69-8E9D06C558A1"
            url_price= "https://rest.coinapi.io/v1/exchangerate/"+tok+"/USD?apikey="+apikey
            res = requests.get(url_price)
            price_details = res.json()
            if 'rate' in price_details:
                token_details = {
                    "token_id": value.token_id,
                    "token_contect_id": value.token_contect_id,
                    "token_type": value.token_type,
                    "issuer_addr": value.issuer_addr,
                    "token_decimal": value.token_decimal,
                    "token_registration_date_time": value.token_registration_date_time,
                    "token_short_name": value.token_short_name,
                    "token_name": value.token_name,
                    "token_logo": value.token_logo,
                    "token_level": value.token_level,
                    "token_vip": value.token_vip,  
                    "token_can_show": value.token_can_show,  
                    "token_price": price_details['rate']
                }
            else:
                token_details = {
                    "token_id": value.token_id,
                    "token_contect_id": value.token_contect_id,
                    "token_type": value.token_type,
                    "issuer_addr": value.issuer_addr,
                    "token_decimal": value.token_decimal,
                    "token_registration_date_time": value.token_registration_date_time,
                    "token_short_name": value.token_short_name,
                    "token_name": value.token_name,
                    "token_logo": value.token_logo,
                    "token_level": value.token_level,
                    "token_vip": value.token_vip,  
                    "token_can_show": value.token_can_show,  
                    "token_price": 1
                }
        data.append(token_details)
    return data               # type: ignore