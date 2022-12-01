from datetime import datetime, time
from typing import Optional

from fastapi import File, UploadFile
from pydantic import BaseModel


class Banner(BaseModel):
    image: Optional[str] = None
    name: Optional[str] = None
    Subtitle: Optional[str] = None
    url: Optional[str] = None