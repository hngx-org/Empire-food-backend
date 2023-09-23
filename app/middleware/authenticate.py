from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user_models import User

from app.middleware.jwt_handler import verify_token

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def send_email(message: str, subject: str, to_email: str):
    pass


def authenticate(access_token: str = Header(), db: Session = Depends(get_db)):
    """
    Authenticates the user by verifying the access token and returning the user
    object from the database.

    Args:
        access_token (str, optional): The access token to verify. Defaults to
            Header().
        db (Session, optional): The database session. Defaults to
            Depends(get_db).

    Raises:
        HTTPException: If the access token is not provided.
        HTTPException: If the user fails to authenticate.

    Returns:
        User: The user object from the database.
    """
    if access_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = verify_token(access_token)

    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=401, detail="failed to authenticate user"
        )
