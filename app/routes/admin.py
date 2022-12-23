from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.oprations.index import (change_admin_pass, create_admin, login_admin,
                                 show_admin, show_all_trans, show_wallet_list)
from app.schemas.index import Admin, AdminLogin, AdminPassChange

admin = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@admin.get('/admin/details', status_code=status.HTTP_200_OK)
def showAdmin(db: Session = Depends(get_db)):
    return show_admin(db)  

@admin.get('/admin/wallet/list', status_code=status.HTTP_200_OK)
def showWalletList(db: Session = Depends(get_db)):
    return show_wallet_list(db) 

@admin.post('/admin', status_code=status.HTTP_200_OK)
def createAdmin(request: Admin, db: Session = Depends(get_db)):
    return create_admin(request, db) 

@admin.post('/admin/login', status_code=status.HTTP_200_OK)
def loginAdmin(request: AdminLogin, db: Session = Depends(get_db)):
    return login_admin(request, db) 

@admin.post('/admin/change/pass', status_code=status.HTTP_202_ACCEPTED)
def changePass(request: AdminPassChange, db: Session = Depends(get_db)):  
    return change_admin_pass(request, db)

@admin.get('/trans/all', status_code=status.HTTP_200_OK)
def transactionAll(db: Session = Depends(get_db)):
    return show_all_trans(db) 