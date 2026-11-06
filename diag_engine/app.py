"""진단 엔진 API (:8100) — 실행 뼈대.

진단 단위·반복 횟수·판정 출력은 설계서 v2.1에서 유보·결정 필요 상태다 (U-01, U-04, D-04).
값은 configs/diagnosis.yaml에서 읽고 코드에 박지 않는다.
실행: uvicorn diag_engine.app:app --port 8100
"""

from __future__ import annotations

from fastapi import FastAPI

from common.contracts import Health
from common.settings import load_diagnosis_config

app = FastAPI(title="diag-engine", version="0.1.0")


@app.get("/health", response_model=Health)
def health() -> Health:
    return Health(service="diag-engine")


@app.get("/config")
def config() -> dict:
    """현재 진단 설정 (유보 항목은 TODO 표시가 붙은 값)."""
    return load_diagnosis_config()
