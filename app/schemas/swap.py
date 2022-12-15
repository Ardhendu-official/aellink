from datetime import datetime, time
from typing import Optional

from fastapi import File, UploadFile
from pydantic import BaseModel


class Estimated(BaseModel):
    currency_from: str
    currency_to: str
    amount: str
