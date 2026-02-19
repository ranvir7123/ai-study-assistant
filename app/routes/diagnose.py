from fastapi import APIRouter
from app.schemas.diagnose import DiagnoseRequest
from app.services.diagnose_service import analyze_answers
from app.services.diagnose_service import generate_diagnostic_questions

router = APIRouter()

@router.post("/diagnose")
def diagnose(request: DiagnoseRequest):

    # MODE 1 → Generate questions
    if request.answers is None:
        questions = generate_diagnostic_questions(request.topic)
        return {"questions": questions}

    # MODE 2 → Analyze answers
    else:
        diagnostic_questions = [
            {"id": a.question_id, "question": a.question}
            for a in request.answers
        ]

        user_answers = [
            {"question_id": a.question_id, "answer": a.answer}
            for a in request.answers
        ]

        results = analyze_answers(
            topic=request.topic,
            diagnostic_questions=diagnostic_questions,
            user_answers=user_answers
        )

        return {"analysis": results}
