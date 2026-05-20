import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Uses DATABASE_URL from Render environment variables in production
# Falls back to your local MySQL when running on your own computer
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:yourpassword@localhost/nexoralab?charset=utf8mb4",
)

# FreeSQLDatabase and Railway give mysql:// but SQLAlchemy needs mysql+pymysql://
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

engine = create_engine(DATABASE_URL, connect_args={"ssl_disabled": True})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
