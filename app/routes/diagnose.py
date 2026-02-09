from fastapi import APIRouter
from app.schemas.diagnose import DiagnoseRequest, DiagnoseResponse
from app.services.diagnose_service import generate_diagnostic_questions

router = APIRouter()

@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose(request: DiagnoseRequest):
    questions = generate_diagnostic_questions(request.topic)
    return {"questions": questions}
