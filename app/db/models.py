from sqlalchemy import Column, Integer, String, DateTime,Text
from sqlalchemy.orm import declarative_base
from datetime import datetime
Base = declarative_base()
class StudyRecord(Base):
    __tablename__ = "study_records"

    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    level = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    embedding = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MisconceptionRecord(Base):
    __tablename__ = "misconception_records"

    id = Column(Integer, primary_key=True, index=True)

    topic = Column(String, index=True, nullable=False)
    concept = Column(String, index=True, nullable=False)
    gap_type = Column(String, nullable=False)

    frequency_count = Column(Integer, default=1)
