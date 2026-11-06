# 보험 도메인 데이터셋 (세이프라이프손해보험, 가상)

담당: 이유진 · 기준: 설계서 v2 §6.1~§6.5

- 이 폴더에 `manifest.json`, `users.json`, `pii_registry.json`과 `docs/`, `records/`, `logs/`를 만든다.
- 형식은 `datasets/schemas/`의 스키마를 따른다. 올리기 전에 검증:
  `python scripts/validate_dataset.py datasets/insurance`
- 예시는 `tests/fixtures/insurance_mini/` (초소형 픽스처).
- 오염 문서(`poisoned/`)는 아직 만들지 않는다 — 설계서 v2.1 D-01 결정 후.
- 실제 개인정보 금지. 주민번호는 체크섬이 일부러 맞지 않게, 이메일은 `@example.com`, 전화는 `010-0xxx-xxxx`.
