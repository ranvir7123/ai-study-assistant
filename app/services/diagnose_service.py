import json
from app.services.retrieval_service import retrieve_similar_records
from app.schemas.diagnose import DiagnosticQuestion
from app.llm import call_llm


DIAGNOSTIC_PROMPT_TEMPLATE = """
You are an expert tutor whose job is to DIAGNOSE understanding, not teach.

You will be given:
- a topic
- canonical reference material (for grounding only)

Your task:
- Generate 5 to 8 diagnostic questions that probe understanding of the topic.

Rules:
- Do NOT explain any concept.
- Do NOT include answers or hints.
- Do NOT define terms.
- Each question must test reasoning or mental models.
- Each question must target EXACTLY ONE of the following gap types:
  - prerequisite
  - mechanism
  - application
  - misconception

Output format:
Return a JSON array where each item has:
- question (string)
- gap_type (one of the allowed types)

Do not include any text outside the JSON.

Topic:
{topic}

REFERENCE MATERIAL (DO NOT EXPLAIN TO USER):
{context}
"""


ALLOWED_GAP_TYPES = {
    "prerequisite",
    "mechanism",
    "application",
    "misconception",
}

FORBIDDEN_PHRASES = [
    "because",
    "means",
    "is when",
    "defined as",
    "for example",
]


def generate_diagnostic_questions(topic: str):
    # 1. Retrieve canonical context (grounding)
    records = retrieve_similar_records(topic)

    context = "\n".join([r[1] for r in records])


    # 2. Build diagnostic prompt
    prompt = DIAGNOSTIC_PROMPT_TEMPLATE.format(
        topic=topic,
        context=context
    )

    # 3. Call LLM (raw text only)
    raw_output = call_llm(prompt)
    print("RAW LLM OUTPUT >>>", repr(raw_output))

    
    start = raw_output.find("[")
    end = raw_output.rfind("]") + 1

    if start == -1 or end == -1:
        raise ValueError("LLM did not return a JSON array")

    json_text = raw_output[start:end]
    parsed = json.loads(json_text)

    
        

    # 5. Enforce schema
    questions = [DiagnosticQuestion(**item) for item in parsed]

    # 6. Validate question count
    if not (5 <= len(questions) <= 8):
        raise ValueError(
            f"Expected 5–8 diagnostic questions, got {len(questions)}"
        )

    # 7. Validate gap types + teaching leakage
    for q in questions:
        if q.gap_type not in ALLOWED_GAP_TYPES:
            raise ValueError(f"Invalid gap type: {q.gap_type}")

        lowered = q.question.lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase in lowered:
                raise ValueError(
                    f"Teaching leakage detected in question: {q.question}"
                )

    # 8. Return clean diagnostic probes
    return questions
