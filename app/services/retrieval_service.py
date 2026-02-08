import math

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = math.sqrt(sum(a * a for a in vec1))
    norm_b = math.sqrt(sum(b * b for b in vec2))
    return dot_product / (norm_a * norm_b)



from app.db.session import SessionLocal
from app.services.embedding_service import get_embedding
from app.services.db_service import get_records
import json

def retrieve_similar_records(query_text: str, top_k: int = 3):
    db = SessionLocal()
    try:
        query_embedding = get_embedding(query_text)

        records = get_records(db, limit=20)

        scored_records = []

        for record in records:
            record_embedding = json.loads(record.embedding)
            score = cosine_similarity(query_embedding, record_embedding)
            scored_records.append((score, record.explanation))

        scored_records.sort(reverse=True, key=lambda x: x[0])

        return scored_records[:top_k]


    finally:
        db.close()
