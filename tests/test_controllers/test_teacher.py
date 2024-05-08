from datetime import date

import bcrypt
from models.teacher import Teacher


def login(client):
    response = client.post('/login', json={
        'input_value': 'samuel',
        'password': '87654321',
        'role_as': 'teacher'
    })
    print("Login response status code:", response.status_code)
    print("Login response JSON:", response.get_json())

    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    return data['access_token']


def test_get_teachers(client, test_session):

    access_token = login(client)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    password = "password123"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    test_teacher_1 = Teacher(teacher_name="Teacher 1", teacher_email="teacher1@example.com", teacher_birthday=date(1990, 1, 1), phone="08080444856", password=hashed_password)
    test_teacher_2 = Teacher(teacher_name="Teacher 2", teacher_email="teacher2@example.com", teacher_birthday=date(1990, 1, 1), phone="00565888521", password=hashed_password)
    test_session.add_all([test_teacher_1, test_teacher_2])
    test_session.commit()

    response = client.get('/teachers', headers=headers)

    assert response.status_code == 200
    assert test_teacher_1.teacher_name == "Teacher 1"
    assert test_teacher_2.teacher_name == "Teacher 2"


def test_get_teacher(client):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = client.get(f'/teachers/8', headers=headers)

    assert response.status_code == 201
    data = response.get_json()
    assert 'teacher' in data, "Response data does not contain 'teacher' key"


def test_create_teacher(client, test_session, mocker):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    new_teacher_data = {
        'teacher_name': 'New Teach',
        'teacher_email': 'newteach@example.com',
        'teacher_birthday': '1990-01-01',
        'phone': '1234567879',
        'password': 'password123'
    }

    mocker.patch.object(Teacher, 'teacher_name', return_value=new_teacher_data)
    response = client.post('/teachers', json=new_teacher_data, headers=headers)

    assert response.status_code == 200


def test_update_teacher(client, test_session, mocker):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    updated_data = {
        "teacher_name": "updet",
        "teacher_email": "updated@example.com",
        "phone": "0987654321"
    }

    mock_teacher = mocker.patch.object(test_session.query(Teacher), 'filter_by').return_value.first.return_value
    mock_teacher.teacher_name = "Tabc"
    mock_teacher.teacher_email = "abc@example.com"
    mock_teacher.phone = "1234567890"

    response = client.put(f'/teachers/{2}', json=updated_data, headers=headers)


    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    mock_teacher.teacher_name = updated_data['teacher_name']
    mock_teacher.teacher_email = updated_data['teacher_email']
    mock_teacher.phone = updated_data['phone']

    assert mock_teacher.teacher_name == updated_data["teacher_name"]
    assert mock_teacher.teacher_email == updated_data["teacher_email"]
    assert mock_teacher.phone == updated_data["phone"]



def test_delete_teacher(client, mocker, test_session):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    expected_response = "Data tidak ditemukan"
    
    mocker.patch.object(test_session, "delete", return_value=expected_response)

    response = client.delete("/teachers/222", headers=headers)

    assert response.status_code == 404


