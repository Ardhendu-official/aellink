from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, HTTPException, Response, responses,
                     status)
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbUser
from app.oprations.index import (create_new_wallet, details_wallet,
                                 details_wallet_bal, import_wallet,
                                 show_user_wallet)
from app.schemas.index import ImportWallet, User, WalletDetails

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

@user.post('/tron/wallet/gen/', status_code=status.HTTP_201_CREATED)
def createWallet(request: User, db: Session = Depends(get_db)):
    return create_new_wallet(request,db)
    

@user.post('/tron/wallet/import/', status_code=status.HTTP_201_CREATED)
def importWallet(request: ImportWallet, db: Session = Depends(get_db)):
    return import_wallet(request, db ) # type: ignore


@user.post('/tron/wallet/details', status_code=status.HTTP_200_OK)
def detailsWallet(request: WalletDetails, db: Session = Depends(get_db)):
    return details_wallet(request, db)  # type: ignore

@user.post('/tron/wallet/balance', status_code=status.HTTP_200_OK)
def detailsWalletBal(request: WalletDetails, db: Session = Depends(get_db)):
    return details_wallet_bal(request, db)  # type: ignore

@user.get('/user/wallet/{hash_id}', status_code=status.HTTP_200_OK)
def Userwallet(hash_id: str, db: Session = Depends(get_db)):
    return show_user_wallet(hash_id ,db)            # type: ignore


# @customer.post('/customer/wallet/addMoney/', status_code=status.HTTP_201_CREATED)
# def custAddMoney(request: CustomerAddMoney, db: Session = Depends(get_db)):
#     return customer_Add_Money(request,db)


# @customer.get('/pincode/finder/{pincode}')
# def all(pincode, db: Session = Depends(get_db)):  # type: ignore
#    return pincode_finder(pincode,db)

