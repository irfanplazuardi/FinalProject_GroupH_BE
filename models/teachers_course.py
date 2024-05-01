from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import mapped_column, relationship

class TeachersCourse(Base):
    __tablename__ = 'teachers_course'

    teachers_course_id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    teacher_id = mapped_column(Integer, ForeignKey('teacher.teacher_id'), nullable=False)
    course_id = mapped_column(Integer, ForeignKey('course.course_id'), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    teacher = relationship("Teacher", back_populates="teachers_course")
    course = relationship("Course", back_populates="teachers_course")

    def serialize(self):
        return {
            "teachers_course_id": self.teachers_course_id,
            "teacher_id": self.teacher_id,
            "course_id": self.course_id,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<TeachersCourse {self.teachers_course_id}, teacher_id={self.teacher_id}, course_id={self.course_id}>'
