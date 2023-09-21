from app.db.database import get_db
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    return db.query(User).filter(user.id == user_id).first()


def create_user_account(db:Session,user_id:int):
    pass


def get_user_account(db:Session,user_id:int):
    pass
