from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, conint
from typing import Optional


# Pydantic schenas for posting data to DB
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# Pydantic schema for data responses from DB
# Extend the Post base and add int and created_at
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True
        # orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True
        # orm_mode = True


# User Schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


# Vote schema
class Vote(BaseModel):
    post_id: int
    vote_dir: int = Field(..., ge=0, le=1)
    # vote_dir: conint(ge=0, le=1)
