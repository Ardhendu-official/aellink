import uvicorn
from fastapi import (Depends, FastAPI, HTTPException, Response, responses,
                     status)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.session import Session

from app.config.database import Base, engine
from app.routes.index import assets, banner, token, user

Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user,tags=['User'])
app.include_router(token,tags=['Token'])
app.include_router(banner,tags=['Banner'])
app.include_router(assets,tags=['Assets'])
