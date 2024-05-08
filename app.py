from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request
from waitress import serve
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from connectors.mysql_connector import engine, connection, db, sql_string
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS

import os
from models.student import Student
from models.teacher import Teacher
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, current_user
from flask_login import LoginManager

from controllers.courses import course_routes
from controllers.students import student_routes
from controllers.teachers import teacher_routes
from controllers.user_login import user_routes_login
from controllers.announcement import announcement_routes
from controllers.user_register import user_routes_register
from controllers.course_subjects import course_subjects_routes
from controllers.teachers_course import teachers_course_routes
from controllers.students_course import students_course_routes




load_dotenv()


def create_app():
    app=Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = sql_string

    # JWT
    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)


    with app.app_context():
        db.create_all()


    @jwt.user_lookup_loader
    def load_user(jwt_header, jwt_data):
        user_id = jwt_data["sub"]
        user_role = jwt_data.get("role") 

        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        try:

            if user_role == "teacher":

                teacher = session.query(Teacher).filter_by(teacher_id=user_id).first()
                if teacher:
                    return teacher.serialize()
            elif user_role == "student":

                student = session.query(Student).filter_by(student_id=user_id).first()
                if student:
                    return student.serialize()

            return None
        
        finally:

            session.close()
    
    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected_route():

        return jsonify({
            "message": "protected - route",
            "user": {
                "id": current_user.student_id if hasattr(current_user, "student_id") else current_user.teacher_id,
                "name": current_user.student_name if hasattr(current_user, "student_name") else current_user.teacher_name,
                "role": "student" if hasattr(current_user, "student_id") else "teacher"                
            }
        }),200

    app.register_blueprint(student_routes)
    app.register_blueprint(teacher_routes)
    app.register_blueprint(user_routes_register)
    app.register_blueprint(user_routes_login)
    app.register_blueprint(announcement_routes)
    app.register_blueprint(course_routes)
    app.register_blueprint(course_subjects_routes)
    app.register_blueprint(teachers_course_routes)
    app.register_blueprint(students_course_routes)



    # Product Route
    @app.route("/")
    def hello_world():
        document_url = "https://documenter.getpostman.com/view/32945632/2sA3JFCQyG"
        return redirect(document_url)

    return app

if __name__ == "__main__":

    app = create_app()
    try:

        port = os.getenv("PORT", default=8080)

        if not port.isdigit():
            port=8080
        port = int(port)

        serve(app, host="0.0.0.0", port=port)

    except Exception as e:
        print(f"Terjadi kesalahan saat menjalankan server: {e}")


