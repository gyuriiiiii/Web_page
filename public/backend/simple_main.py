# simple_main.py - RAG 없이 일반 챗봇만 테스트

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

client = OpenAI(api_key=api_key)

app = FastAPI(title="Yeobaek Chat Backend (Simple)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/api/ping")
def ping():
    return {"status": "ok"}

@app.post("/api/rag-chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 인천대학교 문헌정보학과 동아리 '여백(Yeobaek)'의 "
                        "전문 도서관·정보학(LIS) 어시스턴트야. "
                        "답변은 한국어로 3~6문장 정도로 간결하게 해줘."
                    ),
                },
                {"role": "user", "content": req.message},
            ],
        )
        return ChatResponse(reply=completion.choices[0].message.content)
    except Exception as e:
        print("[ERROR] /api/rag-chat:", e)
        raise HTTPException(status_code=500, detail=str(e))
