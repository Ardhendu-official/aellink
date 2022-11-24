from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL='mysql+mysqlconnector://root@localhost:3306/aellink'                      #localhost

SQLALCHEMY_DATABASE_URL='mysql+mysqlconnector://root:aellink@13.234.52.167:3306/aellink'                      #AWS

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # type: ignore

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
