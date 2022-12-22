from datetime import datetime, time
from typing import Optional

from fastapi import File, UploadFile
from pydantic import BaseModel


class Admin(BaseModel):
    admin_name : Optional[str] = None
    admin_email : Optional[str] = None
    admin_phone : Optional[str] = None
    admin_active : Optional[bool] = None
    admin_password : Optional[str] = None

class AdminLogin(BaseModel):
    admin_email : Optional[str] = None
    admin_password : Optional[str] = None

class AdminPassChange(BaseModel):
    password: str
    new_password: str
    admin_email: Optional[str] = None