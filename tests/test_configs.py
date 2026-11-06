from common.settings import load_diagnosis_config, load_domain_config


def test_diagnosis_config_has_items_and_repetitions():
    cfg = load_diagnosis_config()
    assert cfg["repetitions"] >= 1
    assert {"2.6.3", "3.1.3", "2.5.1"} <= {item["id"] for item in cfg["items"]}


def test_insurance_domain_config_roles():
    cfg = load_domain_config("insurance")
    assert set(cfg["roles"]) == {"guest", "customer", "agent", "admin"}
    assert cfg["llm"]["provider"] == "mock"
