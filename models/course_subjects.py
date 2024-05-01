from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship

class CourseSubjects(Base):
    __tablename__ = 'course_subjects'

    course_subject_id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    course_subject = mapped_column(String(25), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    course = relationship("Course", back_populates="course_subject")
    
    def serialize(self):
        return {
            "course_subject_id": self.course_subject_id,
            "course_subject": self.course_subject,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<CourseSubjects {self.course_subject_id}, course_subject={self.course_subject}>'
