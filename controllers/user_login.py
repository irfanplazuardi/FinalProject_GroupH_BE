from models.student import Student
from models.teacher import Teacher

from sqlalchemy.orm import sessionmaker
from connectors.mysql_connector import engine
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token
from flask import Blueprint, jsonify, request, redirect

user_routes_login = Blueprint('user_routes_login', __name__)

connection = engine.connect()
Session = sessionmaker(connection)
session = Session()

@user_routes_login.route("/login", methods=['GET'])
def user_login():

    return jsonify("welcome to login page")

@user_routes_login.route("/login", methods=['POST'])
def do_user_login():

    data = request.get_json()
    if data is None:
        return jsonify({"message": "Invalid JSON data"}), 400


    input_value = data.get('input_value')
    password = data.get('password')


    print(f"Received input_value: {input_value}")
    print(f"Received password: {password}")


    if not input_value or not password:
        return jsonify({"message": "Email/Name and password are required"}), 400


    with Session() as session:

        user = session.query(Student).filter((Student.student_email == input_value) | (Student.student_name == input_value)).first() or \
               session.query(Teacher).filter((Teacher.teacher_email == input_value) | (Teacher.teacher_name == input_value)).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        if not user.check_password(password):
            return jsonify({"message": "Incorrect password"}), 401

        login_user(user, remember=False)

        if hasattr(user, 'student_id'):
            user_identity = user.student_id
        elif hasattr(user, 'teacher_id'):
            user_identity = user.teacher_id
        else:

            return jsonify({"message": "User identity attribute not found"}), 500


        access_token = create_access_token(
            identity=user_identity,
            additional_claims={
                "username": getattr(user, 'user_name', getattr(user, 'student_name', None)),
                "role": 'teacher' if hasattr(user, 'teacher_id') else 'student'
            }
        )

        return jsonify({"access_token": access_token, "role": "teacher" if hasattr(user, "teacher_id") else "student"})



@user_routes_login.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return redirect('/')

