from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Comment(BaseModel):
    id: int
    post_id: int
    user_id: int
    comment: str
    posted_at: datetime

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    post_id: int
    comment: str

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    publish: bool = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostOut(BaseModel):
    Post: Post
    num_likes: int
    num_comments: Optional[int] = 0
    comments: Optional[List[str]] = "no comments"
    comment_emails: Optional[List[str]] = "no comments"

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Like(BaseModel):
    post_id: int
    dir: conint(le=1)
