from pydantic import BaseModel
from typing import List

class DiagnoseRequest(BaseModel):
    topic: str

class DiagnosticQuestion(BaseModel):
    question: str
    gap_type: str

class DiagnoseResponse(BaseModel):
    questions: List[DiagnosticQuestion]
