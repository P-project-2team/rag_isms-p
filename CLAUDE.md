# CLAUDE.md — AI 코딩 도구용 작업 지침

이 레포에서 코드를 쓰는 AI 도구(Claude 등)가 먼저 읽는 파일이다. 사람용 안내는 README.md.

## 프로젝트

LLM 기반 RAG 서비스 보안 자동진단 및 ISMS-P 매핑 시스템 (가천대 P-프로젝트 2조).
공식 보안 기준(ISMS-P·금융보안원·개인정보위)을 기계가 판정할 수 있는 기준으로 바꿔 RAG 챗봇을 자동 진단하고,
결과를 ISMS-P 항목에 매핑해 보고한다.

## 반드시 지킬 것

1. **기준은 제안서.** 설계서 v2.1(노션 자료함 `design_spec_v2.1`)과 충돌하면 제안서를 따른다.
2. 설계서 v2.1 §0.4에서 **⏸ 유보(U-xx)·❓ 결정 필요(D-xx)** 로 표시된 절은 구현하지 않는다.
   특히: 진단 단위 V01~V05(U-01), 확장 도메인(U-02), 위험도 3단계·Finding 집계(U-04), ISMS-P 매핑 규칙(U-05),
   F1 평가(U-06), 오염 문서(D-01), 고객 삭제 API(D-02), 빈도 제한 점검(D-03).
3. 유보 값(반복 횟수, 진단 항목 ID, 판정 출력 필드)은 코드에 박지 말고 `configs/`에 두고 `TODO(ID)` 주석을 단다.
4. 테스트와 CI는 항상 `LLM_PROVIDER=mock`. 실제 API 호출 코드를 테스트에서 부르지 않는다.
5. 계약 파일(`datasets/schemas/*.json`, `common/contracts.py`)을 바꾸면 schema_version을 올리고 `tests/test_contracts.py`를 함께 고친다.
6. 실제 개인정보, API 키, 공격 프롬프트 원문을 커밋하지 않는다. 레포는 현재 공개 상태다.
7. 공격·진단 실행은 우리가 만든 로컬 타깃에만 한다 (설계서 v2 §1.5, §7.1.4).

## 명령

- `make install-dev` / `make test` / `make lint` / `make dev`
- 데이터셋 검증: `python scripts/validate_dataset.py datasets/insurance`
