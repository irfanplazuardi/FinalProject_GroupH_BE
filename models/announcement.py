from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, DateTime, Text

class Announcement(Base):
    __tablename__ = 'announcement'

    announcement_id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    teacher_id = mapped_column(Integer, ForeignKey('teacher.teacher_id'), nullable=False)
    announcement_desc = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by = mapped_column(String(25), nullable=False)

    teacher = relationship("Teacher", back_populates="announcements")

    def serialize(self):
        return {
            "announcement_id": self.announcement_id,
            "teacher_id": self.teacher_id,
            "announcement_desc": self.announcement_desc,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "created_by": self.created_by
        }

    def __repr__(self):
        return f'<Announcement {self.announcement_id}, created_by={self.created_by}>'
