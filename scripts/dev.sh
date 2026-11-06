#!/usr/bin/env bash
# 로컬 개발 서버 3개를 한 번에 띄운다. Ctrl+C로 모두 종료.
#   타깃 챗봇 :8000 / 진단 엔진 :8100 / Streamlit :8501
set -euo pipefail
cd "$(dirname "$0")/.."

if [ -f .env ]; then
  set -a; source .env; set +a
fi
export LLM_PROVIDER="${LLM_PROVIDER:-mock}"

pids=()
cleanup() { kill "${pids[@]}" 2>/dev/null || true; }
trap cleanup EXIT INT TERM

uvicorn target_chatbot.app:app --port 8000 --reload & pids+=($!)
uvicorn diag_engine.app:app --port 8100 --reload & pids+=($!)
if command -v streamlit >/dev/null 2>&1; then
  streamlit run ui/Home.py --server.port 8501 & pids+=($!)
else
  echo "streamlit 없음: UI는 건너뜀 (pip install -r requirements.txt)"
fi

echo "LLM_PROVIDER=$LLM_PROVIDER · 챗봇 http://localhost:8000/docs · 진단 http://localhost:8100/docs · UI http://localhost:8501"
wait
