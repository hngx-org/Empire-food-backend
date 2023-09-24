from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        """
        Initializes a JWTBearer instance.

        Args:
            auto_error (bool, optional): Determines whether an error should be
                automatically raised if the authentication fails.
                Defaults to True.
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Handles the authentication logic for JWT-based authentication.

        Args:
            request (Request): The incoming request object.

        Raises:
            HTTPException: If the authentication token is invalid or missing.

        Returns:
            str: The JWT token extracted from the request.
        """
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=403, detail="Invalid authorization token"
            )
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=403, detail="Invalid authentication token"
            )
        return credentials.credentials
