# rag_isms-p
RAG 챗봇 보안 취약점 진단 및 AI 기반 ISMS-P 개선 보고 시스템 개발

🚨바로 main에 푸시 금지
용도 별 브랜치 만들어서 올려둔 후 나중에 main에 푸시

팀원 A:
팀원 B:
팀원 C: 유진

## 기준 문서

- **기준은 제안서**다. 설계서(`design_spec_v2.1`)와 충돌하면 제안서를 따른다.
- 설계서 v2.1 §0.4에 ⏸ 유보·❓ 결정 필요로 표시된 절은 **아직 구현하지 않는다**. 목록은 노션 위키 "설계서·구현" 페이지.
- 할 일과 담당은 노션 "프로젝트 현황 → 착수 배분".

## 시작하기

Python 3.11 기준.

```bash
python -m venv .venv && source .venv/bin/activate
make install-dev          # 최소 의존성 (계약 테스트·실행 뼈대·mock LLM)
# make install            # 전체 의존성 (RAG·UI·LLM SDK)
cp .env.example .env      # LLM_PROVIDER=mock 그대로 두면 API 비용 0
make test                 # pytest (항상 mock LLM)
make dev                  # 챗봇 :8000 · 진단 엔진 :8100 · UI :8501
```

- API 문서: http://localhost:8000/docs (챗봇), http://localhost:8100/docs (진단 엔진)
- 실제 LLM은 실측 진단 때만 `LLM_PROVIDER=openai|anthropic`으로 바꾼다 (설계서 v2 §1.5).

## 구조

```
common/            공용 계약·LLM 스위치·설정 로더
  contracts.py     /chat 요청·응답 모델 (타깃 챗봇 ↔ 진단 엔진 계약)
  llm.py           get_llm(): LLM_PROVIDER에 따라 mock / 실제 API
  schemas.py       데이터셋 스키마 검증
target_chatbot/    타깃 RAG 챗봇 API :8000 (이서준)
diag_engine/       진단 엔진 API :8100
ui/                Streamlit :8501
configs/           diagnosis.yaml(반복 횟수·진단 항목, 유보 값은 TODO 표시), domains/insurance.yaml
datasets/
  schemas/         manifest·users·pii_registry JSON Schema (이유진 ↔ 이서준 계약)
  insurance/       보험 데이터셋 (이유진)
scripts/           validate_dataset.py, dev.sh
tests/             pytest, fixtures/insurance_mini (초소형 데이터셋)
```

## 규칙

- 역할: **은상** 프로젝트 전체 흐름 · **유진** 개발(브랜치·PR 관리, 리뷰·main 병합, 개발 일정) · **서준** 문서(제안서·발표·최종보고서)
- 브랜치: `feat/{이름}-{작업}` → PR → 1인 이상 리뷰 후 main 병합
- 계약 파일(`datasets/schemas/`, `common/contracts.py`)을 바꾸면 `schema_version`을 올리고 상대 담당자에게 리뷰 요청
- 유보 값은 코드에 박지 말고 `configs/`에 두고 `TODO(U-01)`처럼 설계서 v2.1 ID를 단다
- 커밋 금지: `.env`·API 키, 실제 개인정보, 공격 세트 원문(`attacks/*.jsonl`은 .gitignore). **이 레포는 현재 공개 상태다**
