from sqlalchemy.orm import Session
from . import models, schemas

def create_data(db: Session, index: schemas.CreateData):
    data = models.Data(index=index)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def get_all(db: Session, skip: int = 0):
    rows = db.query(models.Data).count()
    return db.query(models.Data).offset(skip).limit(rows).all()

def delete_at(db:Session, at:int):
    db.query(models.Data).filter(models.Data.index == db.query(models.Data).offset(at).limit(1).first().index).delete(synchronize_session=False)
    db.commit()

def get_at(db:Session, at:int):
    try:
        return db.query(models.Data).offset(at).limit(1).first().index
    except:
        return None

def delete_all(db:Session):
    db.query(models.Data).delete()
    db.commit()
