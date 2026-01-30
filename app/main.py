from fastapi import FastAPI
from app.routes.generate import router as generate_router

app = FastAPI()

app.include_router(generate_router)

@app.get("/health")
def health():
    return {"status": "ok"}
