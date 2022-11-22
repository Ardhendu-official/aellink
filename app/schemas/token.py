from datetime import datetime, time
from typing import Optional

from fastapi import File, UploadFile
from pydantic import BaseModel


class Assets(BaseModel):
    token_contect_id: str
