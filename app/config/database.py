from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL='mysql+mysqlconnector://root:aellink@192.168.0.229:3306/aellink'                      #localhost

SQLALCHEMY_DATABASE_URL='mysql+mysqlconnector://root:aellink@65.1.190.123:3306/aellink'                      #AWS

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
