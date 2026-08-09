import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq


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


groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class AIRequest(BaseModel):
    income: float
    expenses: float
    savings: float
    top_category: str = "Unknown"


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


@app.post("/ai")
def generate_ai_insight(request: AIRequest):

    prompt = f"""
You are FinPilot AI, a personal finance insights assistant.

Analyze the following financial summary:

Income: ₹{request.income}
Expenses: ₹{request.expenses}
Savings: ₹{request.savings}
Highest spending category: {request.top_category}

Give a short, practical financial insight.

Mention:
1. Current financial situation
2. Biggest spending concern
3. One practical suggestion

Do not make investment promises or guarantees.
Keep the response under 120 words.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.4,
        max_tokens=200,
    )

    return {
        "success": True,
        "insight": response.choices[0].message.content,
    }
