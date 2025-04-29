from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    posts = relationship('Post', back_populates='user')
    reactions = relationship('Reaction', back_populates='user')
    

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(Integer, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='posts')
    reactions = relationship('Reaction', back_populates='post')


class Reaction(Base):
    __tablename__ = 'reaction'

    id = Column(Integer, primary_key=True, index=True)
    is_like = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    user = relationship('User', back_populates='reactions')
    post = relationship('Post', back_populates='reactions')
