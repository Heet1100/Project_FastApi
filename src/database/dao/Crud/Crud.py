from sqlalchemy.orm import Session
from src.database.dao.models import model
from src.database.dao.Schema import Schema


def get_user_id(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: Schema.User, store_id: int):
    db_user = model.User(**user.dict(), store_id=store_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, name: str, price: int, description: str, store_id: int):
    db_user = db.query(model.User).filter(model.User.id == user_id).first()
    db_user.name = name
    db_user.price = price
    db_user.description = description
    db_user.store_id = store_id
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(model.User).filter(model.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Item).offset(skip).limit(limit).all()


def get_item_id(db: Session, store_id: int):
    return db.query(model.User).filter(model.Item.store_id == store_id).first()


def create_user_item(db: Session, item: Schema.Item):
    db_item = model.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, store_id: int):
    db_user = db.query(model.Item).filter(model.Item.store_id == store_id).first()
    db.delete(db_user)
    db.commit()
    return db_user
