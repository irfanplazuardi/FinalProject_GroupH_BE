from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from connectors.mysql_connector import engine, connection, db, sql_string
from sqlalchemy.orm import sessionmaker

import os
from models.student import Student
from models.teacher import Teacher
from flask_jwt_extended import JWTManager
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

app=Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = sql_string
# JWT
jwt = JWTManager(app)

db.init_app(app)

migrate = Migrate(app, db)

with app.app_context():
    db.create_all()




# LOGIN SESSION
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    student = session.query(Student).filter_by(student_id=int(user_id)).first()
    if student:
        session.close()
        return student
    

    teacher = session.query(Teacher).filter_by(teacher_id=int(user_id)).first()
    session.close()
    return teacher

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

    Session = sessionmaker(connection)
    with Session() as session:


        students = session.query(Student).all()
        student_data = [{"ID": student.student_id, "Name": student.student_name} for student in students]


        teachers = session.query(Teacher).all()
        teacher_data = [{"ID": teacher.teacher_id, "Name": teacher.teacher_name} for teacher in teachers]


    data = {
        "students": student_data,
        "teachers": teacher_data
    }
    

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
