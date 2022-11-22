from datetime import datetime

from sqlalchemy import (Column, DateTime, Float, Integer, String, Text, Time,
                        true)

from app.config.database import Base


class DbToken(Base):
    __tablename__ = 'token'
    token_id = Column(Integer, primary_key=True, autoincrement=True)  # type: ignore
    token_name = Column(String(255))
    token_short_name = Column(String(255))
    token_contect_id = Column(String(255))
    token_logo = Column(String(255))
    token_type = Column(String(255))
    token_level = Column(String(255))
    issuer_addr = Column(String(255))
    token_vip = Column(Float)
    token_decimal = Column(Integer)
    token_can_show = Column(Integer)
    token_registration_date_time = Column(DateTime)