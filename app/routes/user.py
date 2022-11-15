from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, HTTPException, Response, responses,
                     status)
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbUser
from app.oprations.index import create_new_wallet, import_wallet
from app.schemas.index import ImportWallet, User

user = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @customer.get('/customer/', status_code=status.HTTP_200_OK)
# def allCustomer(db: Session = Depends(get_db)):
#     return show_all_customer(db)

@user.post('/tron/wallet', status_code=status.HTTP_201_CREATED)
def createWallet(request: User, db: Session = Depends(get_db)):
    return create_new_wallet(request,db)
    

@user.post('/tron/wallet/', status_code=status.HTTP_201_CREATED)
def importWallet(request: ImportWallet, db: Session = Depends(get_db)):
    return import_wallet(request, db ) # type: ignore

# @customer.post('/customer/auth', status_code=status.HTTP_201_CREATED)
# def createCustomer(request: ReqCustomer, db: Session = Depends(get_db)):
#     return create_new_customer(request,db)


# @customer.get('/customer/wallet/{phone}', status_code=status.HTTP_200_OK)
# def Customerwallet(phone: int, db: Session = Depends(get_db)):
#     return show_cust_wallet_amount(phone,db)


# @customer.post('/customer/wallet/addMoney/', status_code=status.HTTP_201_CREATED)
# def custAddMoney(request: CustomerAddMoney, db: Session = Depends(get_db)):
#     return customer_Add_Money(request,db)


# @customer.get('/pincode/finder/{pincode}')
# def all(pincode, db: Session = Depends(get_db)):  # type: ignore
#    return pincode_finder(pincode,db)

