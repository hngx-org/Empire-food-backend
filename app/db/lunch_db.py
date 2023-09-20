from app.models.lunch_models import Lunch
from app.schemas.lunch_schemas import SendLunch
from sqlalchemy.orm import Session


def insert_lunch(db: Session, user_id: int,data:SendLunch):
    #return db.query(Launch).filter(Launch.id == user_id).first()
    lunch_item = Lunch(**data.model_dump(), sender_id=user_id)
    db.add(lunch_item)
    db.commit()
    db.refresh(lunch_item)
    return lunch_item