from pydantic import BaseModel
from typing import List,Literal,Optional
class AnswerInput(BaseModel):
    question_id: int
    question: str
    answer: str

class DiagnoseRequest(BaseModel):
    topic: str
    answers: Optional[List[AnswerInput]] = None

class DiagnosticQuestion(BaseModel):
    id: int
    question: str
    gap_type: str

class DiagnoseResponse(BaseModel):
    questions: List[DiagnosticQuestion]



class AnswerAnalysis(BaseModel):
    question_id: int
    user_answer: str
    correctness: Literal["correct", "partial", "incorrect"]
    gap_type: Literal[
        "prerequisite",
        "mechanism",
        "application",
        "misconception",
        "none"
    ]
    reasoning_summary: str
    missing_concepts: List[str]
