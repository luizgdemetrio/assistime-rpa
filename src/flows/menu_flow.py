# src/flows/menu_flow.py
from playwright.sync_api import Page


def ir_para_custo_puro(page: Page, sel: dict):
    # Abre Financeiro
    if sel.get("btn_financeiro", "").startswith("role="):
        page.get_by_role("button", name="Financeiro", exact=False).click()
    else:
        page.locator(sel["btn_financeiro"]).click()

    # Clica Custo Puro
    if sel.get("link_custo_puro", "").startswith("role="):
        page.get_by_role("link", name="Custo Puro", exact=False).click()
    else:
        page.locator(sel["link_custo_puro"]).click()

    page.wait_for_load_state("networkidle")
