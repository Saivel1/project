# models/feedback.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    issue_type = Column(String)
    description = Column(Text)
    media = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
