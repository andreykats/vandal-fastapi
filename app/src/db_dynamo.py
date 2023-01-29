from pydantic import BaseSettings
import os


class GlobalConfig(BaseSettings):
    # DB_HOST: str = "http://localhost:8000"
    DB_HOST: str = "http://docker.for.mac.localhost:8000/"
    ENVIRONMENT: str = "remote"
    AWS_REGION: str = os.environ.get('AWS_DEFAULT_REGION')
    AWS_ACCESS_KEY_ID: str = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: str = os.environ.get('AWS_SECRET_ACCESS_KEY')


config = GlobalConfig()
