"""LLM 호출 추상화와 mock 스위치 (설계서 v2 §1.5 원칙 3).

개발·단위 테스트·CI에서는 LLM_PROVIDER=mock(기본값)으로 실제 API를 부르지 않는다.
실측 진단에서만 openai / anthropic으로 바꾼다.

    from common.llm import get_llm
    llm = get_llm()  # 환경변수 LLM_PROVIDER를 따른다
    result = llm.generate(system="...", messages=[{"role": "user", "content": "..."}])
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class LLMResult:
    text: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0


class LLMClient(Protocol):
    model: str

    def generate(self, system: str, messages: list[dict[str, str]]) -> LLMResult: ...


@dataclass
class MockLLM:
    """결정적인 가짜 LLM.

    - canned: 마지막 사용자 메시지에 특정 문자열이 들어 있으면 지정한 답을 돌려준다 (테스트용).
    - 그 밖에는 입력 해시로 만든 고정 답을 돌려준다. 같은 입력이면 항상 같은 출력이다.
    """

    model: str = "mock-llm"
    canned: dict[str, str] = field(default_factory=dict)

    def generate(self, system: str, messages: list[dict[str, str]]) -> LLMResult:
        last_user = next((m["content"] for m in reversed(messages) if m.get("role") == "user"), "")
        for trigger, answer in self.canned.items():
            if trigger in last_user:
                return self._result(system, messages, answer)
        digest = hashlib.sha256((system + "\n" + last_user).encode("utf-8")).hexdigest()[:8]
        return self._result(system, messages, f"[mock 응답 {digest}] {last_user[:50]}")

    def _result(self, system: str, messages: list[dict[str, str]], text: str) -> LLMResult:
        prompt_len = len(system) + sum(len(m.get("content", "")) for m in messages)
        return LLMResult(
            text=text, model=self.model, prompt_tokens=prompt_len // 2, completion_tokens=len(text) // 2
        )


SUPPORTED_PROVIDERS = ("mock", "openai", "anthropic")


def get_llm(provider: str | None = None) -> LLMClient:
    """환경변수 LLM_PROVIDER(기본 mock)에 맞는 클라이언트를 돌려준다."""
    provider = (provider or os.getenv("LLM_PROVIDER", "mock")).strip().lower()
    if provider == "mock":
        return MockLLM()
    if provider in ("openai", "anthropic"):
        # TODO(이서준): openai — 챗봇 LLM (gpt-4o-mini, 설계서 v2 §3.3)
        # TODO(진단 담당): anthropic — 판정·보고서 LLM (Claude Haiku 5.5, 설계서 v2 §3.3)
        raise NotImplementedError(f"LLM_PROVIDER={provider}는 아직 구현 전입니다. 개발 중에는 mock을 쓰세요.")
    raise ValueError(f"알 수 없는 LLM_PROVIDER: {provider} (가능: {', '.join(SUPPORTED_PROVIDERS)})")
