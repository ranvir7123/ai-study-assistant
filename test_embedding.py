from app.services.embedding_service import get_embedding

vec = get_embedding("Arrays are a data structure")
print(type(vec))
print(len(vec))
print(vec[:5])
