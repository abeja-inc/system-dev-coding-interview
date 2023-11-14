from datetime import datetime

from sqlalchemy.orm import Session

from sql_app import models


def update_created_at(db: Session, item_id: str, created_at: str) -> None:
    """Update created_at of item
    Args:
        db: db session
        item_id: id of item to update
        created_at: string of date to update(format is %Y-%m-%dT%H:%M:%S)
    """
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    item.created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S")
    db.commit()
