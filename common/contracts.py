"""타깃 챗봇 API 계약 (설계서 v2 §7.4.1).

이서준(타깃 챗봇)과 진단 엔진(어댑터)이 이 모델을 같이 쓴다.
필드를 바꾸면 SCHEMA_VERSION을 올리고 tests/test_contracts.py를 함께 고친다.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

SCHEMA_VERSION = "1.0.0"

# 진단 실행 컨텍스트를 실어 보내는 요청 헤더. 타깃 챗봇은 이 값을 로그에 남긴다.
HEADER_RUN_ID = "X-Run-Id"
HEADER_CASE_ID = "X-Case-Id"


class Role(StrEnum):
    guest = "guest"
    customer = "customer"
    agent = "agent"
    admin = "admin"


class Mode(StrEnum):
    vulnerable = "vulnerable"  # 취약 모드: 보안 통제 off
    defended = "defended"  # 방어 모드: 보안 통제 on (가드레일 등은 설정 플래그로 on/off)


class Sensitivity(StrEnum):
    public = "public"
    internal = "internal"
    confidential = "confidential"
    sensitive = "sensitive"


class AccessLevel(StrEnum):
    public = "public"
    customer_self = "customer_self"
    agent = "agent"
    admin = "admin"


class SourceType(StrEnum):
    document = "document"
    faq = "faq"
    record = "record"
    log = "log"
    poison = "poison"


class LoginRequest(BaseModel):
    user_id: str


class LoginResponse(BaseModel):
    token: str
    user_id: str
    role: Role
    customer_id: str | None = None
    agent_id: str | None = None


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


class Source(BaseModel):
    """응답에 쓰인 검색 청크의 메타데이터. 권한 우회(2.6.3) 판정의 핵심 증거다."""

    chunk_id: str
    doc_id: str
    source_type: SourceType
    sensitivity: Sensitivity
    access_level: AccessLevel
    owner_customer_id: str | None = None
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    log_id: str
    mode: Mode
    model: str
    latency_ms: int = Field(ge=0)


class Health(BaseModel):
    status: str = "ok"
    service: str
    schema_version: str = SCHEMA_VERSION
    domain: str | None = None
    model: str | None = None
    mode: Mode | None = None
