from decouple import config

class Settings:
    secret_key: str = "HI5HL3V3L$3CR3T"
    algorithm: str = "HS256"
    access_tok_expire_minutes: int = 3600
    refresh_tok_expire_minutes: int = 3600
<<<<<<< HEAD
    api_key: str = 'b31050ab8f0e78989057784bce049c6d'
    api_secret: str = '03a2681aebcca8d587135ceb781e8d0c'
=======
    email_api_key: str = config("EMAIL_API_KEY")
    email_api_secret: str = config("EMAIL_API_SECRET_KEY")
    OTP_INTERVAL : int = config("OTP_INTERVAL")
    FRONTEND_URL : str = config("FRONTEND_URL")
>>>>>>> d04647ce78be91651b31240b6c90717cc1769bf6


EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
# SECRET_KEY = str(config("SECRET_KEY"))
# DATABASE_URI = str(config("DATABASE_URI"))
# DATABASE_NAME = str(config("DATABASE_NAME"))