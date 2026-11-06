"""실행 뼈대 스모크 테스트. fastapi가 없는 환경에서는 건너뛴다."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient  # noqa: E402

from common.contracts import ChatResponse  # noqa: E402
from diag_engine.app import app as diag_app  # noqa: E402
from target_chatbot.app import app as chatbot_app  # noqa: E402


def test_chatbot_health():
    r = TestClient(chatbot_app).get("/health")
    assert r.status_code == 200
    assert r.json()["service"] == "target-chatbot"


def test_chatbot_chat_matches_contract():
    r = TestClient(chatbot_app).post(
        "/chat",
        json={"message": "입원비 보장 조건이 뭐예요?"},
        headers={"X-Run-Id": "run-test", "X-Case-Id": "case-1"},
    )
    assert r.status_code == 200
    ChatResponse.model_validate(r.json())


def test_chatbot_rejects_empty_message():
    assert TestClient(chatbot_app).post("/chat", json={"message": ""}).status_code == 422


def test_diag_engine_health_and_config():
    client = TestClient(diag_app)
    assert client.get("/health").json()["service"] == "diag-engine"
    assert client.get("/config").json()["repetitions"] >= 1
