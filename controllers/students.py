from cerberus import Validator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from models.student import Student
from connectors.mysql_connector import engine, db
from decorators.role_checker import role_required
from validations.student_schema import student_schema
from validations.update_student_schema import update_student_schema


student_routes = Blueprint('student_routes', __name__)

session = db.session

@student_routes.route("/students", methods=['GET'])
@login_required
@role_required('student', 'teacher')
def get_students():
    try:

        students = session.query(Student).all()
        response_data = {"students": [student.serialize() for student in students]}
        return jsonify(response_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error processing data"}), 500
    finally:
        session.close()

@student_routes.route("/students/<int:student_id>", methods=['GET'])
@login_required
@role_required('student', 'teacher')
def get_student(student_id):

    try:


        student = session.query(Student).filter(Student.student_id == student_id).first()

        if not student:
            return jsonify({"message": "Student not found"}), 404
        return jsonify({"student": student.serialize()})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error processing data"}), 500
    
    finally:
        session.close()


@student_routes.route("/students", methods=['POST'])
@login_required
@role_required('teacher')
def create_student():

    v = Validator(student_schema)
    json_data = request.get_json()


    if not json_data:
        print(json_data)
        return jsonify({"error": "Invalid JSON data"}), 400

    if not v.validate(json_data):
        print(v.errors)
        return jsonify({"error": v.errors}), 400
    
    try:

        if current_user.role != 'teacher':
            return jsonify({"error": "Forbidden: Only teachers can create new student data"}), 403

        new_student = Student(
            student_name=json_data['student_name'],
            student_email=json_data['student_email'],
            student_birthday=json_data['student_birthday'],
            phone=json_data['phone'],
            password=json_data['password'],
            picture=json_data.get('picture').encode() if json_data.get('picture') else None 
        )

        new_student.set_password(json_data['password'])

        session.add(new_student)
        session.commit()

        return jsonify({"message": "Student created successfully"}), 201
    

    except IntegrityError as ie:

        session.rollback()
        print(f"Integrity Error: {ie}")
        return jsonify({"error": f"Integrity error: {ie}"}), 409

    except Exception as e:

        session.rollback()
        print(f"Error: {e}")
        return jsonify({"error": f"Failed to create student: {e}"}), 500
    
    finally:
        session.close()

@student_routes.route("/students/<int:student_id>", methods=['PUT'])
@login_required
@role_required('student', 'teacher')
def update_student(student_id):

    v = Validator(update_student_schema)
    json_data = request.get_json()


    if not json_data:
        return jsonify({"error": "Invalid data"}), 400

    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400

    try:

        student = session.query(Student).filter(Student.student_id == student_id).first()

        if not student:
            return jsonify({"message": "Student not found"}), 404

        if current_user.role == 'student' and student.student_id != current_user.student_id:
            return jsonify({"message": "Unauthorized"}), 403
        

        

        field_map = {
            "student_name": "student_name",
            "student_email": "student_email",
            "student_birthday": "student_birthday",
            "phone": "phone",
            "picture": "picture",
        }

        for key, attr in field_map.items():
            if key in json_data:
                setattr(student, attr, json_data[key])

        if 'password' in json_data:
            student.set_password(json_data['password'])

        session.commit()

        return jsonify({"message": "Student updated successfully"}), 200

    except Exception as e:

        session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": "Failed to update student"}), 500

    finally:
        session.close()

@student_routes.route("/students/<int:student_id>", methods=['DELETE'])
@login_required
@role_required('teacher')
def delete_student(student_id):
    
    try:

        student = session.query(Student).filter(Student.student_id == student_id).first()

        if not student:
            return jsonify({"message": "Student not found"}), 404

        session.delete(student)
        session.commit()

        return jsonify({"message": "Student deleted successfully"}), 200
    
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": "Failed to delete student"}), 500
    
    finally:
        session.close()

