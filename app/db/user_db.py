from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.user_schemas import UserCreate
from app.models.user_models import User
from datetime import datetime
import logging
from uuid import uuid4
from app.Responses.response import Response
from app.services import user_services


def get_user(db: Session, user_id: int):
    pass


# add user to database
def create_user(db: Session, user: UserCreate):
    t_time = datetime.now()

    createdAt = t_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    updatedAt = t_time.strftime('%Y-%m-%d %H:%M:%S.%f')

    password_hash = user_services.hash_password(user.password)

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        profile_pic="",
        email=user.email,
        phone=user.phone_number,
        is_admin=False,
        lunch_credit_balance=0,
        password_hash=password_hash,
        created_at=createdAt,
        updated_at=updatedAt
    )

    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)

        return Response(
            msg="Successfully created a user",
            statusCode=200,
            data=db_user
        )
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(
            "Failed to Commit because of {error}. Doing Rollback".format(error=e))
