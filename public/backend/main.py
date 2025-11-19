# backend/main.py

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv
from openai import OpenAI

import chromadb
from chromadb.utils import embedding_functions

# ================== 기본 설정 ==================

BASE_DIR = Path(__file__).resolve().parent
RAG_DIR = BASE_DIR / "rag"
DB_DIR = RAG_DIR / "db"

COLLECTION_NAME = "yeobaek_docs"
EMBED_MODEL = "text-embedding-3-small"

load_dotenv()  # .env 읽기
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다. .env를 확인해주세요.")

# OpenAI 클라이언트
client = OpenAI(api_key=api_key)


# ================== Chroma / RAG(1119 신규) ==================

def get_rag_collection():
    """저장된 인덱스를 불러와서 컬렉션 객체를 리턴"""
    if not DB_DIR.exists():
        raise RuntimeError(
            f"RAG DB 디렉터리가 없습니다: {DB_DIR} (rag/build_index.py를 먼저 실행하세요)"
        )

    chroma_client = chromadb.PersistentClient(path=str(DB_DIR))

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name=EMBED_MODEL,
    )

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=openai_ef,
    )
    return collection


def make_context_str(documents: List[str], metadatas: List[dict]) -> str:
    """
    검색된 청크들을 하나의 큰 context 문자열로 합치기.
    각 청크 앞에 [출처: 파일명, chunk: n] 꼬리표를 붙임.
    """
    blocks = []
    for doc, meta in zip(documents, metadatas):
        source = meta.get("source", "unknown")
        idx = meta.get("chunk_index", 0)
        header = f"[출처: {source} | chunk #{idx}]"
        blocks.append(header + "\n" + doc.strip())
    return "\n\n---\n\n".join(blocks)


# ================== 로그 설정 (옵션, 1119 신규) ==================

LOG_PATH = BASE_DIR / "logs" / "chat_logs.jsonl"
LOG_PATH.parent.mkdir(exist_ok=True)


def log_chat(user_message: str, reply: str, meta: Optional[dict] = None):
    """대화 한 건을 jsonl 형식으로 기록"""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_message": user_message,
        "reply": reply,
        "meta": meta or {},
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ================== FastAPI 앱 ==================

app = FastAPI(title="Yeobaek Chat Backend")

# CORS (프론트: http://localhost:5173 에서 접근, 1119 신규)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================== 모델 정의 ==================

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


# ================== 엔드포인트 ==================

# ping test
@app.get("/api/ping")
def ping():
    return {"status": "ok"}


# 1) 일반 LLM Chat (RAG X)
@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant for Yeobaek club. "
                        "Answer briefly in Korean unless the user asks otherwise."
                    ),
                },
                {"role": "user", "content": req.message},
            ],
        )
        reply_text = completion.choices[0].message.content
        log_chat(
            user_message=req.message,
            reply=reply_text,
            meta={"model": "gpt-4.1-mini", "source": "openai", "mode": "plain"},
        )
        return ChatResponse(reply=reply_text)
    except Exception as e:
        print("[ERROR] /api/chat:", e)
        raise HTTPException(status_code=500, detail="OpenAI 호출 중 오류가 발생했습니다.")


# 2) RAG + LLM Chat(1119 신규)
@app.post("/api/rag-chat", response_model=ChatResponse)
def rag_chat(req: ChatRequest):
    """
    1) 사용자의 질문으로 ChromaDB에서 관련 청크 검색
    2) 검색된 내용(context)을 붙여서 OpenAI에게 질문
    3) Yeobaek/LIS 도메인 답변을 생성해서 반환
    """
    query = req.message.strip()
    if not query:
        raise HTTPException(status_code=400, detail="message가 비어 있습니다.")

    try:
        collection = get_rag_collection()

        # 1) 벡터 검색 (Chroma가 내부적으로 임베딩 계산)
        results = collection.query(
            query_texts=[query],
            n_results=4,  # 상위 4개 청크 사용
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        if not docs:
            # 문서를 못 찾은 경우: 일반 답변으로 fallback
            fallback = (
                "아직 인덱스에서 관련 문서를 찾지 못했어요.\n"
                "그래도 일반 지식 기반으로 최대한 답변해볼게요 🙂"
            )
            context = ""
        else:
            context = make_context_str(docs, metas)
            fallback = None

        # 2) OpenAI에게 context + 질문 전달
        system_prompt = (
            "너는 인천대학교 문헌정보학과 동아리 '여백(Yeobaek)'의 "
            "전문 도서관·정보학(LIS) 어시스턴트야.\n"
            "- 주요 도메인: 문헌정보학, 정보검색(IR), 메타데이터/목록, 분류(KDC/DDC), "
            "디지털 아카이빙, 추천 시스템, 시소러스/온톨로지, 동아리 운영.\n"
            "- 아래 제공된 '여백 프로젝트 문서' 내용을 우선적으로 참고해서 답변해.\n"
            "- 문서에 없는 내용은 아는 척하지 말고, 확실히 모른다고 말해.\n"
            "- 답변은 한국어, 3~6문장 정도로 간결하게.\n"
            "- 필요하면 어떤 문서를 참고했는지도 자연스럽게 언급해."
        )

        user_content = query
        if context:
            user_content = (
                "다음은 여백 프로젝트 관련 문서 일부입니다:\n\n"
                f"{context}\n\n"
                "위 내용을 참고해서, 아래 질문에 답변해주세요.\n\n"
                f"질문: {query}"
            )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )

        reply_text = completion.choices[0].message.content

        # fallback 메시지가 있으면 앞에 살짝 붙이기
        if fallback:
            reply_text = fallback + "\n\n" + reply_text

        # 로그 기록
        log_chat(
            user_message=req.message,
            reply=reply_text,
            meta={
                "model": "gpt-4o-mini",
                "source": "openai",
                "mode": "rag",
                "docs_used": [m.get("source") for m in metas] if metas else [],
            },
        )

        return ChatResponse(reply=reply_text)

    except HTTPException:
        raise
    except Exception as e:
        print("[ERROR] /api/rag-chat:", e)
        raise HTTPException(
            status_code=500, detail="RAG 기반 답변 생성 중 오류가 발생했습니다."
        )


# 3) 최근 로그 조회 (옵션)
@app.get("/api/logs/recent")
def get_recent_logs(limit: int = 20):
    """최근 대화 로그 n개 조회 (기본 20개)"""
    if not LOG_PATH.exists():
        return []

    lines = LOG_PATH.read_text(encoding="utf-8").splitlines()
    data = [json.loads(line) for line in lines[-limit:]]
    return data