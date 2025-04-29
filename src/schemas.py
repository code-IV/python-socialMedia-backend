from typing import List
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class PostBase(BaseModel):
    title: str
    content: str


class ReactionBase(BaseModel):
    is_like: bool
    post_id: int


class UserWrite(UserBase):
    password: str


class PostWrite(PostBase):
    user_id: int


class ReactionWrite(ReactionBase):
    user_id: int


class ReactionRead(ReactionBase):
    user_id: int
    
    class Config():
        from_attributes = True


class PostRead(PostBase):
    # created_at: int
    reactions: List[ReactionRead] = []

    class Config():
        from_attributes = True


class UserRead(UserBase):
    id: int
    posts: List[PostRead] = []
    reactions: List[ReactionRead] = []
    
    class Config():
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None