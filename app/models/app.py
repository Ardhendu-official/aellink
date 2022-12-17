import datetime
from datetime import datetime

from sqlalchemy import (BOOLEAN, Column, DateTime, Float, Integer, String,
                        Text, Time, true)

from app.config.database import Base


class DbApps(Base):
    __tablename__ = 'apps_details'
    app_id = Column(Integer, primary_key=True, autoincrement=True)  
    get_app_name = Column(String(255))
    get_package_name = Column(String(255))
    get_version_code = Column(String(255))
    get_version_number = Column(String(255))
    app_created_timestamp = Column(DateTime)
    in_down = Column(BOOLEAN)
