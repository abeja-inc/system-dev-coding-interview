from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: str


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None


class Item(ItemBase):
    id: int
    owner_id: int
    created_at: datetime
    done: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
