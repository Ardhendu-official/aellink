import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import Base

# from app.models.patient import DbPatient


class DbTransaction(Base):
    __tablename__ = 'transaction'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    # cust_id = Column(Integer, ForeignKey(DbPatient.cust_id))
    trans_transaction_id = Column(String(255))
    transaction_amount = Column(Float, default=0, nullable=False)
    transaction_status = Column(String(255))
    transaction_type = Column(String(255))
    transaction_date_time = Column(DateTime, onupdate=datetime.datetime.now)

    cust_id_constraint = relationship(
        "DbCustomer", cascade="all,delete", backref="transaction")