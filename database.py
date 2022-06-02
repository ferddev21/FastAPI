from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create a sqlite engine instance
engine = create_engine("sqlite:///pet2home.db")

# Create a DeclarativeMeta instance
Base = declarative_base()

# Define To Do class inheriting from Base


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    email = Column(String(256))
    fullname = Column(String(256))
    password = Column(String(256))
