from fastapi import APIRouter
from app.schemas.generate import GenerateRequest,GenerateResponse
from app.services.generate_service import generate_explanation
router = APIRouter()
@router.post('/generate',response_model=GenerateResponse)
def generate(request:GenerateRequest):
    explanation = generate_explanation(topic=request.topic,level=request.level)
    return GenerateResponse(explanation=explanation)