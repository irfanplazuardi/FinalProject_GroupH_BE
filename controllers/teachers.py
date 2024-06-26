import os
from cerberus import Validator
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from models.teacher import Teacher
from connectors.mysql_connector import engine, db
from decorators.role_checker import role_required
from validations.teacher_schema import teacher_schema, update_teacher_schema


teacher_routes = Blueprint('teacher_routes', __name__)

session = db.session


@teacher_routes.route('/teachers', methods = ['GET'])
@jwt_required()
@role_required('student', 'teacher')
def get_teachers():

    try:
        teachers = session.query(Teacher).all()
        response_data = {"teachers": [teacher.serialize() for teacher in teachers]}
        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error processing data"}), 500
    
    finally:
        session.close()

@teacher_routes.route("/teachers/<int:teacher_id>", methods=['GET'])
@jwt_required()
@role_required('student', 'teacher')
def get_teacher(teacher_id):

    try:


        teacher = session.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()

        if not teacher:
            return jsonify({"message": "Teacher not Found"}), 404
        
        return jsonify({"teacher": teacher.serialize()}), 201
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": " Error processing request data"}), 500
    
    finally:
        session.close()

@teacher_routes.route("/teachers", methods=['POST'])
@jwt_required()
@role_required('teacher')
def create_teacher():

    v = Validator(teacher_schema)
    json_data = request.get_json()

    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400
    
    try:


        new_teacher = Teacher(
            teacher_name=json_data['teacher_name'],
            teacher_email=json_data['teacher_email'],
            teacher_birthday=json_data['teacher_birthday'],
            phone=json_data['phone'],
            password=json_data['password'],
            picture=json_data.get('picture').encode() if json_data.get('picture') else None,
            role = 'teacher'
        )

        new_teacher.set_password(json_data['password'])

        session.add(new_teacher)
        session.commit()

        return jsonify({"message": "New Teacher Data has been created successfully"})
    
    except IntegrityError as ie:
        session.rollback()
        print(f"Integrity Error: {ie}")
        return jsonify({"message": f"Integrity Error: {ie}"})
    
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": f"Failed create New Data: {e}"})
    
    finally:
        session.close()

@teacher_routes.route("/teachers/<int:teacher_id>", methods=['PUT'])
@jwt_required()
@role_required('teacher')
def update_teacher(teacher_id):
    json_data  = request.get_json()

    if json_data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    v = Validator(update_teacher_schema)
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400

    try:

        teacher = session.query(Teacher).filter_by(teacher_id=teacher_id).first()

        if not teacher:
            return jsonify({"message": "Teacher not found"}), 404

        field_map = {
            "teacher_name": "teacher_name",
            "teacher_email": "teacher_email",
            "teacher_birthday": "teacher_birthday",
            "phone": "phone",
            "picture": "picture",
            "password": "password",
        }

        for json_key, model_attr in field_map.items():
            if json_key in json_data:
                setattr(teacher, model_attr, json_data[json_key])

        if 'password' in json_data:
            teacher.set_password(json_data['password'])

        session.commit()
        
        return jsonify({"message": "Data successfully updated"}), 200
    
    except Exception as e:
        print(f"Error updating data: {e}")
        
        return jsonify({"message": "Error updating data"}), 500
    
    finally:
        session.close()

@teacher_routes.route("/teachers/<int:teacher_id>", methods=['DELETE'])
@jwt_required()
@role_required('teacher')
def delete_teacher(teacher_id):

    try:



        teacher = session.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()

        if not teacher:
            return jsonify({"message": "Data Doesn't Match"}), 404
        
        session.delete(teacher)
        session.commit()
        return jsonify({"message": "Data has been DELETED"}), 200

    except Exception as e:
        print(f"Error deleting: {e}")
        return jsonify({"message": "Failed delete data"}), 500
    
    finally:
        session.close()

