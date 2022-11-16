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
from app.models.index import DbUser
from app.schemas.index import ImportWallet, User

category = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_new_wallet(request: User, db: Session = Depends(get_db)):
    hash_id = 'AL'+uuid.uuid1().hex[:8]
    url= "http://65.2.7.120:2352/api/v1/tron/account"
    # url= "http://192.168.0.140:2352/api/v1/tron/account"
    response = requests.post(url)
    wallet_details = response.json()
    new_user = DbUser(
        user_hash_id=hash_id,
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
    return details

# def import_wallet(request: ImportWallet, db: Session = Depends(get_db)):
#     user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
#     url= "http://192.168.0.140:2352/api/v1/tron/wallet"
#     response = requests.post(url)
#     wallet_details = response.json()
#     if user:
#         user = DbUser(
#             user_hash_id=request.user_hash_id,
#             user_wallet_name = request.user_wallet_name,
#             user_password = request.user_password,
#             user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
#             user_publicKey = wallet_details["publicKey"],
#             user_privateKey = wallet_details["privateKey"],
#             user_mnemonic_key = wallet_details["mnemonic"]["phrase"],
#             user_address =  wallet_details["address"]
#         )
#     db.add(user)
#     db.commit()

#     details = db.query(DbUser).filter(DbUser.user_hash_id == new_user.user_hash_id).all()
#     return details
