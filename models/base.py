from sqlalchemy.orm import DeclarativeBase
from connectors import db

# class Base(DeclarativeBase):
    # pass

Base = db.Model