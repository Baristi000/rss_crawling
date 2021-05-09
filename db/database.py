from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import setting

database_url = f"mysql://trieu:tt123@{setting.db_host}:3306/trieu_db"
engine = create_engine(database_url)
session = sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base = declarative_base()