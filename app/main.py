from fastapi import FastAPI
from app.routes.generate import router as generate_router
from app.db.models import Base
from app.db.session import engine
from app.routes.diagnose import router as diagnose_router

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(generate_router)


app.include_router(diagnose_router)


@app.get("/health")
def health():
    return {"status": "ok"}
