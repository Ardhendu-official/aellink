import datetime
from datetime import datetime

from sqlalchemy import (BOOLEAN, Column, DateTime, Float, Integer, String,
                        Text, Time, true)

from app.config.database import Base


class DbAdmin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True, autoincrement=True)  
    admin_name = Column(String(255))
    admin_email = Column(String(255))
    admin_phone = Column(String(255))
    admin_active = Column(BOOLEAN)
    admin_created_timestamp = Column(DateTime)
    admin_password = Column(String(255))
    admin_comission = Column(Float)
