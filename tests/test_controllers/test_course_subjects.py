import pytest
from flask import json
from models.course_subjects import CourseSubjects
from datetime import datetime


def login(client):

    data = {
        'input_value': 'sad',
        'password': '12345678',
        'role_as': 'teacher'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200, f"Login failed: {response.json}"
    access_token = response.json.get('access_token')
    return access_token

def test_get_course_subjects(client):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = client.get('/course-subjects', headers=headers)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    response_data = response.get_json()
    assert 'course_subjects' in response_data, "Response should contain 'course_subjects' key"



def test_get_course_subject(client, mocker):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    mock_cs = {
        "id": 2,
        "course_subject": "Advance Math"
        }
    
    mocker.patch.object(CourseSubjects, 'course_subject', return_value=mock_cs)
    
    cs = mock_cs['course_subject']
    course_subject_id = mock_cs["id"]

    response = client.get(f'/course-subjects/2', headers=headers)

    assert response.status_code == 201
    assert course_subject_id == 2


    

def test_create_course_subject(client, test_session, mocker):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    new_cs = {
        "course_subject": "Biology"
        }
    
    mocker.patch.object(CourseSubjects, 'course_subject', return_value=new_cs)

    response = client.post('/course-subjects', json=new_cs, headers=headers)
    
    assert response.status_code == 201, f"Expected status code 200, got {response.status_code}"
    assert response.get_json()['message'] == "New course subject has been created successfully"

def test_update_course_subject(client, test_session, mocker):

    course_subject = CourseSubjects(course_subject="Math")
    test_session.add(course_subject)
    test_session.commit()

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    updated_course_subject_data = {
        'course_subject': 'Advanced Math'
    }

    response = client.put(f'/course-subjects/2', json=updated_course_subject_data, headers=headers)
    
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    response_data = response.get_json()
    assert response_data['message'] == "Course subject updated successfully", "Unexpected response message"


def test_delete_course_subject(client, mocker):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


    expected_response = "data not Found"

    mocker.patch.object(CourseSubjects, "course_subject", return_value=expected_response)

    response = client.delete("/course-subjects/232", headers=headers)

    assert response.status_code == 404