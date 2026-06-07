from pydantic import BaseModel,EmailStr
from typing import List,Any
from datetime import date
#pip install 'pydantic[email]'
class User(BaseModel):
    name: str
    email: str
    id: int
    status: int
    added_date: date 
    
class UserResponse(BaseModel):
    message: str
    data: List[User]
    status: int
# 🔹 Request Model (input)
class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str


# 🔹 Response Model (output user)
class PostUser(BaseModel):
    status: int
    message: str


# 🔹 Response Wrapper (POST)
class UserCreateResponse(BaseModel):
    message: str
    data: PostUser  

# 🔹 Request Model (input)
class LoginUser(BaseModel):
    email: EmailStr
    password: str
class UserLogout(BaseModel):
    message: str
    data: None
    status: int