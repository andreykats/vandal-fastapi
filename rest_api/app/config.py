# https://stackoverflow.com/questions/68156262/how-to-set-environment-variable-based-on-development-or-production-in-fastapi

from pydantic import BaseSettings
from os import environ
import typing

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

class GlobalConfig(BaseSettings):
    ENV: typing.Optional[str] = environ.get('ENV')

# class GlobalDBCconfig(GlobalConfig):
    # SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"
    # # SQLALCHEMY_DATABASE_URL = "postgresql://postgres:testing123@127.0.0.1:5432/vandal"
    # engine = create_engine(
    #     # This is only required for SQLite
    #     SQLALCHEMY_DATABASE_URL
    # )
    # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
    # Base = declarative_base()

class GlobalAWSConfig(GlobalConfig):
    AWS_REGION: typing.Optional[str] = environ.get('AWS_DEFAULT_REGION')
    AWS_ACCESS_KEY_ID: typing.Optional[str] = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: typing.Optional[str] = environ.get('AWS_SECRET_ACCESS_KEY')
    
    S3_HOST: typing.Optional[str] = environ.get('S3_HOST')
    S3_BUCKET_IMAGES: typing.Optional[str] = environ.get('S3_BUCKET_IMAGES', '').lower()
    
    DB_HOST: typing.Optional[str] = environ.get('DB_HOST')
    DB_TABLE_LAYERS: typing.Optional[str] = environ.get('DB_TABLE_LAYERS')
    DB_TABLE_MESSAGES: typing.Optional[str] = environ.get('DB_TABLE_MESSAGES')

    WEBSOCKET_URI: typing.Optional[str] = environ.get('WEBSOCKET_URI', '')


config = GlobalAWSConfig()
