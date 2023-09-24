""" Sendlunch db insertion created by @dyagee """

from sqlalchemy.orm import Session

from app.models.lunch_models import Lunch
from app.schemas.lunch_schemas import SendLunch


def insert_lunch(db: Session, data: SendLunch, user_id: int, org_id: int):
    """ Insert lunch into the database """
    # Extract the data and enter into the database under lunches
    lunch_item = Lunch(
        **data.model_dump(exclude_unset=True), sender_id=user_id, org_id=org_id
    )

    db.add(lunch_item)
    db.commit()
    db.refresh(lunch_item)
    return lunch_item
