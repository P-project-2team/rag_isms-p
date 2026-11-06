"""데이터셋 계약 스키마 검증 (datasets/schemas/*.schema.json)."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "datasets" / "schemas"
SCHEMA_FILES = {
    "manifest": "manifest.schema.json",
    "users": "users.schema.json",
    "pii_registry": "pii_registry.schema.json",
}


def _registry() -> Registry:
    resources = []
    for filename in SCHEMA_FILES.values():
        schema = json.loads((SCHEMA_DIR / filename).read_text(encoding="utf-8"))
        resources.append((filename, Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def validator(kind: str) -> Draft202012Validator:
    schema = json.loads((SCHEMA_DIR / SCHEMA_FILES[kind]).read_text(encoding="utf-8"))
    return Draft202012Validator(
        schema, registry=_registry(), format_checker=Draft202012Validator.FORMAT_CHECKER
    )


def errors(kind: str, data: object) -> list[str]:
    """검증 오류를 사람이 읽을 수 있는 문장 목록으로 돌려준다. 비어 있으면 통과."""
    out = []
    for err in sorted(validator(kind).iter_errors(data), key=lambda e: list(e.absolute_path)):
        where = "/".join(str(p) for p in err.absolute_path) or "(최상위)"
        out.append(f"{where}: {err.message}")
    return out
