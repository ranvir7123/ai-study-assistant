from sqlalchemy.orm import Session
from app.db.models import StudyRecord
import json

#session comes from outside with topic level etc gets saved 
def save_record(db:Session,topic:str,level:str,explanation:str,embedding):
    record = StudyRecord(topic=topic,level=level,explanation=explanation,embedding=json.dumps(embedding))
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_records(db:Session,limit:int=10):
    return db.query(StudyRecord).order_by(StudyRecord.created_at.desc()).limit(limit).all()