from database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    userName = Column(String, unique=True, index=True)
    password = Column(String)
    userMail = Column(String)
    phone = Column(String)
    address = Column(String)
    role = Column(String)
    created_by = Column(Integer)
