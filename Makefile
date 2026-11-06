.PHONY: install install-dev dev test lint format validate-fixture

install-dev:        ## 개발·CI 최소 의존성
	pip install -r requirements-dev.txt

install:            ## 전체 의존성 (RAG·UI·LLM)
	pip install -r requirements.txt

dev:                ## 챗봇 :8000, 진단 :8100, UI :8501 한 번에 실행 (LLM_PROVIDER 기본 mock)
	bash scripts/dev.sh

test:               ## pytest (항상 mock LLM)
	LLM_PROVIDER=mock pytest

lint:
	ruff check .

format:
	ruff format . && ruff check --fix .

validate-fixture:   ## 테스트용 초소형 데이터셋 계약 검증
	python scripts/validate_dataset.py tests/fixtures/insurance_mini
