from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbToken
from app.oprations.index import (create_new_token, create_user_token,
                                 show_token, token_all_transaction,
                                 token_receive_transaction,
                                 token_send_transaction, trx_all_transaction,
                                 trx_receive_transaction, trx_send_transaction)
from app.schemas.index import Assets

token = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@token.post('/token/add', status_code=status.HTTP_201_CREATED)
def createToken(request: Assets, db: Session = Depends(get_db)):
    return create_new_token(request,db)  # type: ignore

@token.get('/token/show/{address}', status_code=status.HTTP_200_OK)
def showToken(address: str, db: Session = Depends(get_db)):
    return show_token(address, db)    # type: ignore

@token.post('/token/add/user', status_code=status.HTTP_201_CREATED)
def createUserToken(request: Assets, db: Session = Depends(get_db)):
    return create_user_token(request,db)

@token.get('/token/transaction/all/{address}/{c_address}', status_code=status.HTTP_200_OK)
def transactionAll(address: str, c_address:str, db: Session = Depends(get_db)):
    return token_all_transaction(address, c_address, db)  

@token.get('/token/transaction/send/{address}/{c_address}', status_code=status.HTTP_200_OK)
def transactionSend(address: str, c_address:str, db: Session = Depends(get_db)):
    return token_send_transaction(address, c_address, db)  

@token.get('/token/transaction/receive/{address}/{c_address}', status_code=status.HTTP_200_OK)
def transactionReceive(address: str, c_address:str, db: Session = Depends(get_db)):
    return token_receive_transaction(address, c_address, db) 

@token.get('/trx/transaction/all/{address}/{start}', status_code=status.HTTP_200_OK)
def transactionTrxAll(address: str, start:str, db: Session = Depends(get_db)):
    return trx_all_transaction(address, start, db)  

@token.get('/trx/transaction/send/{address}/{start}', status_code=status.HTTP_200_OK)
def transactionTrxSend(address: str, start:str, db: Session = Depends(get_db)):
    return trx_send_transaction(address, start, db)  

@token.get('/trx/transaction/receive/{address}/{start}', status_code=status.HTTP_200_OK)
def transactionTrxReceive(address: str, start:str, db: Session = Depends(get_db)):
    return trx_receive_transaction(address, start, db) 