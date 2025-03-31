# Database models i.e UserQuery, ChatHistory, logs etc

import sys
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.db import Base
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class UserQuery(Base):
    __tablename__ = "user_query"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    response = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="queries")
    timestamp = Column(DateTime, default=datetime.utcnow) 

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    response = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="chats")
    timestamp = Column(DateTime, default=datetime.utcnow) 
    session_id = Column(String) 

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    queries = relationship("UserQuery", back_populates="user")
    chats = relationship("ChatHistory", back_populates="user")
    logs = relationship("Log", back_populates="user")
    role = Column(String, default = "user") 
    verified_email = Column(Boolean, default = False) 

class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, index=True)
    message = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="logs")
    timestamp = Column(DateTime, default=datetime.utcnow) 
class NamedEntity(Base):
    __tablename__ = "named_entities"
    id = Column(Integer, primary_key=True, index=True)
    entity = Column(String)
    entity_type = Column(String)
    query_id = Column(Integer, ForeignKey("user_query.id"))
    user_query = relationship("UserQuery")

class JwtToken(Base):
    __tablename__ = "jwt_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
    expires = Column(DateTime)