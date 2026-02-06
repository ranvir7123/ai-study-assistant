from pydantic import BaseModel

class GenerateRequest(BaseModel):
    topic:str
    level:str


class GenerateResponse(BaseModel):
    explanation:str

    