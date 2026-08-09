from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FinPilot AI Backend",
    description="AI-powered financial insights API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "FinPilot AI Backend is running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
