# sendlunch db insertion created by @dyagee


from app.models.lunch_models import Lunch
from app.schemas.lunch_schemas import SendLunch
from sqlalchemy.orm import Session


def insert_lunch(db: Session, data: SendLunch, user_id: int):
    # Extract the data and enter into the database under lunches
    lunch_item = Lunch(**data.model_dump(exclude_unset=True), sender_id=user_id)
    db.add(lunch_item)
    db.commit()
    db.refresh(lunch_item)
    return lunch_item
