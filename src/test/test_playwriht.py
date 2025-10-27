from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    out_file = Path("screenshot.png")

    with sync_playwright() as p:
        # Use o Edge do sistema:
        # browser = p.chromium.launch(channel="msedge", headless=False, slow_mo=100)

        # Ou use o Chromium baixado pelo Playwright (recomendado p/ teste):
        browser = p.chromium.launch(headless=False, slow_mo=150)

        page = browser.new_page()
        page.on(
            "console", lambda msg: print("[console]", msg.text)
        )  # log do console da página
        page.goto("https://example.com", wait_until="domcontentloaded")
        print("Título da página:", page.title())

        page.screenshot(path=str(out_file), full_page=True)
        print(f"Screenshot salvo em: {out_file.resolve()}")

        browser.close()
        print("Feito com sucesso ✅")


if __name__ == "__main__":
    main()
