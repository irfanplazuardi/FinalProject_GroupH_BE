from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

username = os.getenv('DATABASE_USERNAME')
password = os.getenv('DATABASE_PASSWORD')
host = os.getenv('DATABASE_URL')
database = os.getenv('DATABASE_NAME')

# Connect to the database
print("Connecting to the MySQL Database")
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{database}')

# Test the connection
connection = engine.connect()
Session = sessionmaker(connection)
print(f'Connected to the MySQL Database at {host}')