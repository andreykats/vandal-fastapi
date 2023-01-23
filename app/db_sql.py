from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:testing123@127.0.0.1:5432/vandal"

engine = create_engine(
    # This is only required for SQLite
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()
