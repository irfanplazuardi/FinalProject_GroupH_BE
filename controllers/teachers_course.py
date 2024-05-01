import os
from flask_login import login_required
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify

from models.course import Course
from models.teacher import Teacher
from connectors.mysql_connector import engine
from models.teachers_course import TeachersCourse
from decorators.role_checker import role_required

teachers_course_routes = Blueprint('teachers_course_routes', __name__)

Session = sessionmaker(bind=engine)

@teachers_course_routes.route("/teachers_course", methods=['GET'])
@login_required
@role_required('teacher')
def get_all_teachers_course():

    session = Session()

    try:
        teachers_courses = session.query(TeachersCourse).all()
        results = [tc.serialize() for tc in teachers_courses]
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({"message": f"Something wrong: {e}"}), 400
    
    finally:
        session.close()

@teachers_course_routes.route("/teachers_course/<int:teachers_course_id>", methods=['GET'])
@login_required
@role_required('teacher')
def get_teachers_course(teachers_course_id):

    session = Session()

    try:
        teachers_course = session.query(TeachersCourse).get(teachers_course_id)
        if not teachers_course:
            return jsonify({"message": f"Courses not found"}), 404
        
        return jsonify(teachers_course.serialize()), 200
    
    except Exception as e:
        return jsonify({"message": f"Failed to get data {e}"})
    
    finally:
        session.close()

@teachers_course_routes.route("/teachers_course", methods=['POST'])
@login_required
@role_required('teacher')
def create_teachers_course():

    teacher_id = request.form.get('teacher_id')
    course_id = request.form.get('course_id')

    if not teacher_id or not course_id:
        return jsonify({"error": "Invalid form data"}), 400
    
    session = Session()

    try:

        teacher = session.query(Teacher).get(teacher_id)
        course = session.query(Course).get(course_id)

        if not teacher or not course:
            return jsonify({"error": "Invalid Teacher or Course ID"}), 400
        
        new_teachers_course = TeachersCourse(
            teacher_id = teacher_id,
            course_id = course_id

        )

        session.add(new_teachers_course)
        session.commit()

        return jsonify({"success": "data  created successfully"}), 200
    
    except IntegrityError as ie:
        session.rollback()
        return jsonify({"message": f"Integrity Error: {ie}"}), 400
    
    except Exception as e:
        session.rollback()
        return jsonify({"message": f"Failed to add data {e}"}), 400
    
    finally:
        session.close()
    
@teachers_course_routes.route("/teachers_course/<int:teachers_course_id>", methods=['PUT'])
@login_required
@role_required('teacher')
def update_teachers_course(teachers_course_id):
    
    teacher_id = request.form.get('teacher_id')
    course_id = request.form.get('course_id')


    if not teacher_id or not course_id:
        return jsonify({"error": "Invalid form data"}), 400

    session = Session()
    try:

        teachers_course = session.query(TeachersCourse).get(teachers_course_id)
        if not teachers_course:
            return jsonify({"error": "Course not found"}), 404

        teachers_course.teacher_id = teacher_id
        teachers_course.course_id = course_id

        session.commit()
        return jsonify({"message": "Course updated successfully"}), 200
    except IntegrityError as ie:
        session.rollback()
        return jsonify({"message": f"Integrity Error: Course not Found {ie}"}), 400
    except Exception as e:
        session.rollback()
        return jsonify({"message": f"Failed to update: {e}"}), 400
    finally:
        session.close()

@teachers_course_routes.route("/teachers_course/<int:teachers_course_id>", methods=['DELETE'])
@login_required
@role_required('teacher')
def delete_teachers_course(teachers_course_id):
    session = Session()
    try:
        teachers_course = session.query(TeachersCourse).get(teachers_course_id)
        if not teachers_course:
            return jsonify({"error": "Course not found"}), 404
        

        session.delete(teachers_course)
        session.commit()
        return jsonify({"message": "Deleted successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"message": f"Failed to delete data: {e}"}), 400
    finally:
        session.close()


