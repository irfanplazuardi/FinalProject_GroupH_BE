from unittest.mock import MagicMock
from flask import json
import pytest
from models.course import Course
from models.student import Student
from models.students_course import StudentsCourse
from flask_jwt_extended import current_user, jwt_required

def login(client):

    data = {
        'input_value': 'irfan',
        'password': '12345678',
        'role_as': 'student'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200, f"Login failed: {response.json}"
    access_token = response.json.get('access_token')
    return access_token


def test_get_students_courses(client):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = client.get('/students_course', headers=headers)
    assert response.status_code == 200, "Failed to retrieve students' courses"

    data = response.get_json()
    assert isinstance(data, list), "Expected a list of students' courses"

def test_get_students_course(client, test_session):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    students_course_id = 1
    
    response = client.get(f'/students_course/{students_course_id}', headers=headers)
    assert response.status_code == 200, "Failed to retrieve the students' course"

    data = response.get_json()
    assert 'student_id' in data, "Student ID not found in response"
    assert 'course_id' in data, "Course ID not found in response"


def test_create_students_course(client, mocker, test_session):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    students_course_data = {
        'course_id': '5'
    }

    mocker.patch.object(test_session, 'add')
    mocker.patch.object(test_session, 'commit')

    response = client.post('/students_course', json=students_course_data, headers=headers)

    assert response.status_code == 400, 'Invalid Form Data'



def test_delete_students_course(client, mocker):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


    expected_response = "data not Found"

    mocker.patch.object(StudentsCourse, "query", return_value=expected_response)

    response = client.delete("/students_course/232", headers=headers)

    assert response.status_code == 404