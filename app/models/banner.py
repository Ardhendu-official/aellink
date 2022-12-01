from datetime import datetime

from sqlalchemy import (Column, DateTime, Float, Integer, String, Text, Time,
                        true)

from app.config.database import Base


class DbBanner(Base):
    __tablename__ = 'banner'
    banner_id = Column(Integer, primary_key=True, autoincrement=True)  
    image = Column(Text(4294000000))
    name = Column(String(255))
    Subtitle = Column(Text(4294000000))
    url = Column(String(255))
