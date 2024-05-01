import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from models.course import Course
from models.student import Student
from connectors.mysql_connector import engine
from decorators.role_checker import role_required
from models.students_course import StudentsCourse

students_course_routes = Blueprint('students_course_routes', __name__)

Session = sessionmaker(bind=engine)

@students_course_routes.route("/students_course", methods=['GET'])
@login_required
@role_required('student')
def get_all_students_course():

    session = Session()

    try:
        students_courses = session.query(StudentsCourse).all()
        results = [tc.serialize() for tc in students_courses]
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({"message": f"Something wrong: {e}"}), 400
    
    finally:
        session.close()

@students_course_routes.route("/students_course/<int:students_course_id>", methods=['GET'])
@login_required
@role_required('student')
def get_students_course(students_course_id):

    session = Session()

    try:
        students_course = session.query(StudentsCourse).get(students_course_id)
        if not students_course:
            return jsonify({"message": f"Courses not found"}), 404
        
        return jsonify(students_course.serialize()), 200
    
    except Exception as e:
        return jsonify({"message": f"Failed to get data {e}"})
    
    finally:
        session.close()

@students_course_routes.route("/students_course", methods=['POST'])
@login_required
@role_required('student')
def create_students_course():

    student_id = request.form.get('student_id')
    course_id = request.form.get('course_id')
    
    if not student_id or not course_id:
        return jsonify({"error": "Invalid form data"}), 400
    
    session = Session()

    try:

        student = session.query(Student).get(student_id)
        course = session.query(Course).get(course_id)

        if not student or not course:
            return jsonify({"error": "Invalid student or Course ID"}), 400
        
        new_students_course = StudentsCourse(
            student_id = current_user.student_id,
            course_id = course_id

        )

        session.add(new_students_course)
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
    
@students_course_routes.route("/students_course/<int:students_course_id>", methods=['PUT'])
@login_required
@role_required('student')
def update_students_course(students_course_id):
    
    student_id = request.form.get('student_id')
    course_id = request.form.get('course_id')


    if not student_id or not course_id:
        return jsonify({"error": "Invalid form data"}), 400

    session = Session()
    try:

        students_course = session.query(StudentsCourse).get(students_course_id)
        if not students_course:
            return jsonify({"error": "Course not found"}), 404

        students_course.student_id = student_id
        students_course.course_id = course_id

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

@students_course_routes.route("/students_course/<int:students_course_id>", methods=['DELETE'])
@login_required
@role_required('student')
def delete_students_course(students_course_id):
    session = Session()
    try:
        students_course = session.query(StudentsCourse).get(students_course_id)
        if not students_course:
            return jsonify({"error": "Course not found"}), 404
        

        session.delete(students_course)
        session.commit()
        return jsonify({"message": "Deleted successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"message": f"Failed to delete data: {e}"}), 400
    finally:
        session.close()
