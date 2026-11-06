"""데이터셋 계약 검증.

    python scripts/validate_dataset.py datasets/insurance
    python scripts/validate_dataset.py tests/fixtures/insurance_mini

manifest.json, users.json, pii_registry.json을 스키마로 검사하고,
manifest에 적힌 파일이 실제로 있는지 확인한다. 실패하면 종료 코드 1.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common.schemas import errors  # noqa: E402

TARGETS = {"manifest": "manifest.json", "users": "users.json", "pii_registry": "pii_registry.json"}


def validate(root: Path) -> list[str]:
    problems: list[str] = []
    loaded: dict[str, object] = {}
    for kind, filename in TARGETS.items():
        path = root / filename
        if not path.exists():
            problems.append(f"{filename}: 파일 없음")
            continue
        try:
            loaded[kind] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"{filename}: JSON 문법 오류 ({exc})")
            continue
        problems += [f"{filename} {msg}" for msg in errors(kind, loaded[kind])]

    manifest = loaded.get("manifest")
    if isinstance(manifest, dict):
        for item in manifest.get("files", []):
            if isinstance(item, dict) and "path" in item and not (root / item["path"]).exists():
                problems.append(f"manifest.json: files의 경로가 없음 → {item['path']}")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    root = Path(argv[1])
    problems = validate(root)
    if problems:
        print(f"[실패] {root}")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"[통과] {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
