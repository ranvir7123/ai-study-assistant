import requests

from app.db.session import SessionLocal
from app.services.db_service import save_record

from app.services.embedding_service import get_embedding


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def generate_explanation(topic: str, level: str) -> str:
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": f"Explain {topic} in a {level} way.",
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        data = response.json()
        embedding = get_embedding(data.get("response", "No response from model."))

        db = SessionLocal()
        try:
            save_record(db, topic, level, data.get("response", "No response from model."),embedding=embedding)
        finally:
            db.close()

        return data.get("response", "No response from model.")

    except Exception as e:
        print("LLM ERROR:", e)
        return "Error generating explanation."




def generate_response_with_context(context: str, question: str) -> str:
    """
    Generate a response using retrieved context (RAG).
    """
    try:
        prompt = f"""
You are a helpful assistant.

Context:
{context}

Question:
{question}
"""

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "No response from model.")

    except Exception as e:
        print("LLM CONTEXT ERROR:", e)
        return "Error generating grounded response."
