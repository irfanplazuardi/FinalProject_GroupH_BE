from datetime import date

import bcrypt
from models.student import Student


def login(client):
    response = client.post('/login', json={
        'input_value': 'jojonsy@gmail.com',
        'password': '12345678',
        'role_as': 'student'
    })
    print("Login response status code:", response.status_code)
    print("Login response JSON:", response.get_json())

    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    return data['access_token']


def test_get_students(client, test_session):

    access_token = login(client)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    password = "password123"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    test_student_1 = Student(student_name="studentone", student_email="s1@example.com", student_birthday=date(1990, 1, 1), phone="08080844856", password=hashed_password)
    test_student_2 = Student(student_name="studenttwo", student_email="s2@example.com", student_birthday=date(1990, 1, 1), phone="00565828521", password=hashed_password)
    test_session.add_all([test_student_1, test_student_2])
    test_session.commit()

    response = client.get('/students', headers=headers)

    assert response.status_code == 200
    assert test_student_1.student_name == "studentone"
    assert test_student_2.student_name == "studenttwo"


def test_get_student(client):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = client.get(f'/students/8', headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert 'student' in data, "Response data does not contain 'student' key"


def test_create_student(client, mocker):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    new_student_data = {
        'student_name': 'Newstud',
        'student_email': 'studbaru@example.com',
        'student_birthday': '1990-01-01',
        'phone': '1234567879',
        'password': 'password123'
    }

    mocker.patch.object(Student, 'student_name', return_value=new_student_data)
    response = client.post('/students', json=new_student_data, headers=headers)

    assert response.status_code == 403, "Expected status code 403, but got {response.status_code}"



def test_update_student(client, test_session, mocker):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    updated_data = {
        "student_name": "updet",
        "student_email": "updated@example.com",
        "phone": "0987654321"
    }

    mock_student = mocker.patch.object(test_session.query(Student), 'filter_by').return_value.first.return_value
    mock_student.student_name = "Tabc"
    mock_student.student_email = "abc@example.com"
    mock_student.phone = "1234567890"

    response = client.put(f'/students/2', json=updated_data, headers=headers)


    assert response.status_code == 403, "Expected status code 403, but got {response.status_code}"


def test_delete_student(client, mocker, test_session):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    expected_response = "Data tidak ditemukan"
    
    mocker.patch.object(test_session, "delete", return_value=expected_response)

    response = client.delete("/students/222", headers=headers)

    assert response.status_code == 403


