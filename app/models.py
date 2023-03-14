from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    publish = Column(Boolean, server_default="TRUE")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User")
    likes = relationship("Likes")
    comments = relationship("Comments")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )


class Likes(Base):
    __tablename__ = "likes"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )


class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    comment = Column(String, nullable=False)
    posted_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )
