from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class HealthCheck(BaseModel):
    status: str


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    done: bool | None = None


class Item(ItemBase):
    id: int
    owner_id: int
    created_at: datetime
    done: bool

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    model_config = ConfigDict(from_attributes=True)
