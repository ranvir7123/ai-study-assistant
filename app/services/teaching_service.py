from typing import List, Set
from app.schemas.diagnose import AnswerAnalysis
from app.services.retrieval_service import retrieve_similar_records
from app.llm import call_llm


def teach_from_gaps(topic: str, analyses: List[AnswerAnalysis]) -> str:

    # ---- Aggregate Gaps ----
    missing_concepts: Set[str] = set()

    for analysis in analyses:
        if analysis.gap_type != "none":
            missing_concepts.update(analysis.missing_concepts)

    missing_concepts = list(missing_concepts)

    # If no real gaps detected
    if not missing_concepts:
        return "No conceptual gaps detected."

    # ---- Retrieval: Topic-Level (Filtered inside retrieval service) ----
    topic_results = retrieve_similar_records(topic)

    if not topic_results:
        return "No high-confidence canonical material found for this topic."

    # Use highest-confidence canonical explanation
    _, canonical_explanation = topic_results[0]

    context_block = canonical_explanation

    # Clean bullet formatting
    concept_block = "\n".join(f"- {concept}" for concept in missing_concepts)

    # ---- Controlled Teaching Prompt ----
    prompt = f"""
You are an AI tutor.

Teach ONLY the listed concepts.
Do NOT redefine the full topic.
Do NOT introduce new concepts.
Do NOT repeat prerequisites the student already understands.
Do NOT mention that these were missing concepts.
Do NOT restate the topic unless strictly necessary.
Use a neutral instructional tone.
Avoid enthusiasm, introductions, or commentary.

Concepts to Teach:
{concept_block}

Canonical Reference Material:
{context_block}

For each concept:
1. Provide a one-sentence definition.
2. Explain the mechanism in 2-3 concise sentences.
3. Provide ONE short technical example directly related to the topic.
   Do NOT use analogies or storytelling.
4. Ask ONE quick check question.

Keep explanations minimal and precise.
Do not add extra sections.
"""

    response = call_llm(prompt)

    return response
