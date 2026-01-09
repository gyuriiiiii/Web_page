# simple_main.py - RAG 없이 일반 챗봇만 테스트

import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError, APIError, APIConnectionError, RateLimitError, APITimeoutError

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

client = OpenAI(api_key=api_key)

app = FastAPI(title="Yeobaek Chat Backend (Simple)")

# CORS 설정
# 환경 변수로부터 허용할 origin 읽기 (프로덕션 환경 대응)
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # 필요한 메서드만 허용
    allow_headers=["Content-Type", "Authorization"],  # 필요한 헤더만 허용
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
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="메시지가 비어 있습니다.")

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
            timeout=30.0,  # 타임아웃 30초 설정
        )
        return ChatResponse(reply=completion.choices[0].message.content)

    except RateLimitError as e:
        logger.error(f"OpenAI Rate Limit 에러: {e}")
        raise HTTPException(
            status_code=429,
            detail="요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
        )
    except APITimeoutError as e:
        logger.error(f"OpenAI Timeout 에러: {e}")
        raise HTTPException(
            status_code=504,
            detail="요청 시간이 초과되었습니다. 다시 시도해주세요."
        )
    except APIConnectionError as e:
        logger.error(f"OpenAI 연결 에러: {e}")
        raise HTTPException(
            status_code=503,
            detail="AI 서비스에 연결할 수 없습니다. 잠시 후 다시 시도해주세요."
        )
    except APIError as e:
        logger.error(f"OpenAI API 에러: {e}")
        raise HTTPException(
            status_code=502,
            detail="AI 서비스에서 오류가 발생했습니다."
        )
    except Exception as e:
        logger.error(f"예상치 못한 에러 (/api/rag-chat): {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="답변 생성 중 예상치 못한 오류가 발생했습니다."
        )
