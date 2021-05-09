from typing import List, Optional
from pydantic import BaseModel

class DataBase(BaseModel):
    index: str

class CreateData(DataBase):
    pass

class Data(DataBase):
    id: int
    class Config():
        orm_mode = True