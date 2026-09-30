from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases.base import Base
from datetime import datetime


class TodoModel(Base):
    __tablename__ = 'todos'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime) 
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TodoModel id={self.id} title='{self.title}'>"