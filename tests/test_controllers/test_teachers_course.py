
from models.teachers_course import TeachersCourse

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


def test_get_teachers_courses(client):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = client.get('/teachers_course', headers=headers)
    assert response.status_code == 200, "Failed to retrieve teachers' courses"

    data = response.get_json()
    assert isinstance(data, list), "Expected a list of teachers' courses"

def test_get_teachers_course(client, test_session):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    teachers_course_id = 1
    
    response = client.get(f'/teachers_course/{teachers_course_id}', headers=headers)
    assert response.status_code == 200, "Failed to retrieve the teachers' course"

    data = response.get_json()
    assert 'teacher_id' in data, "teacher ID not found in response"
    assert 'course_id' in data, "Course ID not found in response"


def test_create_teachers_course(client, mocker, test_session):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    teachers_course_data = {
        'course_id': '5'
    }

    mocker.patch.object(test_session, 'add')
    mocker.patch.object(test_session, 'commit')

    response = client.post('/teachers_course', json=teachers_course_data, headers=headers)

    assert response.status_code == 400, 'Invalid Form Data'



def test_delete_teachers_course(client, mocker):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


    expected_response = "data not Found"

    mocker.patch.object(TeachersCourse, "query", return_value=expected_response)

    response = client.delete("/teachers_course/232", headers=headers)

    assert response.status_code == 404