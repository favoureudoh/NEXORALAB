from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Member(Base):
    # This is the name of the table in MySQL
    __tablename__ = "members"

    # Each variable here is a column in the table
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # will store hashed password
    joined_at = Column(DateTime, server_default=func.now())
