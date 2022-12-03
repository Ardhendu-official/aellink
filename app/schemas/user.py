from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    user_wallet_name: str
    user_password: str
    user_hash_id: Optional[str] = None

class ImportWallet(BaseModel):
    user_wallet_name: str
    m_key_or_p_key: str
    user_hash_id: Optional[str] = None
    user_password: str

class WalletDetails(BaseModel):
    user_hash_id: Optional[str] = None
    user_address: str

class liveprice(BaseModel):
    user_hash_id: Optional[str] = None
    assets: str

class sendTron(BaseModel):
    from_account: str
    to_account: str
    amount: int
    user_hash_id: Optional[str] = None
    password: Optional[str] = None

class passVarify(BaseModel):
    user_address: str
    password: str
    user_hash_id: Optional[str] = None

class passChange(BaseModel):
    user_address: str
    password: str
    new_password: str
    user_hash_id: Optional[str] = None

class updateWallet(BaseModel):
    user_address: str
    user_wallet_name: str
    user_hash_id: Optional[str] = None

class deleteWallet(BaseModel):
    user_address: str
    user_hash_id: Optional[str] = None