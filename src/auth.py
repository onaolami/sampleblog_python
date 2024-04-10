from datetime import timedelta,datetime
import os
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field,field_validator,EmailStr
from sqlalchemy.orm import Session
from starlette import status
from src.database.db import SessionLocal
from src.models.user import User
from src.database.db import engine
from passlib.context import CryptContext
from jose import jwt, JWTError
from uuid import UUID,uuid4

router = APIRouter(
    prefix='/auth',
    tags= ['auth']
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
   name: str
   email: EmailStr
   password: str #= Field(min_length=5, max_length=12)

   class Config:
      json_schema_extra = {
         'example': {
            'name': 'onaola chidera',
            'email': 'onaola@gmail.com',
            'password': 'test1234@'
            
         }
      }


   @field_validator('password')
   def password_validator(cls,value):
      if value == 'test1234@':
         raise ValueError('Please do not use default password..')
      return value


#class User(CreateUserRequest):
    #id: UUID = Field(default_factory=uuid4) 

class LoginRequest(BaseModel):
   email: str
   password:str


class Token(BaseModel):
   access_token: str
   token_type: str

def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()

db_dependency = Annotated[Session, Depends(get_db)]  

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserRequest, db: db_dependency):
   create_user_model = User(
      name=request.name,
      email=request.email,
      hashed_password=bcrypt_context.hash(request.password)
   )
   try:
      db.add(create_user_model)
      db.commit()
   except:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail='Email is already used') 


@router.post("/login", response_model=Token)
async def login_for_access_token(login_request:LoginRequest, db: db_dependency):

   user = authenticate_user(login_request.email, login_request.password, db)
   if not user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail='Could not validate user.')
   token = create_access_token(user.name,user.email,user.id, timedelta(minutes=20))
   return {'access_token': token, 'token_type':'bearer'}


def authenticate_user( email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
       return False
    if not bcrypt_context.verify(password, user.hashed_password):
       return False
    return user

def create_access_token(name: str, email: str, user_id:int, expires_delta:timedelta):
    encode = {'sub':name,'git':email, 'id': user_id}
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
       
      