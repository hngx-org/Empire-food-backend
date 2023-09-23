from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.middleware.jwt_handler import verify_token, oauth2_scheme
from app.db.database import get_db
from app.models.user_models import User


def authenticate(access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = verify_token(access_token)

    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="failed to authenticate user")


def get_admin_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    """
    Dependency function to get the admin user from the access token.

    Parameters:
        - token (str): Access token obtained from the request header.
        - db (Session): Database session dependency.

    Returns:
        models.Admins: Admin user retrieved from the database.

    Raises:
        HTTPException: If the access token is invalid, user is not found, or user is not authorized.
    """

    user_id = verify_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user and not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to execute this action"
        )
    return user
