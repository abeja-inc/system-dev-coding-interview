from typing import List, Optional

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from sqlalchemy.orm import Session

from . import models, schemas

pwd_context = PasswordHash([BcryptHasher()])


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_item(
    db: Session,
    user_id: int,
    item_id: int,
) -> Optional[models.Item]:
    q = db.query(models.Item).filter(
        models.Item.owner_id == user_id, models.Item.id == item_id
    )
    return q.first()


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(
    db: Session, item: schemas.ItemCreate, user_id: int
) -> models.Item:
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_user_item(
    db: Session, item: schemas.ItemUpdate, db_item: models.Item
) -> models.Item:
    if item.title is not None:
        db_item.title = item.title  # type: ignore
    if item.description is not None:
        db_item.description = item.description  # type: ignore
    if item.done is not None:
        db_item.done = item.done  # type: ignore
    db.commit()
    db.refresh(db_item)
    return db_item
