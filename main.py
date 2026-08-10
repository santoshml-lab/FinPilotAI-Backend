import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq


MODEL = "openai/gpt-oss-20b"


app = FastAPI(
    title="FinPilot AI + SupportFlow AI Backend",
    description="AI-powered finance and customer support API",
    version="1.1.0",
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


# =========================
# FINPILOT
# =========================

class AIRequest(BaseModel):
    income: float
    expenses: float
    savings: float
    top_category: str = "Unknown"


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
        model=MODEL,
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


# =========================
# SUPPORTFLOW AI
# =========================

class SupportRequest(BaseModel):
    message: str


@app.post("/support/analyze")
def analyze_support_ticket(request: SupportRequest):

    prompt = f"""
You are SupportFlow AI, an AI customer-support assistant.

Analyze this customer support message:

"{request.message}"

Return ONLY valid JSON with exactly these fields:

{{
    "category": "Billing | Technical | Account | Refund | General",
    "priority": "Low | Medium | High | Critical",
    "sentiment": "Positive | Neutral | Negative",
    "summary": "short summary of the issue",
    "suggested_reply": "professional reply for the support agent"
}}

Rules:
- Category must be one of the listed categories.
- Priority must be one of the listed priorities.
- Sentiment must be one of the listed sentiments.
- Keep the summary short.
- Suggested reply should be polite, professional and useful.
- Do not invent company policies, refunds or guarantees.
"""

    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
        max_tokens=300,
    )

    ai_result = response.choices[0].message.content

    return {
        "success": True,
        "analysis": ai_result,
    }


# =========================
# HEALTH / ROOT
# =========================

@app.get("/")
def root():
    return {
        "message": "FinPilot AI + SupportFlow AI Backend is running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
