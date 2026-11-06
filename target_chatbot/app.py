"""타깃 챗봇 API (:8000) — 실행 뼈대.

지금은 /health와 계약 형태만 맞춘 /chat 자리표시만 있다.
RAG 로직(로그인, 인덱싱, 검색, 권한 필터, 마스킹, 로그)은 이서준이 설계서 v2 §7.1~§7.4, §7.6대로 채운다.
실행: uvicorn target_chatbot.app:app --port 8000
"""

from __future__ import annotations

import os
import time
import uuid

from fastapi import FastAPI, Header

from common.contracts import HEADER_CASE_ID, HEADER_RUN_ID, ChatRequest, ChatResponse, Health, Mode
from common.llm import get_llm

app = FastAPI(title="target-chatbot", version="0.1.0")


def current_mode() -> Mode:
    return Mode(os.getenv("CHATBOT_MODE", Mode.vulnerable.value))


@app.get("/health", response_model=Health)
def health() -> Health:
    return Health(service="target-chatbot", domain="insurance", model=get_llm().model, mode=current_mode())


@app.post("/chat", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    x_run_id: str | None = Header(default=None, alias=HEADER_RUN_ID),
    x_case_id: str | None = Header(default=None, alias=HEADER_CASE_ID),
) -> ChatResponse:
    # TODO(이서준): 세션 토큰 → 역할 확인 (설계서 v2 §7.4.1 /auth/login)
    # TODO(이서준): 검색(§7.3) → 프롬프트 조립(§7.1) → LLM → 출력 필터 → 로그(§7.6, x_run_id·x_case_id 기록)
    started = time.perf_counter()
    llm = get_llm()
    messages = [{"role": "user", "content": req.message}]
    result = llm.generate(system="(시스템 프롬프트 자리)", messages=messages)
    return ChatResponse(
        answer=result.text,
        sources=[],
        log_id=f"log-{uuid.uuid4().hex[:12]}",
        mode=current_mode(),
        model=result.model,
        latency_ms=int((time.perf_counter() - started) * 1000),
    )
