from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.connection import Base


class User(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer,nullable=False)
    description = Column(String)
    store_id= Column(Integer, ForeignKey("store"))
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "store"

    store_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    owner = relationship("User", back_populates="items")