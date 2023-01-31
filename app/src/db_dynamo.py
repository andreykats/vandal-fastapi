from pydantic import BaseSettings
from os import environ
import typing


class GlobalConfig(BaseSettings):
    DB_HOST: typing.Optional[str] = environ.get('DB_HOST')
    AWS_REGION: typing.Optional[str] = environ.get('AWS_DEFAULT_REGION')
    AWS_ACCESS_KEY_ID: typing.Optional[str] = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: typing.Optional[str] = environ.get('AWS_SECRET_ACCESS_KEY')


config = GlobalConfig()
