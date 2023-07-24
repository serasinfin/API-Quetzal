# Python
import os
from os.path import join, dirname
# DotEnv
from dotenv import load_dotenv


class Settings:
    # Load env vars
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # Basic config
    SECRET_KEY: str = os.getenv('SECRET')
    # 60 minutes * 24 hours * 1 day = 1 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    SERVER_NAME: str = os.getenv('SERVER_NAME') or 'API'
    PROJECT_NAME: str = os.getenv('PROJECT_NAME') or 'DEFAULT'

    # DB config
    DB_USER: str = os.getenv('PG_USER')
    DB_PASSWORD: str = os.getenv('PG_PASSWORD')
    DB_NAME: str = os.getenv('PG_DBNAME')
    DB_HOST: str = os.getenv('PG_HOST')
    DB_PORT: str = os.getenv('PG_PORT')

    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
    )

    class Config:
        case_sensitive = True


settings = Settings()
