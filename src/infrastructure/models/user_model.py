from sqlalchemy import Column, Integer, String, DateTime, Boolean
from infrastructure.databases.base import Base
from datetime import datetime


class UserModel(Base):
    __tablename__ = 'flask_user'
    # __table_args__ = {'extend_existing': True}  # Thêm dòng này
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_name = Column(String(18), nullable=False,unique= True)
    password = Column(String(18), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(Boolean, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime) 
    status = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserModel id={self.id} user_name='{self.user_name}'>"