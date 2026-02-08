from app.services.retrieval_service import retrieve_similar_records
from app.services.generate_service import generate_response_with_context

def generate_with_rag(topic: str, level: str) -> str:
    retrieved_texts = retrieve_similar_records(topic)

    context = "\n".join(f"- {text}" for text in retrieved_texts)

    question = f"Explain {topic} in a {level} way."

    return generate_response_with_context(context=context, question=question)
