"""이유진(데이터셋) ↔ 이서준(타깃 챗봇) 계약 테스트."""

import json
import re

import pytest
from pydantic import ValidationError

from common.contracts import ChatResponse, Mode, Source
from common.schemas import errors
from scripts.validate_dataset import validate


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_fixture_dataset_passes_all_schemas(fixture_dataset):
    assert validate(fixture_dataset) == []


def test_manifest_rejects_unknown_access_level(fixture_dataset):
    manifest = load(fixture_dataset / "manifest.json")
    manifest["files"][0]["access_level"] = "everyone"
    assert any("access_level" in e for e in errors("manifest", manifest))


def test_manifest_rejects_unknown_pii_type(fixture_dataset):
    manifest = load(fixture_dataset / "manifest.json")
    manifest["files"][1]["pii_fields"][0]["pii_type"] = "SSN"
    assert errors("manifest", manifest)


def test_customer_user_requires_customer_id(fixture_dataset):
    users = load(fixture_dataset / "users.json")
    users[1]["customer_id"] = None
    assert errors("users", users)


def _rrn_checksum_ok(rrn: str) -> bool:
    digits = [int(c) for c in rrn.replace("-", "")]
    weights = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]
    check = (11 - sum(d * w for d, w in zip(digits[:12], weights, strict=True)) % 11) % 10
    return check == digits[12]


def test_registry_rrns_are_synthetic(fixture_dataset):
    """설계서 v2 §6.1·§6.4 Q1: 합성 주민번호는 체크섬이 일부러 맞지 않아야 한다."""
    registry = load(fixture_dataset / "pii_registry.json")
    rrns = [e["value"] for e in registry["entries"] if e["pii_type"] == "RRN"]
    assert rrns
    for rrn in rrns:
        assert re.fullmatch(r"\d{6}-\d{7}", rrn)
        assert not _rrn_checksum_ok(rrn), f"실존 가능한 형식의 주민번호: {rrn}"


def test_registry_covers_manifest_pii_fields(fixture_dataset):
    """설계서 v2 §6.4 Q4: manifest의 PII 필드 값은 모두 레지스트리에 있어야 한다 (이름 제외)."""
    manifest = load(fixture_dataset / "manifest.json")
    registered = {e["value"] for e in load(fixture_dataset / "pii_registry.json")["entries"]}
    for f in manifest["files"]:
        if f["format"] != "json" or not f["pii_fields"]:
            continue
        for record in load(fixture_dataset / f["path"]):
            for pf in f["pii_fields"]:
                if pf["pii_type"] == "NAME":
                    continue  # 이름은 단독으로 유출 판정하지 않음 (§6.3.12)
                assert record[pf["field"]] in registered


def test_chat_response_contract():
    resp = ChatResponse(
        answer="안녕하세요",
        sources=[
            Source(
                chunk_id="c1",
                doc_id="d1",
                source_type="record",
                sensitivity="sensitive",
                access_level="customer_self",
                owner_customer_id="C0001",
                score=0.8,
            )
        ],
        log_id="log-1",
        mode=Mode.vulnerable,
        model="mock-llm",
        latency_ms=3,
    )
    dumped = resp.model_dump(mode="json")
    assert set(dumped) == {"answer", "sources", "log_id", "mode", "model", "latency_ms"}
    assert set(dumped["sources"][0]) == {
        "chunk_id",
        "doc_id",
        "source_type",
        "sensitivity",
        "access_level",
        "owner_customer_id",
        "score",
    }


def test_chat_response_rejects_bad_mode():
    with pytest.raises(ValidationError):
        ChatResponse(answer="x", sources=[], log_id="l", mode="unsafe", model="m", latency_ms=0)
