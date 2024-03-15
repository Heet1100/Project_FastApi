from typing import List

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    store_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    price: int
    description: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True