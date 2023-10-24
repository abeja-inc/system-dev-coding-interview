from typing import Generator, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_session = Depends(get_db)


@app.get("/health-check", response_model=schemas.HealthCheck)
def health_check(db: Session = db_session) -> schemas.HealthCheck:
    return schemas.HealthCheck(status="ok")


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = db_session) -> models.User:
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=List[schemas.User])
def read_users(
    skip: int = 0, limit: int = 100, db: Session = db_session
) -> List[models.User]:
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = db_session) -> models.User:
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = db_session
) -> models.Item:
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items", response_model=List[schemas.Item])
def read_items(
    skip: int = 0, limit: int = 100, db: Session = db_session
) -> List[models.Item]:
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.patch("/users/{user_id}/items/{item_id}", response_model=schemas.Item)
def update_item_for_user(
    user_id: int, item_id: int, item: schemas.ItemUpdate, db: Session = db_session
) -> models.Item:
    db_item = crud.get_item(
        db=db,
        user_id=user_id,
        item_id=item_id,
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.update_user_item(db=db, item=item, db_item=db_item)
