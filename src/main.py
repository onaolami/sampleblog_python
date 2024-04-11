from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel,Field
from typing import Annotated
from src.models.comment import Comment
from src.models.post import Post
#from src.models.user import User
from src.database.db import engine,SessionLocal,Base
from sqlalchemy.orm import Session
import src.auth

load_dotenv()

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(src.auth.router)


class PostBase(BaseModel):
    title: str
    content:str
    user_id: int


class CommentBase(BaseModel):
    body:str
    user_id:int
    post_id:int

class UserCreate(BaseModel):
    name:str
    email:str 
    password:str 



def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]

#USER
#CREATE USER






#CREATE 
#GET
#GETALL
#SEARCH
#DELETE

# CREATE POST
@app.post("/post/",status_code=status.HTTP_201_CREATED)
async def create_post(post:PostBase, db:db_dependency):
    db_post = Post(**post.model_dump())
    db.add(db_post)
    db.commit()



#GET POST
@app.get("/post/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db:db_dependency):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post was not found")
    return post


#GET ALL POSTS
@app.get("/posts/", status_code=status.HTTP_200_OK)
async def getall_post( db:db_dependency):
    post = db.query(Post).all()
    if post is None:
       return[]
      
    return post


#SEARCH FOR POST
@app.get("/post/search/", status_code=status.HTTP_200_OK)
async def search_posts(title: str,db:db_dependency):
    post = db.query(Post).filter(Post.title.contains(title)).all()
    if post is None:
      raise HTTPException(status_code=404, detail=title+" not found")
    return post


#DELETE POST
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(post_id:int, db:db_dependency):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail= "Post not found")
    db.delete(db_post)
    db.commit()


#COMMENT
#CREATE
#GET ALL
#DELETE
    

#CREATE COMMENTS
@app.post("/comments/", status_code=status.HTTP_201_CREATED)
async def create_comments(comment:CommentBase, db:db_dependency):
    db_comment = Comment(**comment.model_dump())
    db.add(db_comment)
    db.commit()


#GET ALL COMMENTS
@app.get("/comments/", status_code=status.HTTP_200_OK)
async def getall_comments(db:db_dependency):
    comment = db.query(Comment).all()
    if comment is None:
        return []
      
    return comment


#DELETE COMMENTS
@app.delete("/comment/{comment_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_comments(comment_id:int, db:db_dependency):
    db_comment= db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        HTTPException(status_code=404, detail="Comment not found")
    db.delete(db_comment)
    db.commit()


      

