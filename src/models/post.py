from sqlalchemy import Boolean,Column,String,Integer,DateTime
from src.database.db import Base
from datetime import datetime


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True )
    title = Column(String(455))
    content = Column(String(455))
    created_at = Column(DateTime,default=datetime.now())
    user_id = Column(Integer)