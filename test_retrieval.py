import json

from app.db.session import SessionLocal
from app.services.embedding_service import get_embedding
from app.services.db_service import get_records
from app.utils.similarity import cosine_similarity

query = "Explain arrays in simple terms"

# 🔹 MISSING STEP (this is the fix)
query_embedding = get_embedding(query)

db = SessionLocal()
records = get_records(db, limit=10)
db.close()

results = []
print(get_records)
print(type(records))

for record in records:

    record_embedding = json.loads(record.embedding)
    score = cosine_similarity(query_embedding, record_embedding)
    results.append((score, record))

results.sort(key=lambda x: x[0], reverse=True)

for score, record in results[:3]:
    
    print("Score:", round(score, 3))
    print("Topic:", record.topic)
    print("Explanation:", record.explanation[:200])
    print("-" * 40)
