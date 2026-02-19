# test_adaptive_diagnosis.py

import app.db.models  # ensure models are registered

from app.db.session import engine, Base
Base.metadata.create_all(bind=engine)

from app.services.diagnose_service import generate_diagnostic_questions
from app.db.session import SessionLocal
from app.db.models import MisconceptionRecord


def print_memory_state():
    db = SessionLocal()
    records = db.query(MisconceptionRecord).all()
    print("\n--- Current Misconception Memory ---")
    for r in records:
        print(
            f"Topic: {r.topic}, "
            f"Concept: {r.concept}, "
            f"Frequency: {r.frequency_count}"
        )
    db.close()


def run_test():

    topic = "Recursion"

    print_memory_state()

    print("\n--- Generating Diagnostic Questions ---\n")

    questions = generate_diagnostic_questions(topic)

    for q in questions:
        print(f"[{q.gap_type.upper()}] {q.question}")


if __name__ == "__main__":
    run_test()
