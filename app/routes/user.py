from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbUser
from app.oprations.index import (backup_wallet_phase, backup_wallet_private,
                                 change_pass, create_new_wallet,
                                 details_wallet, details_wallet_bal,
                                 import_wallet, send_trx, show_all_transaction,
                                 show_note_transaction,
                                 show_receive_transaction,
                                 show_send_transaction, show_user_wallet,
                                 varify_pass, wallet_delete, wallet_update)
from app.schemas.index import (ImportWallet, User, WalletDetails, deleteWallet,
                               liveprice, passChange, passVarify, sendTron,
                               updateWallet)

user = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user.post('/tron/wallet/gen', status_code=status.HTTP_201_CREATED)
def createWallet(request: User, db: Session = Depends(get_db)):
    return create_new_wallet(request,db)
    
@user.post('/tron/wallet/import', status_code=status.HTTP_201_CREATED)
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
    return show_user_wallet(hash_id, db)           

@user.post('/tron/send', status_code=status.HTTP_200_OK)
def sendTrx(request: sendTron, db: Session = Depends(get_db)):  
    return send_trx(request, db)  

@user.get('/transaction/all/{address}/{start}', status_code=status.HTTP_200_OK)
def transactionAll(address: str, start:str, db: Session = Depends(get_db)):
    return show_all_transaction(address, start, db)  

@user.get('/transaction/send/{address}/{start}', status_code=status.HTTP_200_OK)
def transactionSend(address: str, start:str, db: Session = Depends(get_db)):
    return show_send_transaction(address, start, db)  

@user.get('/transaction/receive/{address}/{start}', status_code=status.HTTP_200_OK)
def transactionReceive(address: str, start:str, db: Session = Depends(get_db)):
    return show_receive_transaction(address, start, db)  

@user.get('/transaction/note/{address}/{start}', status_code=status.HTTP_200_OK)
def transactionNote(address: str, start:str, db: Session = Depends(get_db)):
    return show_note_transaction(address, start, db) 

@user.post('/verify/pass', status_code=status.HTTP_200_OK)
def varifyPass(request: passVarify, db: Session = Depends(get_db)):  
    return varify_pass(request, db)  

@user.post('/change/pass', status_code=status.HTTP_202_ACCEPTED)
def changePass(request: passChange, db: Session = Depends(get_db)):  
    return change_pass(request, db)

@user.post('/wallet/update', status_code=status.HTTP_202_ACCEPTED)
def walletUpdate(request: updateWallet, db: Session = Depends(get_db)):  
    return wallet_update(request, db)

@user.post('/wallet/backup', status_code=status.HTTP_200_OK)
def WalletBackup(request: WalletDetails, db: Session = Depends(get_db)):
    return backup_wallet_private(request, db)  # type: ignore

@user.post('/wallet/backup/phase', status_code=status.HTTP_200_OK)
def WalletBackupPhase(request: WalletDetails, db: Session = Depends(get_db)):
    return backup_wallet_phase(request, db)  # type: ignore

@user.post('/wallet/delete', status_code=status.HTTP_202_ACCEPTED)
def walletDelete(request: deleteWallet, db: Session = Depends(get_db)):  
    return wallet_delete(request, db)