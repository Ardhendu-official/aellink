from sqlalchemy import Column, DateTime, Integer, String

from app.config.database import Base


class DbPin(Base):
    __tablename__ = 'pincode'
    pincode_id = Column(Integer, primary_key=True, autoincrement=True)
    pincode_code = Column(String(255), default=0, nullable=False)
    pincode_creation_timestamp = Column(DateTime, default=0, nullable=False)
