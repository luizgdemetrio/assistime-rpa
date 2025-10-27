# src/flows/login_flow.py
import os
from playwright.sync_api import Page, expect


def do_login(page: Page, base_url: str):
    # 1) Abrir página de login
    page.goto(base_url, wait_until="domcontentloaded")

    # 2) Preencher campos pelos rótulos acessíveis (do seu HTML: aria-label="Login"/"Senha")
    page.get_by_label("Login").click()
    page.get_by_label("Login").fill(os.environ["ASSISTME_USER"])

    page.get_by_label("Senha").click()
    page.get_by_label("Senha").fill(os.environ["ASSISTME_PASS"])

    # (Opcional) Marcar "Lembrar Senha"
    # page.get_by_role("checkbox", name="Lembrar Senha").check()

    # 3) Entrar
    page.get_by_role("button", name="Entrar").click()

    # 4) Esperar rede ociosa e confirmar que NÃO estamos mais na rota de login
    page.wait_for_load_state("networkidle")
    # Estratégia 1: URL não contém '/login'
    assert (
        "/login" not in page.url.lower()
    ), f"Parece que ainda estamos no login: {page.url}"

    # Estratégia 2 (se preferir): esperar um elemento típico do pós-login
    # ex.: o menu lateral, ou um link "Financeiro"
    # expect(page.get_by_role("button", name="Financeiro")).to_be_visible(timeout=15000)
