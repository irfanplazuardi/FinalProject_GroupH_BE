from flask import Blueprint
from sqlalchemy.exc import IntegrityError
import bcrypt
from datetime import date
from models.student import Student
from tests.conftest import client, test_session


def test_login_success(client):

    login_data = {
        "input_value": "samuel",
        "password": "12345678",
        "role_as": "teacher"
    }
    
    response = client.post("/login", json=login_data)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.get_json()
    assert "access_token" in data, "Expected 'access_token' in response"
    assert "role" in data, "Expected 'role' in response"
    assert data["role"] in ["teacher", "student"], "Expected role to be 'teacher' or 'student'"


def test_login_empty_credentials(client):
    login_data = {
        "input_value": "",
        "password": "",
        "role_as": ""
    }

    response = client.post("/login", json=login_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"

