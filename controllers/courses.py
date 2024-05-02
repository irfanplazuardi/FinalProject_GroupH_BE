import os
from cerberus import Validator
from flask_login import login_required
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify

from models.course import Course
from connectors.mysql_connector import engine, db
from models.course_subjects import CourseSubjects
from decorators.role_checker import role_required
from validations.course_schema import course_schema, update_course_schema

course_routes = Blueprint('course_routes', __name__)

session = db.session

@course_routes.route('/courses', methods=['GET'])
@login_required
@role_required('student', 'teacher')
def get_courses():

    try:


        courses = session.query(Course).all()
        response_data = {"courses": [course.serialize() for course in courses]}
        print(response_data)

        return jsonify(response_data)
    
    except Exception as e:

        print(f"Error: {e}")
        return jsonify({"error": "Error processing data"}), 500
    
    finally:
        session.close()

@course_routes.route('/courses/<int:course_id>', methods=['GET'])
@login_required
@role_required('student', 'teacher')
def get_course(course_id):

    try:

        course = session.query(Course).filter(Course.course_id == course_id).first()

        if not course:
            return jsonify({"message": "Course not found"}), 404
        
        return jsonify({"course": course.serialize()}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error processing request data"}), 500
    finally:
        session.close()

@course_routes.route("/courses", methods=['POST'])
@login_required
@role_required('teacher')
def create_course():

    v = Validator(course_schema)
    # json_data = request.get_json()
    form_data = request.form
    print("Form data received:", form_data)



    if not form_data:
        return jsonify({"error": "Invalid form data"}), 400
    
    if not v.validate(form_data):
        return jsonify({"error": v.errors}), 400

    
    try:

        new_course = Course(
            course_name=form_data.get['course_name'],
            course_subject_id=form_data.get['course_subject_id'],
            course_description=form_data.get['course_description'],
            picture=form_data.get('picture'),
            course_grade=form_data.get['course_grade'],
        )

        session.add(new_course)
        session.commit()
        return jsonify({"message": "New course has been created successfully"}), 201
    
    except IntegrityError as ie:
        session.rollback()
        print(f"Integrity Error: {ie}")
        return jsonify({"message": f"Integrity Error: {ie}"})
    
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": f"Failed to create new course: {e}"})
    finally:
        session.close()

@course_routes.route("/courses/<int:course_id>", methods=['PUT'])
@login_required
@role_required('teacher')
def update_course(course_id):
    v = Validator(update_course_schema)
    json_data = request.get_json()

    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400

    try:

        course = session.query(Course).filter(Course.course_id == course_id).first()

        if not course:
            return jsonify({"message": "Course not found"}), 404
        
        course.course_name = json_data.get('course_name', course.course_name)
        course.course_subject_id = json_data.get('course_subject_id', course.course_subject)
        course.course_description = json_data.get('course_description', course.course_description)
        course.course_grade = json_data.get('course_grade', course.course_grade)
        course.picture = json_data.get('picture', course.picture)

        session.commit()
        return jsonify({"message": "Course updated successfully"}), 200
    
    except Exception as e:
        session.rollback()
        print(f"Error updating course: {e}")
        return jsonify({"message": "Error updating course"}), 500
    finally:
        session.close()

@course_routes.route("/courses/<int:course_id>", methods=['DELETE'])
@login_required
@role_required('teacher')
def delete_course(course_id):
    try:

        course = session.query(Course).filter(Course.course_id == course_id).first()

        if not course:
            return jsonify({"message": "Course not found"}), 404
        
        session.delete(course)
        session.commit()
        return jsonify({"message": "Course has been deleted"}), 200
    
    except Exception as e:
        print(f"Error deleting course: {e}")
        return jsonify({"message": "Failed to delete course"}), 500
    finally:
        session.close()




