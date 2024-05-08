
from datetime import date
import bcrypt
import pytest
from flask import Flask
from models.base import Base
from tests.test_db_config import create_test_engine, create_test_session
from flask_sqlalchemy import SQLAlchemy
from models.teacher import Teacher
from app import create_app  


db = SQLAlchemy()


@pytest.fixture(scope='session')
def test_engine():
    return create_test_engine()

@pytest.fixture(scope='function')
def test_session(test_engine):
    session = create_test_session(test_engine)
    Base.metadata.create_all(test_engine)
    yield session
    session.rollback()
    session.close()

@pytest.fixture(scope='function')
def app(test_session):
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.db_session = test_session
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def dummy_user(app):
    password = "12345678"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    dummy_user = Teacher(
        teacher_id= 1,
        password = hashed_password,
        teacher_name = "samuel",
        teacher_email = "sa@gmail.com",
        teacher_birthday = date(1990, 1, 1),
        phone = "0877005955555",
        role='teacher'
        )

    app.db_session.add(dummy_user)
    app.db_session.commit()
    yield dummy_user

    app.db_session.delete(dummy_user)
    app.db_session.commit()

@pytest.fixture(scope='function')
def login(client, dummy_user):
    response = client.post('/login', json={
        'input_value': dummy_user.teacher_name, 
        'password': '12345678'
    })
    assert response.status_code == 200, "Login failed"

    data = response.get_json()
    assert 'access_token' in data, "Access token not found in response"

    access_token = data['access_token']

    print(response, 'access_token:', access_token)
    
    return access_token
