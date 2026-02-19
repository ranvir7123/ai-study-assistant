# test_misconception_memory.py

from app.services.diagnose_service import persist_misconceptions
from app.schemas.diagnose import AnswerAnalysis
from app.db.session import SessionLocal
from app.db.models import MisconceptionRecord
from app.db.models import Base
from app.db.session import engine
Base.metadata.create_all(bind=engine)



def print_all_records():
    db = SessionLocal()
    records = db.query(MisconceptionRecord).all()
    print("\n--- Current Misconception Records ---")
    for r in records:
        print(
            f"Topic: {r.topic}, "
            f"Concept: {r.concept}, "
            f"Frequency: {r.frequency_count}"
        )
    db.close()


def run_test():

    topic = "Recursion"

    # Simulate misconception analysis
    analyses = [
        AnswerAnalysis(
            question_id=1,
            user_answer="Recursion does not use stack frames.",
            correctness="incorrect",
            gap_type="misconception",
            reasoning_summary="User denies stack frame role.",
            missing_concepts=["stack frame"]
        )
    ]

    print("\n--- First Run ---")
    persist_misconceptions(topic, analyses)
    print_all_records()

    print("\n--- Second Run (Same Misconception) ---")
    persist_misconceptions(topic, analyses)
    print_all_records()


if __name__ == "__main__":
    run_test()
