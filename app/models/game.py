import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from app.config.database import Base


class DbGame(Base):
    __tablename__ = 'game'
    game_id = Column(Integer, primary_key=True, autoincrement=True)
    game_unique_id = Column(String(255))
    game_name = Column(String(255))
    game_image = Column(String(255), default=0, nullable=False)
    game_registration_date_time = Column(DateTime)
    game_end_date_time = Column(DateTime)
    game_unit_price = Column(String(255))
    game_min_ticket_number = Column(String(255))
    game_1st_price = Column(String(255))
    game_2nd_price = Column(String(255))
    game_3nd_price = Column(String(255))
    number_of_ticket_sale = Column(String(255))
    game_1st_Winner = Column(String(255))
    game_2nd_Winner = Column(String(255))
    game_3nd_Winner = Column(String(255))