from decouple import config


class Settings:
    secret_key: str = "HI5HL3V3L$3CR3T"
    algorithm: str = "HS256"
    access_tok_expire_minutes: int = 3600
    refresh_tok_expire_minutes: int = 3600
    email_api_key: str = config("EMAIL_API_KEY")
    email_api_secret: str = config("EMAIL_API_SECRET_KEY")
    OTP_INTERVAL: int = config("OTP_INTERVAL")
    FRONTEND_URL: str = config("FRONTEND_URL")


EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
# SECRET_KEY = str(config("SECRET_KEY"))
# DATABASE_URI = str(config("DATABASE_URI"))
# DATABASE_NAME = str(config("DATABASE_NAME"))
