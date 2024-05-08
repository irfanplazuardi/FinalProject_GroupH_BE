from datetime import datetime
import bcrypt
from models.student import Student
from tests.conftest import client,test_session
from sqlalchemy.exc import IntegrityError

def test_registration_failure(client, test_session):

    existing_student = Student(
        student_name="Jane Doe",
        student_email="johndoe@example.com",
        student_birthday=datetime.strptime("2000-01-01", "%Y-%m-%d").date(),
        phone="1234567890",
        password=bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
    )
    test_session.add(existing_student)
    
    try:
        test_session.commit()
    except IntegrityError:
        test_session.rollback()
        return

    new_student_data = {
        "student_name": "John Smith",
        "student_email": "johnsmith@example.com",
        "student_birthday": "2000-02-02",
        "phone": "1234567890", 
        "password": "newpassword123"
    }
    

    response = client.post("/register", json=new_student_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    data = response.get_json()
    assert "error" in data, "Expected 'error' in response"
    assert data["error"] == "Already have Account, go to LOGIN", f"Expected 'Already have Account, go to LOGIN', got {data['error']}"
