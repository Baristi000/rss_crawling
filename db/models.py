from sqlalchemy import Column, Integer, String
from .database import Base

class Data(Base):
    __tablename__ = "data"
    id = Column("id", Integer, primary_key=True)
    index = Column("index", String(255))