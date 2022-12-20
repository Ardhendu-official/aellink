from datetime import datetime, time
from typing import Optional

from fastapi import File, UploadFile
from pydantic import BaseModel


class Exchange(BaseModel):
    currency_from: str
    currency_to: str
    address_to: str
    amount_from: str
    user_hash_id: str
    # password: Optional[str] = None