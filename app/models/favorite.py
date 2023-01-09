from datetime import datetime

from sqlalchemy import (Column, DateTime, Float, Integer, String, Text, Time,
                        true)

from app.config.database import Base


class DbFavorite(Base):
    __tablename__ = 'favorite'
    favorite_id = Column(Integer, primary_key=True, autoincrement=True)  
    user_hash_id = Column(String(255))
    name = Column(String(255))
    image = Column(Text(4294000000))
    Subtitle = Column(Text(4294000000))
    url = Column(String(255))