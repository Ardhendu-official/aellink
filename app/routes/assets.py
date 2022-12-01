from datetime import datetime
from mimetypes import guess_type
from os.path import isfile
from typing import List

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine

assets = APIRouter()

@assets .get("/images/{file_name}")
async def get_images(file_name):
    url = "static/" + file_name
    return FileResponse(url)