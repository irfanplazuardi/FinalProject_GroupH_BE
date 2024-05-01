import bcrypt
import base64
from cerberus import Validator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request, redirect, url_for

from models.student import Student
from connectors.mysql_connector import connection
from validations.student_schema import student_schema


user_routes_register = Blueprint('user_routes_register', __name__)
Session = sessionmaker(connection)

@user_routes_register.route("/register", methods=['POST'])
def do_registration():
    v = Validator(student_schema)
    json_data = request.get_json()
    print("Received JSON data:", json_data)
    
    if not v.validate(json_data):
        print(v.errors)
        return jsonify({"error": v.errors}), 400


    student_name = json_data.get('student_name')
    student_email = json_data.get('student_email')
    student_birthday = json_data.get('student_birthday')
    phone = json_data.get('phone')
    password = json_data.get('password')
    picture = json_data.get('picture')
    

    if picture:
        try:
            picture = base64.b64decode(picture)
        except Exception:
            picture = None


    with Session() as session:

        existing_student = session.query(Student).filter_by(student_email=student_email).first()
        if existing_student:
            return jsonify({"Already have Account, go to LOGIN"}), 400
        

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        

        new_student = Student(
            student_name=student_name,
            student_email=student_email,
            student_birthday=student_birthday,
            phone=phone,
            password=hashed_password,
            role='student',
            picture=picture
        )
        

        try:
            session.add(new_student)
            session.commit()
            

            return redirect(url_for('user_routes_login.do_user_login'))
        
        except IntegrityError:
            session.rollback()
            return "Failed to register user. Please try again."
        finally:
            session.close()
