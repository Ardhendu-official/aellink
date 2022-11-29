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
    password: str

class passVarify(BaseModel):
    user_address: str
    password: str