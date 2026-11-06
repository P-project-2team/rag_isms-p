# 보험 도메인 데이터셋 (세이프라이프손해보험, 가상)

담당: 이유진 · 기준: 설계서 v2 §6.1~§6.5

- 이 폴더에 `manifest.json`, `users.json`, `pii_registry.json`과 `docs/`, `records/`, `logs/`를 만든다.
- 형식은 `datasets/schemas/`의 스키마를 따른다. 올리기 전에 검증:
  `python scripts/validate_dataset.py datasets/insurance`
- 예시는 `tests/fixtures/insurance_mini/` (초소형 픽스처).
- 오염 문서(`poisoned/`)는 아직 만들지 않는다 — 설계서 v2.1 D-01 결정 후.
- 실제 개인정보 금지. 주민번호는 체크섬이 일부러 맞지 않게, 이메일은 `@example.com`, 전화는 `010-0xxx-xxxx`.

## 현재 내용: 소량 샘플 (insurance-0.1.0)

챗봇 개발 착수용. 전체 데이터셋(§6.3, 고객 50명 등)은 이 위에 이어서 만든다.

| 파일 | 내용 |
| --- | --- |
| `docs/public/terms_medical.md` | 실손의료보험 약관 1종 (제1관~제7관 + 별표) |
| `records/customers.json` | 고객 5명 (C0001~C0005). C0003·C0005는 동명이인 "박모의" (권한 우회 시나리오용) |
| `records/contracts.json` | 계약 7건 (실손·자동차·암진단, 실효 1건 포함) |
| `records/claims.jsonl` | 청구 7건 (지급완료 3·심사중 1·부지급 2·보류 1) |
| `users.json` | guest 1, customer 5 (cust_a~cust_e ↔ C0001~C0005), agent 1, admin 1 |
| `pii_registry.json` | 위 레코드의 PII 값 전부 (이름 포함) |

- 고객 A(`cust_a`, C0001 김가상): 계약 2건(실손·자동차), 청구 2건 → `/chat` 첫 테스트용
- 설계서와 다른 점: PII 필드는 레지스트리 대조가 쉽도록 평평하게 둔다 — 계좌는 `bank_name` + `bank_account`(번호), 수익자는 `beneficiary_name` + `beneficiary_relation`
- 아직 없음: 청구 마스킹본(`claims_masked.jsonl`), 상담 로그, FAQ, 안내서·처리방침, 내부 문서, 오염 문서(D-01)
