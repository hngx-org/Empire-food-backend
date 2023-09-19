import os


class Settings:
    db_hostname: str = os.environ.get('DB_HOSTNAME')
    db_port: str = os.environ.get('DB_PORT')
    db_password: str = os.environ.get('DB_PASSWORD')
    db_username: str = os.environ.get('DB_USERNAME')
    db_name: str = os.environ.get('DB_NAME')
    secret_key: str = os.environ.get('SECRET_KEY')
    algorithm: str = os.environ.get('ALGORITHM')


settings = Settings()