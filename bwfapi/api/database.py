from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{config('MYSQL_USER')}:@{config('MYSQL_HOST')}/{config('MYSQL_DB')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
