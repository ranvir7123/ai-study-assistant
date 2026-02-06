import requests

OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"

def get_embedding(text:str)->list[float]:
    payload={"model":EMBEDDING_MODEL,"prompt":text}
    response = requests.post(OLLAMA_EMBEDDING_URL,json=payload)
    response.raise_for_status()
    data= response.json()
    return data["embedding"]