from datetime import datetime

from sqlalchemy import (Column, DateTime, Float, Integer, String, Text, Time,
                        true)

from app.config.database import Base


class DbUser(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)  # type: ignore
    user_hash_id = Column(String(255))  # type: ignore
    user_wallet_name = Column(String(255))
    user_image = Column(String(255), default=0, nullable=False)
    user_publicKey = Column(Text(4294000000))
    user_privateKey = Column(Text(4294000000))
    user_address = Column(Text(4294000000))
    user_mnemonic_key = Column(String(255))
    user_registration_date_time = Column(DateTime)
    user_password = Column(String(255))
    user_token_id = Column(String(255))
    