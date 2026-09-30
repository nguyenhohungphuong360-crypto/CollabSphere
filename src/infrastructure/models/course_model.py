from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Column, Integer, String, DateTime, Date
from infrastructure.databases.base import Base
from datetime import datetime


class CourseModel(Base):
    __tablename__ = 'courses'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime) 
    
    # ORM: Object Relational Mapping
    # Anhs xa giua database va object trong code
    status = Column(String(50), nullable=False, default="active")
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<CourseModel id={self.id} course_name='{self.course_name}'>"