from sqlalchemy import Boolean,String,Integer,Column,DateTime
from src.database.db import Base
from datetime import datetime


class Comment(Base):
   __tablename__= "comments" 

   id = Column(Integer,primary_key=True, index=True)
   body = Column(String(500))
   created_at = Column(DateTime,default=datetime.now())
   user_id = (Integer)
   post_id = (Integer)