from sqlalchemy import String,Column,Integer
from src.database.db import Base

class User(Base):
    __tablename__= "users"

    id = Column(Integer,primary_key=True, index=True)
    hashed_password = Column(String(255)) 
    name = Column(String(255))
    email = Column(String(255))