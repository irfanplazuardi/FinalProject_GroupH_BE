
import os
from cerberus import Validator
from flask_login import login_required
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify

from models.course import Course
from connectors.mysql_connector import engine
from models.course_subjects import CourseSubjects
from decorators.role_checker import role_required
from validations.course_subjects_schema import course_subjects_schema

course_subjects_routes = Blueprint('course_subjects_routes', __name__)

Session = sessionmaker(bind=engine)


@course_subjects_routes.route("/course-subjects", methods=['GET'])
@login_required
@role_required('student', 'teacher')
def get_course_subjects():
    try:
        session = Session()
        course_subjects = session.query(CourseSubjects).all()
        response_data = {"course_subjects": [cs.serialize() for cs in course_subjects]}
        return jsonify(response_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error processing data"}), 500
    finally:
        session.close()

@course_subjects_routes.route("/course-subjects/<int:course_subject_id>", methods=['GET'])
@login_required
@role_required('student', 'teacher')
def get_course_subject(course_subject_id):
    try:
        session = Session()
        course_subject = session.query(CourseSubjects).filter(CourseSubjects.course_subject_id == course_subject_id).first()

        if not course_subject:
            return jsonify({"message": "Course subject not found"}), 404
        
        return jsonify({"course_subject": course_subject.serialize()}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error processing request data"}), 500
    finally:
        session.close()

@course_subjects_routes.route("/course-subjects", methods=['POST'])
@login_required
@role_required('teacher')
def create_course_subject():
    v = Validator(course_subjects_schema)
    json_data = request.get_json()

    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400
    
    try:
        session = Session()
        new_course_subject = CourseSubjects(
            course_subject=json_data['course_subject']
        )

        session.add(new_course_subject)
        session.commit()
        return jsonify({"message": "New course subject has been created successfully"}), 201
    
    except IntegrityError as ie:
        session.rollback()
        print(f"Integrity Error: {ie}")
        return jsonify({"message": f"Integrity Error: {ie}"})
    
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": f"Failed to create new course subject: {e}"})
    finally:
        session.close()

@course_subjects_routes.route("/course-subjects/<int:course_subject_id>", methods=['PUT'])
@login_required
@role_required('teacher')
def update_course_subject(course_subject_id):
    v = Validator(course_subjects_schema)
    json_data = request.get_json()

    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400

    try:
        session = Session()
        course_subject = session.query(CourseSubjects).filter(CourseSubjects.course_subject_id == course_subject_id).first()

        if not course_subject:
            return jsonify({"message": "Course subject not found"}), 404
        
        course_subject.course_subject = json_data.get('course_subject', course_subject.course_subject)

        session.commit()
        return jsonify({"message": "Course subject updated successfully"}), 200
    
    except Exception as e:
        session.rollback()
        print(f"Error updating course subject: {e}")
        return jsonify({"message": "Error updating course subject"}), 500
    finally:
        session.close()

@course_subjects_routes.route("/course-subjects/<int:course_subject_id>", methods=['DELETE'])
@login_required
@role_required('teacher')
def delete_course_subject(course_subject_id):
    try:
        session = Session()
        course_subject = session.query(CourseSubjects).filter(CourseSubjects.course_subject_id == course_subject_id).first()

        if not course_subject:
            return jsonify({"message": "Course subject not found"}), 404
        
        session.delete(course_subject)
        session.commit()
        return jsonify({"message": "Course subject has been deleted"}), 200
    
    except Exception as e:
        print(f"Error deleting course subject: {e}")
        return jsonify({"message": "Failed to delete course subject"}), 500
    finally:
        session.close()