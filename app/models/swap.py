import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import Base


class DbSwap(Base):
    __tablename__ = 'swap_transaction'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_tx_from = Column(String(255))
    transaction_tx_to = Column(String(255))
    transaction_tx_id = Column(String(255))
    transaction_amount_from = Column(Float, default=0, nullable=False)
    transaction_amount_to = Column(Float, default=0, nullable=False)
    transaction_status = Column(String(255))
    trans_to_account = Column(String(255))
    trans_from_account = Column(String(255))
    trans_user_id = Column(String(255))
    trans_currency_from = Column(String(255))
    trans_currency_to = Column(String(255))
    transaction_date_time = Column(DateTime)