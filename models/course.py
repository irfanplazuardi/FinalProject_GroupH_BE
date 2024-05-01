from models.base import Base
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Enum, ForeignKey, Integer, String, DateTime, Text, LargeBinary

class Course(Base):
    __tablename__ = 'course'

    course_id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    course_name = mapped_column(String(50), nullable=False)
    course_subject_id= mapped_column(Integer, ForeignKey('course_subjects.course_subject_id'), nullable=False)
    course_description = mapped_column(Text, nullable=False)
    picture = mapped_column(LargeBinary, nullable=True)
    course_grade = mapped_column(Enum("SD", "SMP", "SMA"), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    course_subject = relationship("CourseSubjects", back_populates="course")
    teachers_course = relationship("TeachersCourse", back_populates="course")
    students_course = relationship("StudentsCourse", back_populates="course")


    def serialize(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "course_subjects": self.course_subject.course_subject,
            "course_description": self.course_description,
            "picture": self.picture,
            "course_grade": self.course_grade,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<Course {self.course_id}, course_name={self.course_name}>'
