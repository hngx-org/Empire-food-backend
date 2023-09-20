from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
from app.models.user_models import Users
from datetime import datetime
from uuid import uuid4
from app.Responses.response import Response

def get_user(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()


# add user to database
def create_user(db: Session, user: UserCreate):
    db_user = Users(
        id = uuid4(),
       first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=user.password,
        is_admin=False,
        phonenumber=user.phone_number,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    try:
        
      db.add(db_user)
      db.commit()
      db.refresh(db_user)
      return db_user, None
    except Exception as e:
      print(e)
      return None, Response(msg="failed to create r", code=500)

