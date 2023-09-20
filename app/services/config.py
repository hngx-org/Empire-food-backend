import os


class Settings:
    secret_key: str = os.environ.get('SECRET_KEY')
    algorithm: str = os.environ.get('ALGORITHM')
    access_tok_expire_minutes: int = os.environ.get('ACCESS_TOK_EXPIRE_MINUTES')


settings = Settings()
