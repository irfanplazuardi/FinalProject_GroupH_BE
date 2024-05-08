import pytest
from flask import json
from models.course import Course
from models.course_subjects import CourseSubjects
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from unittest.mock import MagicMock, patch

def login(client):

    data = {
        'input_value': 'samuel',
        'password': '87654321',
        'role_as': 'teacher'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200, f"Login failed: {response.json}"
    access_token = response.json.get('access_token')
    return access_token


def test_get_courses(client, mocker, test_session):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    mock_courses = [
        Course(course_id=1, course_name="caraloncat", course_subject_id=1, course_description="Basic Math", course_grade="A"),
        Course(course_id=2, course_name="Science", course_subject_id=2, course_description="Basic Science", course_grade="B")
    ]

    mocker.patch.object(test_session, 'query').return_value.all.return_value = mock_courses

    response = client.get('/courses', headers=headers)

    assert response.status_code == 200
    response_data = response.get_json()
    assert 'courses' in response_data, "Response should contain 'courses' key"


def test_get_course(client, mocker, test_session):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


    course_id = 3
    mock_course = {
        "course_id": course_id, 
        "course_name": "Advanced Math", 
        "course_subject_id": 2, 
        "course_description":"Advanced concepts in math", 
        "course_grade":"SD"
        }

    mocker.patch.object(test_session, 'query').return_value.filter.return_value.first.return_value = mock_course

    response = client.get(f'/courses/3', headers=headers)

    assert response.status_code == 201
    data = response.get_json()
    assert 'course' in data
    assert data['course']['course_name'] == mock_course['course_name']
    assert data['course']['course_id'] == mock_course['course_id']
    assert data['course']['course_description'] == mock_course['course_description']
    assert data['course']['course_grade'] == mock_course['course_grade']


def test_create_course(client, mocker, test_session):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    new_course_data = {
        'course_name': 'History',
        'course_subject_id': 3,
        'course_description': 'World History',
        'course_grade': 'SD'
    }

    mocker.patch.object(test_session, 'add')
    mocker.patch.object(test_session, 'commit')

    response = client.post('/courses', json=new_course_data, headers=headers)

    assert response.status_code == 201
    assert response.get_json()['message'] == "New course has been created successfully"


def test_update_course(client):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    updated_course_data = {
        'course_name': 'Advanced Math',
        'course_description': 'Advanced concepts in math',
        'course_subject_id': 3
    }

    response = client.put(f'/courses/3', json=updated_course_data, headers=headers)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.get_json()
    assert data['message'] == "Course updated successfully"


def test_delete_fail_course(client, mocker):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


    expected_response = "data not Found"

    mocker.patch.object(Course, "query", return_value=expected_response)

    response = client.delete("/courses/232", headers=headers)

    assert response.status_code == 404






