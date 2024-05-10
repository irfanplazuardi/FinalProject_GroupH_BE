import json
from unittest.mock import MagicMock

from models.announcement import Announcement


def login(client):
    response = client.post('/login', json={
        'input_value': 'sad',
        'password': '12345678',
        'role_as': 'teacher'
    })
    print("Login response status code:", response.status_code)
    print("Login response JSON:", response.get_json())

    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    return data['access_token']



def test_get_announcements(client):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = client.get('/announcement', headers=headers)

    assert response.status_code == 200, "Failed to retrieve announcements"

    data = response.get_json()
    assert isinstance(data, dict), "Data format incorrect"
    assert "announcements" in data, "Announcements key missing in response"
    

    
def test_get_announcement(client, mocker, test_session):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    announcement_id = 2
    mock_announcement = {
        "announcement": {
            "id": announcement_id,
            "announcement_desc": "First announcement"
        }
    }

    mock_announcement = mocker.patch.object(test_session.query(Announcement), 'filter_by').return_value.first.return_value
    mock_announcement.announcement_desc = "First announcement"

    response = client.get(f'/announcement/{announcement_id}', headers=headers)

    assert response.status_code == 200


    
def test_create_announcement(client):

    access_token = login(client)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


    announcement_data = {
        "announcement_desc": "New announcement"
    }
    
    response = client.post(
        '/announcement',
        data=json.dumps(announcement_data),
        headers=headers
    )
    
    assert response.status_code == 201, "Failed to create new announcement"
    data = response.get_json()
    assert data.get("message") == "New announcement created successfully", "Unexpected message"
    
def test_update_announcement(client, mocker, test_session):
    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    announcement_id = 2
    updated_announcement_data = {
        "announcement_desc": "Updated announcement"
    }

    mock_response = {
        "message": "Announcement updated successfully"
    }

    mock_announcement = mocker.patch.object(test_session.query(Announcement), 'filter_by').return_value.first.return_value
    mock_announcement.announcement_desc = "Updated announcement"

    response = client.put(
        f'/announcement/{announcement_id}',
        data=json.dumps(updated_announcement_data),
        headers=headers
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data == mock_response
    assert mock_announcement.announcement_desc == updated_announcement_data['announcement_desc']
    
def test_delete_announcement_not_found(client, mocker):

    access_token = login(client)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


    expected_response = "data not Found"

    mocker.patch.object(Announcement, "query", return_value=expected_response)

    response = client.delete("/announcement/232", headers=headers)

    assert response.status_code == 404
