from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import mapped_column, relationship

class StudentsCourse(Base):
    __tablename__ = 'students_course'

    students_course_id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    student_id = mapped_column(Integer, ForeignKey('student.student_id'), nullable=False)
    course_id = mapped_column(Integer, ForeignKey('course.course_id'), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="students_course")
    course = relationship("Course", back_populates="students_course")

    def serialize(self):
        return {
            "students_course_id": self.students_course_id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<StudentsCourse {self.students_course_id}, student_id={self.student_id}, course_id={self.course_id}>'
