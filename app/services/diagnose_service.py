import json
from app.services.retrieval_service import retrieve_similar_records
from app.schemas.diagnose import DiagnosticQuestion
from app.llm import call_llm
from typing import List
from app.schemas.diagnose import AnswerAnalysis
from app.db.session import SessionLocal
from app.db.models import MisconceptionRecord


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
def get_top_misconceptions(topic: str, limit: int = 1):
    db = SessionLocal()
    try:
        records = (
            db.query(MisconceptionRecord)
            .filter(MisconceptionRecord.topic == topic)
            .order_by(MisconceptionRecord.frequency_count.desc())
            .limit(limit)
            .all()
        )
        return records
    finally:
        db.close()

def generate_diagnostic_questions(topic: str):

    # ---- Retrieve canonical reference ----
    records = retrieve_similar_records(topic)
    context = "\n".join([r[1] for r in records])

    # ---- Retrieve memory bias ----
    top_misconceptions = get_top_misconceptions(topic)

    memory_hint = ""
    if top_misconceptions:
        concepts = [m.concept for m in top_misconceptions]
        concept_block = "\n".join(f"- {c}" for c in concepts)

        memory_hint = f"""
Historical frequent misconceptions for this topic:
{concept_block}

Ensure at least ONE diagnostic question explicitly tests understanding of these concepts.
"""

    # ---- Build prompt with memory injection ----
    prompt = DIAGNOSTIC_PROMPT_TEMPLATE.format(
        topic=topic,
        context=context
    ) + memory_hint

    raw_output = call_llm(prompt)
    print("RAW LLM OUTPUT >>>", repr(raw_output))

    start = raw_output.find("[")
    end = raw_output.rfind("]") + 1

    if start == -1 or end == -1:
        raise ValueError("LLM did not return a JSON array")

    json_text = raw_output[start:end]
    parsed = json.loads(json_text)

    questions = []

    for idx, item in enumerate(parsed, start=1):
        question_obj = DiagnosticQuestion(
            id=idx,
            question=item["question"],
            gap_type=item["gap_type"]
        )
        questions.append(question_obj)

    if not (5 <= len(questions) <= 8):
        raise ValueError(
            f"Expected 5–8 diagnostic questions, got {len(questions)}"
        )

    for q in questions:
        if q.gap_type not in ALLOWED_GAP_TYPES:
            raise ValueError(f"Invalid gap type: {q.gap_type}")

    return questions

def build_evaluation_prompt(
    canonical_explanation: str,
    question: str,
    user_answer: str,
    question_id: int) -> str:
    prompt = f"""
You are performing structured answer evaluation.

Canonical Explanation:
{canonical_explanation}

Question:
{question}

Student Answer:
{user_answer}

Step 1:
Extract a list of CORE CONCEPTS from the Canonical Explanation.
Core concepts must be short technical phrases (2–5 words max).

Step 2:
Extract the concepts explicitly present in the Student Answer.

Step 3:
Compare both lists and determine:
- Missing concepts (from canonical list only)
- Incorrect concepts (if student contradicts canonical explanation)

Step 4:
Classify the PRIMARY gap type based strictly on comparison:
- "prerequisite"
- "mechanism"
- "application"
- "misconception"
- "none"

Rules:
- Missing concepts MUST come only from canonical concepts.
- Do NOT invent abstract terms like "purpose" or "scope".
- Be specific (e.g., "base case", "termination condition", "stack frame").
- Select only ONE primary gap type.
- If student contradicts canonical explanation → gap_type = "misconception".

Respond ONLY in valid JSON using this schema:

{{
  "question_id": {question_id},
  "user_answer": "{user_answer}",
  "correctness": "correct" | "partial" | "incorrect",
  "gap_type": "prerequisite" | "mechanism" | "application" | "misconception" | "none",
  "reasoning_summary": "brief explanation based strictly on concept comparison",
  "missing_concepts": ["concept_from_canonical_list"]
}}

NO text outside JSON.
Start directly with {{ """
    return prompt

def analyze_answers(topic: str, diagnostic_questions: List[dict], user_answers: List[dict]) -> List[AnswerAnalysis]:
    
    analyses = []
    context_records = retrieve_similar_records(topic)
    
    SIMILARITY_THRESHOLD = 0.75

    if context_records and context_records[0][0] >= SIMILARITY_THRESHOLD:
        canonical_explanation = context_records[0][1]
    else:
        eval_prompt=f"""
Explain the topic '{topic}' in depth.

Include:
- Clear definition
- Core mechanisms
- Key components
- Important constraints
- Common misconceptions
- Concrete examples

Be precise and concept-focused.
"""
        print("calling llm for new generation for explanation")
        canonical_explanation = call_llm(eval_prompt)
    
    
    for question in diagnostic_questions:
        q_id = question["id"]
        q_text = question["question"]
        matching_answer = next((a["answer"] for a in user_answers if a["question_id"] == q_id),"")

        # 3. Build evaluation prompt
        prompt = build_evaluation_prompt(
            canonical_explanation,
            q_text,
            matching_answer,
            q_id
        )

        # 4. Call LLM
        response_text = call_llm(prompt)

        # 5. Validate structured output
        analysis = AnswerAnalysis.model_validate_json(response_text)

        analyses.append(analysis)

    return analyses



from app.db.session import SessionLocal
from app.db.models import MisconceptionRecord
from sqlalchemy.orm import Session



def persist_misconceptions(topic: str, analyses: list):
    db: Session = SessionLocal()

    try:
        for analysis in analyses:
            if analysis.gap_type == "misconception":
                for concept in analysis.missing_concepts:

                    existing = (
                        db.query(MisconceptionRecord)
                        .filter(
                            MisconceptionRecord.topic == topic,
                            MisconceptionRecord.concept == concept,
                        )
                        .first()
                    )

                    if existing:
                        existing.frequency_count += 1
                    else:
                        new_record = MisconceptionRecord(
                            topic=topic,
                            concept=concept,
                            gap_type="misconception",
                            frequency_count=1,
                        )
                        db.add(new_record)

        db.commit()

    finally:
        db.close()
 