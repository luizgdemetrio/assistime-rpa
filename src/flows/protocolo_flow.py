# src/flows/protocolo_flow.py
from playwright.sync_api import Page, TimeoutError as PWTimeout


def _usar_filtro(page: Page, filtro_sel: str, texto: str):
    f = page.locator(filtro_sel)
    if f.count():
        f.first.fill("")
        f.first.fill(texto)
        page.keyboard.press("Enter")
        page.wait_for_load_state("networkidle")


def abrir_visualizar_do_protocolo(page: Page, protocolo: str, sel: dict):
    # Tenta usar filtro/ busca, se existir
    if sel.get("filtro_busca"):
        try:
            _usar_filtro(page, sel["filtro_busca"], protocolo)
        except PWTimeout:
            pass

    # Procura linha que contém o protocolo
    linhas = page.locator(sel["grid_linhas"])
    n = linhas.count()
    if n == 0:
        raise RuntimeError(
            "Grid não carregou (0 linhas). Ajuste 'grid_linhas' no config.yaml."
        )

    alvo_idx = -1
    for i in range(n):
        txt = linhas.nth(i).inner_text(timeout=10000)
        if protocolo in txt:
            alvo_idx = i
            break
    if alvo_idx < 0:
        raise RuntimeError(f"Protocolo {protocolo} não encontrado na grid.")

    linha = linhas.nth(alvo_idx)

    # Abre menu "Mais" dessa linha (três pontinhos)
    mais = linha.locator(sel["menu_mais"])
    if not mais.count():
        # fallback: procurar por texto "Mais" dentro da linha
        mais = linha.get_by_text("Mais", exact=False)
    mais.first.click()

    # Clica "Visualizar"
    page.locator(sel["acao_visualizar"]).first.click()

    page.wait_for_load_state("networkidle")
