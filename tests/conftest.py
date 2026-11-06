from pathlib import Path

import pytest

FIXTURE_DATASET = Path(__file__).parent / "fixtures" / "insurance_mini"


@pytest.fixture(autouse=True)
def _always_mock_llm(monkeypatch):
    """테스트는 실제 LLM API를 절대 부르지 않는다."""
    monkeypatch.setenv("LLM_PROVIDER", "mock")


@pytest.fixture
def fixture_dataset() -> Path:
    return FIXTURE_DATASET
