import fastapi
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi import APIRouter
from src.database.dao.Crud import Crud
from src.database.dao.models import model
from src.database.dao.Schema import Schema
from sqlalchemy.orm import sessionmaker
from src.core.config import Settings
se = Settings()
a = se.db_url()
engine = create_engine(a)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

model.Base.metadata.create_all(bind=engine)

route = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


@route.post("/items/", response_model=Schema.User)
def create_an_item(user: Schema.User, store_id: int, db: Session = fastapi.Depends(get_db)):
    return Crud.create_user(db=db, user=user, store_id=store_id)


@route.get("/items/", response_model=list[Schema.User])
def Read_all_items(skip: int = 0, limit: int = 100, db: Session = fastapi.Depends(get_db)):
    users = Crud.get_users(db, skip=skip, limit=limit)
    return users


@route.get("/items/{item_id}", response_model=Schema.User)
def Read_an_item_with_given_id(item_id: int, db: Session = fastapi.Depends(get_db)):
    db_user = Crud.get_user_id(db, user_id=item_id)
    if db_user is None:
        raise fastapi.HTTPException(status_code=404, detail="Item not found")
    return db_user


@route.put("/items/{item_id}", response_model=Schema.User)
def update_an_item_with_given_id(item_id: int, name: str, price: int, des: str, store_id: int, db: Session = fastapi.Depends(get_db)):
    db_user = Crud.update_user(db, item_id, name, price, des, store_id)
    if db_user is None:
        raise fastapi.HTTPException(status_code=404, detail="Item not found to update it")
    return db_user


@route.delete("/items/{item_id}", response_model=Schema.User)
def delete_an_item_with_given_id(item_id: int, db: Session = fastapi.Depends(get_db)):
    db_user = Crud.delete_user(db, item_id)
    if db_user is None:
        raise fastapi.HTTPException(status_code=404, detail="Item not found to delete it")
    return db_user


@route.post("/store/", response_model=Schema.Item)
def create_a_store(item: Schema.Item, db: Session = fastapi.Depends(get_db)):
    return Crud.create_user_item(db=db, item=item)


@route.get("/store/", response_model=list[Schema.Item])
def read_all_stores(skip: int = 0, limit: int = 100, db: Session = fastapi.Depends(get_db)):
    items = Crud.get_items(db, skip=skip, limit=limit)
    if items is None:
        raise fastapi.HTTPException(status_code=404, detail="Item not found to update it")
    return items


@route.get("/store/store{store_id}", response_model=Schema.Item)
def read_the_store_with_given_id(store_id: int, db: Session = fastapi.Depends(get_db)):
    item = Crud.get_item_id(db, store_id)
    if item is None:
        raise fastapi.HTTPException(status_code=404, detail="Item not found")
    return item


@route.delete("/store/{store_id}", response_model=Schema.Item)
def delete_the_store_with_given_id(store_id: int, db: Session = fastapi.Depends(get_db)):
    item = Crud.delete_item(db, store_id)
    if item is None:
        raise fastapi.HTTPException(status_code=404, detail="Item not found delete it")
    return item
