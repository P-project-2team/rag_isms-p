"""Streamlit UI (:8501) — 실행 뼈대. 두 API의 상태만 보여준다.

실행: streamlit run ui/Home.py --server.port 8501
페이지(챗봇 / 진단 실행 / 대시보드 / 보고서)는 설계서 v2 §7.5대로 ui/pages/에 추가한다.
"""

import os

import httpx
import streamlit as st

st.set_page_config(page_title="RAG ISMS-P 진단", layout="wide")
st.title("RAG 서비스 보안 자동진단 · ISMS-P 매핑")

services = {
    "타깃 챗봇": os.getenv("TARGET_CHATBOT_URL", "http://localhost:8000"),
    "진단 엔진": os.getenv("DIAG_ENGINE_URL", "http://localhost:8100"),
}

cols = st.columns(len(services))
for col, (name, url) in zip(cols, services.items(), strict=True):
    with col:
        st.subheader(name)
        try:
            data = httpx.get(f"{url}/health", timeout=2).json()
            st.success(f"정상 · {url}")
            st.json(data)
        except httpx.HTTPError as exc:
            st.error(f"연결 안 됨 · {url}")
            st.caption(str(exc))
