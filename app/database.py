from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL='postgresql://<username>:<password>@<ip-address>/<hostname>/<database-name>'
# host='localhost'
# database='fastapi'
# user='postgres'
# password="'r00t@admin'"

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:5432/db"
# SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{database}"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
