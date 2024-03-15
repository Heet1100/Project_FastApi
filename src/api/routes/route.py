import fastapi
from sqlalchemy.orm import Session
from fastapi import APIRouter
from src.database.dao.Crud import Crud
from src.database.dao.models import model
from src.database.dao.Schema import Schema
from src.database.connection import sessionmaker
from src.database.connection import DBConnector as dbase
from src.core.config import s

engine = dbase.get_rds_instance(s)

model.Base.metadata.create_all(bind=engine)

route = APIRouter()


# Dependency
def get_db():
    db = sessionmaker()
    try:
        yield db
    finally:
        db.close_all()


@route.post("/users/", response_model=Schema.User)
def create_user(user: Schema.UserCreate, db: Session = fastapi.Depends(get_db)):
    db_user = Crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already registered")
    return Crud.create_user(db=db, user=user)


@route.get("/users/", response_model=list[Schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = fastapi.Depends(get_db)):
    users = Crud.get_users(db, skip=skip, limit=limit)
    return users


@route.get("/users/{user_id}", response_model=Schema.User)
def read_user(user_id: int, db: Session = fastapi.Depends(get_db)):
    db_user = Crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return db_user


@route.post("/users/{user_id}/items/", response_model=Schema.Item)
def create_item_for_user(
        user_id: int, item: Schema.ItemCreate, db: Session = fastapi.Depends(get_db)
):
    return Crud.create_user_item(db=db, item=item, user_id=user_id)


@route.get("/items/", response_model=list[Schema.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = fastapi.Depends(get_db)):
    items = Crud.get_items(db, skip=skip, limit=limit)
    return items
