"""설정 파일 로더 (configs/*.yaml)."""

from __future__ import annotations

from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "configs"


def load_yaml(relative: str) -> dict:
    return yaml.safe_load((CONFIG_DIR / relative).read_text(encoding="utf-8"))


def load_diagnosis_config() -> dict:
    return load_yaml("diagnosis.yaml")


def load_domain_config(domain: str = "insurance") -> dict:
    return load_yaml(f"domains/{domain}.yaml")
