import base64
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, LargeBinary, String, DateTime, func, Date

import bcrypt

from models.base import Base


class Teacher(Base):
    __tablename__ = 'teacher'

    teacher_id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    teacher_name = mapped_column(String(30), nullable=False, unique=True)
    teacher_email = mapped_column(String(50), nullable=False, unique=True)
    teacher_birthday = mapped_column(Date, nullable=False)
    phone = mapped_column(String(20), nullable=False, unique=True)
    picture = mapped_column(LargeBinary, nullable=True)
    password = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    role = mapped_column(String(20), default='teacher', nullable=False)

    announcements = relationship("Announcement", back_populates="teacher")
    teachers_course = relationship("TeachersCourse", back_populates="teacher")

    def set_password(self, password):
        self.password = bcrypt.hashpw( password.encode('utf-8') , bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def get_id(self):
        return str(self.teacher_id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.teacher_id)
    
    def serialize(self):

        if self.picture:
            picture_base64 = base64.b64encode(self.picture).decode('utf-8')
        else:
            picture_base64 = None
        
        return {
            "teacher_id": self.teacher_id,
            "teacher_name": self.teacher_name,
            "teacher_email": self.teacher_email,
            "teacher_birthday": self.teacher_birthday,
            "phone": self.phone, 
            "picture": picture_base64,
            "password": self.password,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "role": self.role
        }
    
    def __repr__(self):
        return f'<Teacher {self.teacher_id}, teacher_name={self.teacher_name}, teacher_email={self.teacher_email}, teacher_birthday={self.teacher_birthday}, phone={self.phone}, password={self.password}>'