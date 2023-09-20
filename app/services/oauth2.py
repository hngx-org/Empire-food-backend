"""
Module Name: Authentication

This module provides authentication functions and dependencies for the StudentsEvaluationAPI application.

Functions:
    - create_access_token: Creates an access token with the provided data.
    - verify_tok: Verifies the access token and returns token data.
    - get_admin_user: Dependency function to get the admin user from the access token.

Dependencies:
    - jose.JWTError: Exception class for JWT-related errors.
    - jose.jwt: Provides functions for encoding and decoding JSON Web Tokens (JWT).
    - datetime.datetime: Provides classes for working with dates and times.
    - datetime.timedelta: Represents a duration or difference between two dates or times.
    - .schemas: Module containing Pydantic schemas used in the application.
    - .database: Module providing database-related functions.
    - .models: Module containing database models.
    - fastapi.Depends: Dependency decorator for declaring dependencies.
    - fastapi.status: Provides HTTP status codes.
    - fastapi.HTTPException: Exception class for HTTP-specific exceptions.
    - .config.settings: Module containing application settings.
    - fastapi.security.OAuth2PasswordBearer: OAuth2 password bearer authentication scheme.

Global Constants:
    - SECRET_KEY: Secret key used for JWT token encoding and decoding.
    - ALGORITHM: Algorithm used for JWT token encoding and decoding.
    - ACCESS_TOKEN_EXPIRE_MINUTES: Number of minutes until the access token expires.
    - credentials_exception: HTTPException instance for unauthorized credentials.

Dependencies (continued):
    - oauth2_scheme: OAuth2 password bearer authentication scheme instance.

"""

from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .config import settings
from fastapi.security import OAuth2PasswordBearer

from ..schemas.config import TokData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token/sign-in")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_tok_expire_minutes)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)


def create_access_token(data: dict):
    """
    Create an access token with the provided data.

    Parameters:
        - data (dict): Data to be encoded in the access token.

    Returns:
        str: Encoded access token.
    """

    encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expire})

    encoded = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verify_tok(token: str, credentialsException):
    """
    Verify the access token and extract token data.

    Parameters:
        - token (str): Access token to be verified.
        - credentialsException (HTTPException): Exception instance for unauthorized credentials.

    Returns:
        schemas.TokData: Token data extracted from the access token.

    Raises:
        HTTPException: If the access token is invalid or does not contain user_id.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        _id = payload.get("user_id")

        if not _id:
            raise credentialsException
        tok_data = TokData(id=_id)
    except JWTError:
        raise credentialsException
    return tok_data



