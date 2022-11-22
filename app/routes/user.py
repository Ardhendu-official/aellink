from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbUser
from app.oprations.index import (create_new_wallet, details_wallet,
                                 details_wallet_bal, import_wallet, send_trx,
                                 show_user_wallet)
from app.schemas.index import sendTron  # type: ignore
from app.schemas.index import ImportWallet, User, WalletDetails, liveprice

user = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

@user.post('/tron/send', status_code=status.HTTP_200_OK)
def sendTron(request: sendTron, db: Session = Depends(get_db)):  # type: ignore
    return send_trx(request, db)  # type: ignore




@user.websocket("/live/price/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
        return data


