from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3

TEST_DATABASE_URI = 'sqlite:///:memory:'

def create_test_engine():
    test_engine = create_engine(TEST_DATABASE_URI)
    return test_engine

def create_test_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

