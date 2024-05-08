from flask import Blueprint, jsonify, redirect, request
from flask_login import logout_user
from models.student import Student
from models.teacher import Teacher
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, current_user
from sqlalchemy.orm import sessionmaker
from connectors.mysql_connector import db

user_routes_login = Blueprint('user_routes_login', __name__)

session = db.session

@user_routes_login.route("/login", methods=['POST'])
def do_user_login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid JSON data"}), 400

    input_value = data.get('input_value')
    password = data.get('password')
    role_as = data.get('role_as')

    if not input_value or not password or role_as not in ['student', 'teacher']:
        return jsonify({"message": "Email/Name, password, and role_as (student or teacher) are required"}), 400

    if not input_value or not password:
        return jsonify({"message": "Email/Name and password are required"}), 400

    with session() as s:

        if role_as == 'student':
            user = s.query(Student).filter(
            (Student.student_email == input_value) | (Student.student_name == input_value)).first()
        
        else:
            user = s.query(Teacher).filter(
            (Teacher.teacher_email == input_value) | (Teacher.teacher_name == input_value)).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        if not user.check_password(password):
            return jsonify({"message": "Incorrect password"}), 401
        
        if user.role != role_as:
                    return jsonify({"message": "Incorrect role"}), 403

        if isinstance(user, Student):
            user_id = user.student_id
            username = user.student_name
            role = 'student'
        elif isinstance(user, Teacher):
            user_id = user.teacher_id
            username = user.teacher_name
            role = 'teacher'
        else:
            return jsonify({"message": "bukan user type"}), 500

        user_id = user.student_id if role_as == 'student' else user.teacher_id
        username = user.student_name if role_as == 'student' else user.teacher_name

        # Create access token
        access_token = create_access_token(
            identity=user_id,
            additional_claims={
                "username": username,
                "role": role
            }
        )

        return jsonify({
            "access_token": access_token,
            "role": role,
            "user_id": user_id
        }), 200

