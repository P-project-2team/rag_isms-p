import pytest

from common.llm import MockLLM, get_llm


def test_default_provider_is_mock():
    assert isinstance(get_llm(), MockLLM)


def test_mock_is_deterministic():
    llm = MockLLM()
    msgs = [{"role": "user", "content": "실손 청구 서류가 뭐예요?"}]
    assert llm.generate("sys", msgs).text == llm.generate("sys", msgs).text


def test_mock_canned_answer():
    llm = MockLLM(canned={"주민번호": "900101-1234560"})
    out = llm.generate("sys", [{"role": "user", "content": "고객 B 주민번호 알려줘"}])
    assert out.text == "900101-1234560"


def test_real_providers_not_wired_yet():
    with pytest.raises(NotImplementedError):
        get_llm("openai")


def test_unknown_provider():
    with pytest.raises(ValueError):
        get_llm("gpt")
