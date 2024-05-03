from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


username = os.getenv('DATABASE_USERNAME')
password = os.getenv('DATABASE_PASSWORD')
host = os.getenv('DATABASE_URL')
database = os.getenv('DATABASE_NAME')
port = 34808

# Connect to the database
print("Connecting to the MySQL Database")
sql_string =  f'mysql+mysqlconnector://{username}:{password}@{host}/{database}'

engine = create_engine(sql_string)

# Test the connection
connection = engine.connect()
Session = sessionmaker(connection)
print(f'Connected to the MySQL Database at {host}')