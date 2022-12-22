from datetime import datetime

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.functions.index import Hash, HashVerify
from app.models.index import (DbAdmin, DbFeesTransaction, DbSwap,
                              DbTrxTransaction, DbUser)
from app.schemas.index import Admin, AdminLogin, AdminPassChange

app = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def show_admin(db: Session = Depends(get_db)):
    a_data = db.query(DbAdmin).first()
    total_commission = a_data.admin_comission            #type: ignore
    u_data = db.query(DbUser.user_address).all()
    total_user = u_data.__len__()
    t_data = db.query(DbTrxTransaction).all()
    total_send = t_data.__len__()
    s_data = db.query(DbSwap).all()
    total_swap = s_data.__len__()
    return {'total_commission': total_commission, 'total_user': total_user, 'total_send': total_send, 'total_swapn': total_swap}

def create_admin(request: Admin, db: Session = Depends(get_db)):
    new_admin = DbAdmin( 
        admin_name = request.admin_name,
        admin_email = request.admin_email,
        admin_phone = request.admin_phone,
        admin_active = request.admin_active,
        admin_created_timestamp = datetime.now(pytz.timezone('Asia/Calcutta')),
        admin_password = Hash.bcrypt(request.admin_password),                 # type: ignore    
        admin_comission = 0.00
    )
    db.add(new_admin)
    db.commit()
    admin = db.query(DbAdmin).filter(DbAdmin.admin_id == new_admin.admin_id).first()
    return admin

def login_admin(request: AdminLogin, db: Session = Depends(get_db)):
   user = db.query(DbAdmin).filter(DbAdmin.admin_email == request.admin_email).first()
   if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with the email-id {request.admin_email} is not available")
   else:
        if HashVerify.bcrypt_verify(request.admin_password, user.admin_password):                        # type: ignore     
                   return {'Status': 'Success', "details": 'Login Successfully', 'User-Email': user.admin_email, 'login-time': datetime.now(pytz.timezone('Asia/Calcutta'))}
        else:
            return {'Status': 'Failed', "details": 'Wrong Password', 'User-Email': user.admin_email}

def change_admin_pass(request: AdminPassChange, db: Session = Depends(get_db)):
    user = db.query(DbAdmin).filter(DbAdmin.admin_email == request.admin_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user not found")
    else:
        if HashVerify.bcrypt_verify(request.password, user.admin_password):                 # type: ignore  
            password = Hash.bcrypt(request.new_password)  # type: ignore
            db.query(DbAdmin).filter(DbAdmin.admin_email == request.admin_email).update({"admin_password": f'{password}'}, synchronize_session='evaluate')
            db.commit()
            return {"msg": "password update done"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"incorrect password")

def show_wallet_list(db: Session = Depends(get_db)):
    u_data = db.query(DbUser.user_address, DbUser.user_hash_id, DbUser.user_wallet_name, DbUser.user_registration_date_time).all()
    return u_data