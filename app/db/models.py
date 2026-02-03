from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
Base = declarative_base()
class StudyRecord(Base):
    __tablename__ = "study_records"

    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    level = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
