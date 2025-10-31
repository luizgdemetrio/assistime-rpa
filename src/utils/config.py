# src/utils/config.py
from __future__ import annotations
import os
import yaml

DEFAULT_CONFIG = {
    "seletores": {
        "btn_financeiro": 'role=button[name="Financeiro"]',
        "link_custo_puro": 'role=link[name="Custo Puro"]',
        "grid_linhas": 'css=div[role="row"]',
        "menu_mais": 'css=button[aria-label="Mais"], css=button:has-text("Mais"), css=[data-testid="more"]',
        "acao_visualizar": "text=Visualizar",
        "filtro_busca": 'css=input[placeholder*="Buscar"], css=input[type="search"]',
    },
    "downloads_root": "./data",
}


def load_config(path: str = "config.yaml") -> dict:
    if not os.path.exists(path):
        print(f"⚠️  {path} não encontrado. Usando DEFAULT_CONFIG.")
        return DEFAULT_CONFIG

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    # merge rústico: defaults <- arquivo
    cfg = DEFAULT_CONFIG.copy()
    for k, v in (data or {}).items():
        if isinstance(v, dict) and isinstance(cfg.get(k), dict):
            cfg[k].update(v)
        else:
            cfg[k] = v
    return cfg
