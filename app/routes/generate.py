from fastapi import APIRouter
from app.schemas.generate import GenerateRequest,GenerateResponse
from app.services.generate_service import generate_explanation

from app.services.retrieval_service import retrieve_similar_records
from app.services.rag_service import generate_with_rag
from app.services.generate_service import generate_explanation

SIMILARITY_THRESHOLD = 0.7

router = APIRouter()
@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    results = retrieve_similar_records(request.topic)

    if results and results[0][0] >= SIMILARITY_THRESHOLD:
        print("USING RAG")
        explanation = generate_with_rag(request.topic, request.level)
    else:
        print("USING Path")
        explanation = generate_explanation(request.topic, request.level)

    return GenerateResponse(explanation=explanation)
