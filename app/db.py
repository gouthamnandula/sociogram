from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column, Text, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi import Depends

DATABASE_URL = "sqlite+aiosqlite:///.test.db"

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    #it is saying one User can have many posts
    posts = relationship("Post", back_populates="user")

#one to many relationship where User is parent and Post is child

class Post(Base):
    
    __tablename__= "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False) #it is main to connect the tables together
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    #these relationships automatically link these together and makes two way access, it is nothing but saying Each post → belongs to one user
    user = relationship("User", back_populates="posts")
    
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# this is for creating the tables in the database, we will call this function in main.py when the app starts, so that it creates the tables if they are not already created
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
# this is for getting the session to interact with the database, we will use this in our routes to interact with the database
async def get_async_session()-> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        #yield is like return but it will return the session and then after the function is done it will close the session, it is like a context manager for the session, it will automatically close the session after the function is done, so that we don't have to worry about closing the session manually
        yield session

#this is for getting the user database, we will use this in our users.py to interact with the user table in the database, it is a generator function that will yield the user database, so that we can use it in our routes to interact with the user table in the database
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
        